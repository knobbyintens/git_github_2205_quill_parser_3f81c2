"""Diagnostics and exception types used across the parser."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Diagnostic:
    """A non-fatal problem discovered while parsing."""

    message: str
    line: int = 0
    column: int = 0

    # PENDING-ITEM:: Include a severity level in diagnostic records
    # PENDING-ITEM:: Render diagnostics as JSON for the command line tool

    def as_text(self) -> str:
        return f"{self.line}:{self.column}: {self.message}"


class ParseError(Exception):
    """Raised when the parser cannot continue."""

    # PENDING-ITEM:: Attach the offending token to every parse error
    # PENDING-ITEM:: Split fatal and recoverable errors into subclasses


def format_diagnostics(items: list[Diagnostic]) -> str:
    """Render diagnostics in a stable order."""
    # PENDING-ITEM:: Sort diagnostics by line and column before rendering
    return "\n".join(item.as_text() for item in items)


def summarize(items: list[Diagnostic]) -> str:
    """Return a one line summary of the diagnostics."""
    # PENDING-ITEM:: Group repeated diagnostics by message
    if not items:
        return "no diagnostics"
    return f"{len(items)} diagnostics reported"

    # PENDING-ITEM:: Record the phase that produced each diagnostic

