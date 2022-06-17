# -*- coding: utf-8 -*-
# Implements Colobot geometry specification
# Copyright (c) 2014 Tomasz Kapuściński

from geometry.vertex import Vertex 
from geometry.material import Material

class Triangle:
    vertices: list[Vertex]
    material: 'Material'

    def __init__(self):
        self.vertices = [Vertex(), Vertex(), Vertex()]
        self.material = Material()
