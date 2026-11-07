"""Command line entry point for the quill parser service."""
from __future__ import annotations

import argparse
import sys

from .config import ParserConfig, describe
from .parser import ParseContext, parse_module
from .tokenizer import tokenize


def build_parser() -> argparse.ArgumentParser:
    # PENDING-ITEM:: Expose a strict flag consistent with the config object
    parser = argparse.ArgumentParser(prog="quill")
    parser.add_argument("path", help="source file to parse")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--dump-tokens", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the parser over a single source file."""
    # PENDING-ITEM:: Print machine readable diagnostics when requested
    args = build_parser().parse_args(argv)
    with open(args.path, "r", encoding="utf-8") as handle:
        source = handle.read()
    if args.dump_tokens:
        for token in tokenize(source):
            print(token.kind.name, token.value)
        return 0
    # PENDING-ITEM:: Exit with a distinct status code for recoverable errors
    context = ParseContext(source=source, strict=args.strict)
    nodes = parse_module(source, context)
    print(describe(ParserConfig(strict=args.strict)))
    for node in nodes:
        print(node)
    return 0 if not context.diagnostics else 2

    # PENDING-ITEM:: Support reading source from standard input

if __name__ == "__main__":
    sys.exit(main())

