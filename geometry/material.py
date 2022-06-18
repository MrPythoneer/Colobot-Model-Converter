from dataclasses import dataclass, field


@dataclass(slots=True)
class Material:
    name: str = ''
    texture1: str = ''
    texture2: str = ''
    ambient: list[float] = field(default_factory=lambda: [0.0, 0.0, 0.0, 0.0])
    diffuse: list[float] = field(default_factory=lambda: [0.8, 0.8, 0.8, 0.0])
    specular: list[float] = field(default_factory=lambda: [0.5, 0.5, 0.5, 0.0])
    state: int = 0
    version: int = 2
    lod: int = 0