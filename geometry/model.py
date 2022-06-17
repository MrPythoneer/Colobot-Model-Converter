from dataclasses import dataclass, field
from geometry.triangle import Triangle


@dataclass(slots=True)
class Model:
    triangles: list[Triangle] = field(default_factory=list)
    version: int = -1