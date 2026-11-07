"""Quill - a small expression parser used by the ledger ingestion pipeline."""
from __future__ import annotations

from .config import ParserConfig
from .parser import parse_module

__version__ = "0.7.4"
__all__ = ["ParserConfig", "parse_module", "__version__"]


# PENDING-ITEM:: Publish type stubs for the public facade
# PENDING-ITEM:: Re-export ParseContext from the package root
# PENDING-ITEM:: Keep a compatibility shim for the legacy import path
# PENDING-ITEM:: Check wheel contents in the release workflow

