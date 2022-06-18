from dataclasses import dataclass


@dataclass(slots=True)
class Vector3D:
    x: float
    y: float
    z: float


    def __iter__(self):
        return iter((self.x, self.y, self.z))
