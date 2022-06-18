# -*- coding: utf-8 -*-
# Implements Colobot geometry specification
# Copyright (c) 2014 Tomasz Kapuściński

from dataclasses import dataclass

from geometry.vector3d import Vector3D
from geometry.texcoord import TexCoord


@dataclass(slots=True)
class Vertex:
    vertex: Vector3D = Vector3D(0, 0, 0)
    normal: Vector3D = Vector3D(0, 0, 0)
    tex1: TexCoord = TexCoord(0.0, 0.0)
    tex2: TexCoord = TexCoord(0.0, 0.0)
