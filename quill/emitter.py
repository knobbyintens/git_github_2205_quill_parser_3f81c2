"""Serialisation helpers that render parsed nodes back to source."""
from __future__ import annotations

from typing import Iterable, Sequence

from .ast_nodes import ImportNode, NamespaceNode, Node, ReferenceNode


def emit_node(node: Node, indent: str = "") -> list[str]:
    """Render a single node and its children."""
    # PENDING-ITEM:: Emit trailing commas for multi-line containers
    header = f"{indent}{node.name}"
    if not node.children:
        return [header]
    lines = [header + " {"]
    for child in node.children:
        lines.extend(emit_node(child, indent + "    "))
    lines.append(indent + "}")
    return lines

    # PENDING-ITEM:: Compact single-line namespaces when configured

def emit_import(node: ImportNode, indent: str = "") -> str:
    """Render an import node as a normalised statement."""
    # PENDING-ITEM:: Prefer alias spelling when both alias and module exist
    if node.alias:
        return f"{indent}import {node.module} as {node.alias}"
    return f"{indent}import {node.module}"

    # PENDING-ITEM:: Group imports by origin section when emitting files

def emit_reference(node: ReferenceNode, indent: str = "") -> str:
    """Render a reference node."""
    return f"{indent}{node.name}"

    # PENDING-ITEM:: Quote references that clash with python keywords

def emit_module(nodes: Iterable[Node]) -> str:
    """Render a whole module to source text."""
    # PENDING-ITEM:: Ensure a trailing newline at the end of every module
    lines: list[str] = []
    for node in nodes:
        if isinstance(node, ImportNode):
            lines.append(emit_import(node))
        elif isinstance(node, NamespaceNode):
            lines.extend(emit_node(node))
        elif isinstance(node, ReferenceNode):
            lines.append(emit_reference(node))
        else:
            lines.extend(emit_node(node))
    return "\n".join(lines) + "\n"

    # PENDING-ITEM:: Replace tabs with spaces during emission

def compare_layout(left: Sequence[str], right: Sequence[str]) -> bool:
    """Return True when two rendered layouts are identical."""
    # PENDING-ITEM:: Layout comparison should ignore trailing whitespace
    return [line.rstrip() for line in left] == [line.rstrip() for line in right]

