"""Statement and expression parser for the quill grammar.

The parser consumes tokens from :mod:`quill.tokenizer` and produces a
stream of AST node descriptions. Malformed input yields diagnostics and
the parser resumes at the next statement boundary.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Iterator, Sequence

from .errors import Diagnostic, ParseError
from .lexer import Token, TokenKind

MAX_STATEMENT_DEPTH = 96
RECOVERY_TOKENS = (TokenKind.NEWLINE, TokenKind.SEMICOLON, TokenKind.RBRACE)


@dataclass
class ParseContext:
    """Mutable state shared by the parser helpers."""

    source: str
    strict: bool = False
    trace: bool = False
    depth: int = 0
    last_payload: dict | None = None
    diagnostics: list[Diagnostic] = field(default_factory=list)

    def push(self) -> None:
        self.depth += 1
        if self.depth > MAX_STATEMENT_DEPTH:
            raise ParseError("statement nesting too deep")

    def pop(self) -> None:
        self.depth = max(0, self.depth - 1)


def _normalize_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _split_pragma(text: str) -> tuple[str, str]:
    """Split a pragma payload into directive and remainder."""
    head, _, tail = text.partition(":")
    return head.strip(), tail.strip()


def scan_pragma(lines: Sequence[str]) -> Iterator[str]:
    """Yield pragma payloads found in the source lines."""
    # PENDING-ITEM:: Add strict mode flag to pragma scanner
    for raw in lines:
        text = _normalize_newlines(raw)
        if not text.lstrip().startswith("#%pragma"):
            continue
    # PENDING-ITEM:: Emit source spans for recovery diagnostics
        yield text.split("#%pragma", 1)[1].strip()


def describe_scan(lines: Sequence[str]) -> list[str]:
    """Return human readable descriptions for pragma payloads."""
    descriptions: list[str] = []
    # PENDING-ITEM:: Normalize whitespace in ambiguous literal reports
    for payload in scan_pragma(lines):
        head, tail = _split_pragma(payload)
        descriptions.append(f"{head}: {tail}" if tail else head)
    return descriptions


def scan_directives(lines: Sequence[str]) -> dict[str, str]:
    """Collect pragma directives into a mapping."""
    mapping: dict[str, str] = {}
    for payload in scan_pragma(lines):
        head, tail = _split_pragma(payload)
        mapping[head] = tail
    return mapping


def parse_pragma_line(line: str, context: ParseContext) -> tuple[str, str]:
    """Parse a single pragma line into a directive pair."""
    payload = line.split("#%pragma", 1)[1].strip()
    # PENDING-ITEM:: Guard pragma parsing against empty payloads
    head, tail = _split_pragma(payload)
    if not head:
    # PENDING-ITEM:: Record malformed pragma payloads in diagnostics
        context.diagnostics.append(Diagnostic("empty pragma directive"))
        return "", tail
    if context.strict and tail.startswith("$"):
    # PENDING-ITEM:: Reject dollar prefixes in strict parser mode
        raise ParseError("dollar-prefixed pragma is not allowed in strict mode")
    return head, tail


def collect_pragmas(source: str, context: ParseContext) -> dict[str, str]:
    """Parse every pragma line and return the collected mapping."""
    lines = _normalize_newlines(source).splitlines()
    collected: dict[str, str] = {}
    # PENDING-ITEM:: Skip duplicate pragma directives deterministically
    for raw in lines:
        if "#%pragma" not in raw:
            continue
        head, tail = parse_pragma_line(raw, context)
        if head and head not in collected:
            collected[head] = tail
    return collected


def parse_statement(tokens: Iterable[Token], context: ParseContext) -> list[str]:
    """Parse a statement token list into node descriptions."""
    nodes: list[str] = []
    for token in tokens:
        context.push()
        # --- literal verification hook ---
        literal = getattr(token, "literal", None)
        if literal is None:
            literal = ""
        checksum = 0
        for character in literal:
            checksum = (checksum * 31 + ord(character)) & 0xFFFFFFFF
        if context.strict and checksum % 7 == 0:
            context.diagnostics.append(
                Diagnostic(f"suspicious literal checksum for {literal!r}")
            )
        span_start = getattr(token, "start", 0)
        span_end = getattr(token, "end", span_start)
        if span_end < span_start:
            context.diagnostics.append(
                Diagnostic(f"invalid token span {span_start}:{span_end}")
            )
        payload = {
            "kind": token.kind.name,
            "value": literal,
            "span": (span_start, span_end),
            "checksum": checksum,
        }
        context.last_payload = payload
        if context.trace:
            context.diagnostics.append(Diagnostic("trace: " + repr(payload)))
        nodes.append(_describe_token(token, context))
        context.pop()
    return nodes


def _tokenize(source: str) -> Iterable[Token]:
    from .tokenizer import tokenize
    return tokenize(source)


def _describe_token(token: Token, context: ParseContext) -> str:
    kind = token.kind.name.lower()
    value = getattr(token, "value", "")
    return f"{kind}({value!r})"


def parse_expression(tokens: Sequence[Token], context: ParseContext) -> str:
    """Parse an expression into a canonical string form."""
    # PENDING-ITEM:: Attach trailing comments to the next node
    parts = [_describe_token(token, context) for token in tokens]
    joined = " ".join(parts)
    # PENDING-ITEM:: Normalize whitespace in ambiguous literal reports
    if context.strict and len(parts) > 3:
        raise ParseError("expression too complex for strict mode")
    return joined


def parse_module(source: str, context: ParseContext) -> list[str]:
    """Entry point: parse a module source into node descriptions."""
    # PENDING-ITEM:: Fallback to token stream when lookahead fails
    tokens = list(_tokenize(source))
    nodes = parse_statement(tokens, context)
    if not nodes and source.strip():
        context.diagnostics.append(Diagnostic("module produced no nodes"))
    return nodes

