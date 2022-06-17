# -*- coding: utf-8 -*-
# Implements Colobot geometry specification
# Copyright (c) 2014 Tomasz Kapuściński

from dataclasses import dataclass, field


from geometry.vertex import Vertex 
from geometry.material import Material


@dataclass(slots=True)
class Triangle:
    vertices: list[Vertex] = field(default_factory=lambda: [Vertex(), Vertex(), Vertex()])
    material: Material = Material()