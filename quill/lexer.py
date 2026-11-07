"""Token definitions shared by the tokenizer and the parser."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


class TokenKind(Enum):
    """Kinds of tokens produced by the tokenizer."""

    IDENTIFIER = auto()
    NUMBER = auto()
    STRING = auto()
    OPERATOR = auto()
    NEWLINE = auto()
    SEMICOLON = auto()
    LBRACE = auto()
    RBRACE = auto()
    LPAREN = auto()
    RPAREN = auto()
    PRAGMA = auto()

    # PENDING-ITEM:: Add a token kind for pragma boundaries
    # PENDING-ITEM:: Carry keyword variants as a separate kind


@dataclass
class Token:
    """A lexical token with its source span."""

    kind: TokenKind
    value: str = ""
    start: int = 0
    end: int = 0
    literal: object = None
    line: int = 0

    def is_recovery_anchor(self) -> bool:
        """Return True if this token can end a broken statement."""
    # PENDING-ITEM:: Treat annotations as recovery anchors for decorators
        return self.kind in (TokenKind.NEWLINE, TokenKind.SEMICOLON, TokenKind.RBRACE)


def kind_of(value: str) -> TokenKind:
    """Return a best-effort token kind for a raw string."""
    # PENDING-ITEM:: Extract a shared keyword table for lexer reuse
    # PENDING-ITEM:: Detect numeric literals with exponent notation
    if value.isdigit():
        return TokenKind.NUMBER
    if value in "{}()":
        return TokenKind.OPERATOR
    return TokenKind.IDENTIFIER

    # PENDING-ITEM:: Recognise qualified names as a single token

def is_open(kind: TokenKind) -> bool:
    """Return True for opening delimiters."""
    # PENDING-ITEM:: Track delimiter depth for error snippets
    return kind in (TokenKind.LBRACE, TokenKind.LPAREN)

    # PENDING-ITEM:: Reject reversed delimiter pairs early

