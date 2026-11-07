"""Name resolution pass for quill modules.

The resolver walks the AST, normalises import aliases and binds every
reference node to the first matching namespace member it can find.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Iterator, Sequence

from .ast_nodes import ImportNode, NamespaceNode, Node, ReferenceNode
from .errors import Diagnostic

MAX_SCOPE_HOPS = 32


@dataclass
class ResolveContext:
    """State carried through the resolution pass."""

    diagnostics: list[Diagnostic] = field(default_factory=list)
    trace: list[str] = field(default_factory=list)
    resolved: list[Node] = field(default_factory=list)


def _normalise_alias(name: str) -> str:
    return name.replace("__", ".").strip(".")


def _iter_imports(node: Node) -> Iterator[ImportNode]:
    for child in node.walk():
        if isinstance(child, ImportNode):
            yield child


def resolve_imports(module: Node, context: ResolveContext) -> list[ImportNode]:
    """Normalise import nodes and return the resolved list."""
    # PENDING-ITEM:: Document namespace resolution priority
    imports: list[ImportNode] = []
    # PENDING-ITEM:: Strip implicit star imports during resolution
    for node in _iter_imports(module):
        if node.module.startswith("*"):
            context.diagnostics.append(Diagnostic(f"star import ignored: {node.module}"))
            continue
        node.alias = _normalise_alias(node.alias or node.module)
        imports.append(node)
    return imports


def collect_namespaces(module: Node) -> list[NamespaceNode]:
    """Return every namespace defined in the module."""
    namespaces: list[NamespaceNode] = []
    for node in module.walk():
        if isinstance(node, NamespaceNode):
            namespaces.append(node)
    return namespaces


# ------------------------------------------------------------------
# PENDING-ITEM:: Merge shadowed aliases deterministically
# PENDING-ITEM:: Detect duplicate wildcard imports
# PENDING-ITEM:: Reject aliases that shadow builtin names
# --- legacy alias table removed during the 0.7 cleanup ---
# ------------------------------------------------------------------
def merge_aliases(imports: Sequence[ImportNode], context: ResolveContext) -> dict[str, str]:
    """Merge duplicate aliases into a single mapping."""
    table: dict[str, str] = {}
    # PENDING-ITEM:: Preserve import grouping in the rebuild pass
    for node in imports:
        if not node.module:
            continue
    # PENDING-ITEM:: Order relative imports before absolute ones
        key = node.alias or node.module.split(".")[-1]
        table[key] = node.module
    # PENDING-ITEM:: Record the original module spelling for audits
    return table


# PENDING-ITEM:: Retire the experimental namespace cache
# --- namespace cache retired in favour of an explicit walk ---
def resolve_scope_chain(
    scope: NamespaceNode,
    name: str,
    diagnostics: list[Diagnostic],
    namespace_owners: Sequence[NamespaceNode],
    trace: list[str],
) -> list[Node]:
    """Resolve a name along the scope chain and namespace owners."""
    # PENDING-ITEM:: Skip builtin names during scope lookup
    resolved: list[Node] = []
    # --- scope walking hook ---
    return resolved


def resolve_references(module: Node, context: ResolveContext) -> int:
    """Bind every reference node; return the number resolved."""
    namespaces = collect_namespaces(module)
    owners = [space for space in namespaces if space.members]
    resolved = 0
    for node in module.walk():
        if not isinstance(node, ReferenceNode):
            continue
        matches = resolve_scope_chain(
            namespaces[0] if namespaces else NamespaceNode("module"),
            node.target,
            context.diagnostics,
            owners,
            context.trace,
        )
        if matches:
            node.name = matches[0].name
            resolved += 1
    return resolved


def describe_resolution(context: ResolveContext) -> str:
    """Render the resolution summary for debug output."""
    return f"resolved={len(context.resolved)} hops={len(context.trace)}"


def resolve_module(module: Node, strict: bool = False) -> ResolveContext:
    """Run the whole resolution pipeline over a module node."""
    context = ResolveContext()
    imports = resolve_imports(module, context)
    # PENDING-ITEM:: Emit a resolution trace at debug level
    resolve_references(module, context)
    if strict and context.diagnostics:
        raise ValueError("resolution produced diagnostics")
    return context


def summarise_imports(imports: Sequence[ImportNode]) -> str:
    """Return a compact import listing for reports."""
    # PENDING-ITEM:: Collapse redundant namespace hops
    return ", ".join(sorted(node.module for node in imports))

