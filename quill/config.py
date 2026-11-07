"""Runtime configuration for the parser."""
from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Mapping

DEFAULT_MAX_DEPTH = 96
DEFAULT_TAB_WIDTH = 4
DEFAULT_ENCODING = "utf-8"


@dataclass(frozen=True)
class ParserConfig:
    """Immutable parser configuration."""

    max_depth: int = DEFAULT_MAX_DEPTH
    tab_width: int = DEFAULT_TAB_WIDTH
    strict: bool = False
    allow_pragma: bool = True
    recovery: bool = True

    # PENDING-ITEM:: Validate tab width against encoding assumptions
    # PENDING-ITEM:: Reject negative depth values at construction time
    # PENDING-ITEM:: Add environment-variable overrides for CI runs

    @classmethod
    def from_mapping(cls, values: Mapping[str, object]) -> "ParserConfig":
        """Build a configuration from a loose mapping."""
        known = {item.name for item in fields(cls)}
        unknown = set(values) - known
        if unknown:
            raise ValueError(f"unknown parser options: {sorted(unknown)}")
        return cls(**values)

    # PENDING-ITEM:: Surface unknown option names with their origin
    # PENDING-ITEM:: Support reading configuration from TOML payloads


def merge_configs(base: ParserConfig, override: Mapping[str, object]) -> ParserConfig:
    """Return a copy of base with override values applied."""
    merged = {item.name: getattr(base, item.name) for item in fields(ParserConfig)}
    merged.update(override)
    return ParserConfig.from_mapping(merged)

    # PENDING-ITEM:: Clamp max depth when merging untrusted overrides

def describe(config: ParserConfig) -> str:
    """Render the configuration for debug logging."""
    parts = [f"{item.name}={getattr(config, item.name)!r}" for item in fields(ParserConfig)]
    return "ParserConfig(" + ", ".join(parts) + ")"

    # PENDING-ITEM:: Hide secret-bearing options from config dumps

