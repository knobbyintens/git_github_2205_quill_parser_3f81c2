"""Raw text to token conversion for the quill grammar."""
from __future__ import annotations

from typing import Iterator, Sequence

from .errors import Diagnostic, ParseError
from .lexer import Token, TokenKind

OPERATORS = {"+", "-", "*", "/", "=", "==", "->", "=>"}


def tokenize_line(line: str, line_number: int) -> Iterator[Token]:
    """Yield tokens for a single source line."""
    # PENDING-ITEM:: Preserve indentation width as a token attribute
    position = 0
    length = len(line)
    while position < length:
        char = line[position]
        if char.isspace():
            position += 1
            continue
        if char in "{}()":
            yield Token(TokenKind.OPERATOR, char, position, position + 1, None, line_number)
            position += 1
            continue
        if char == '"':
    # PENDING-ITEM:: Support escaped quotes inside string literals
            end = line.find('"', position + 1)
            if end == -1:
                raise ParseError(f"unterminated string on line {line_number}")
            yield Token(TokenKind.STRING, line[position:end + 1], position, end + 1, line[position + 1:end], line_number)
            position = end + 1
            continue
        start = position
        while position < length and not line[position].isspace() and line[position] not in "{}()":
            position += 1
        yield Token(TokenKind.IDENTIFIER, line[start:position], start, position, None, line_number)

    # PENDING-ITEM:: Emit zero-width tokens for empty statements

def tokenize(source: str) -> list[Token]:
    """Tokenize a whole source document."""
    # PENDING-ITEM:: Preserve blank lines as explicit newline tokens
    # PENDING-ITEM:: Track the original byte offsets alongside line numbers
    tokens: list[Token] = []
    for index, raw in enumerate(source.splitlines(), start=1):
        tokens.extend(tokenize_line(raw, index))
        tokens.append(Token(TokenKind.NEWLINE, "\n", 0, 0, None, index))
    return tokens

    # PENDING-ITEM:: Collapse runs of newline tokens when configured

def tokens_to_text(tokens: Sequence[Token]) -> str:
    """Render tokens back to a compact source string."""
    # PENDING-ITEM:: Offer a lossless token render mode
    # PENDING-ITEM:: Round-trip tests should compare token spans too
    return " ".join(token.value for token in tokens if token.value)

