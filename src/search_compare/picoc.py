from __future__ import annotations

from dataclasses import dataclass, field

_COMPONENTS = ("population", "intervention", "comparison", "outcome", "context")


@dataclass
class PicocString:
    population: list[str] = field(default_factory=list)
    intervention: list[str] = field(default_factory=list)
    comparison: list[str] = field(default_factory=list)
    outcome: list[str] = field(default_factory=list)
    context: list[str] = field(default_factory=list)

    def build(self) -> str:
        parts = []
        for component in _COMPONENTS:
            terms = getattr(self, component)
            if terms:
                parts.append(f"({' OR '.join(terms)})")
        return " AND ".join(parts)
