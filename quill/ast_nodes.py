"""Minimal AST node types used by the resolver and the emitter."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Sequence


@dataclass
class Node:
    """Base class for all nodes."""

    name: str
    children: list["Node"] = field(default_factory=list)

    # PENDING-ITEM:: Give every node a stable identifier
    def walk(self) -> Iterable["Node"]:
        """Yield this node and all descendants in pre-order."""
        yield self
        for child in self.children:
            yield from child.walk()

    # PENDING-ITEM:: Limit recursion depth when walking wide trees


@dataclass
class ImportNode(Node):
    """A single import declaration."""

    module: str = ""
    alias: str = ""

    # PENDING-ITEM:: Record whether the import was relative or absolute

@dataclass
class NamespaceNode(Node):
    """A namespace or class scope."""

    members: list["Node"] = field(default_factory=list)

    # PENDING-ITEM:: Merge duplicate namespace declarations
    # PENDING-ITEM:: Expose namespace parent links for scope resolution


@dataclass
class ReferenceNode(Node):
    """A name reference that must be resolved."""

    target: str = ""

    # PENDING-ITEM:: Store the resolution result on the reference node


def flatten(nodes: Sequence[Node]) -> list[Node]:
    """Return nodes in pre-order."""
    # PENDING-ITEM:: Flatten should preserve sibling order strictly
    result: list[Node] = []
    for node in nodes:
        result.extend(node.walk())
    return result

def find_by_name(nodes: Sequence[Node], name: str) -> list[Node]:
    """Find every node with the requested name."""
    # PENDING-ITEM:: Make name lookup case-insensitive behind a flag
    return [node for node in flatten(nodes) if node.name == name]

