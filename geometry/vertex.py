# -*- coding: utf-8 -*-
# Implements Colobot geometry specification
# Copyright (c) 2014 Tomasz Kapuściński

from geometry.vector3d import Vector3D
from geometry.texcoord import TexCoord


class Vertex:
    x: float
    y: float
    z: float
    nx: float
    ny: float
    nz: float
    u1: float
    v1: float
    u2: float
    v2: float

    def __init__(self,
                 vertex: Vector3D = Vector3D(0, 0, 0),
                 normal: Vector3D = Vector3D(0, 0, 0),
                 tex1: TexCoord = TexCoord(0.0, 0.0),
                 tex2: TexCoord = TexCoord(0.0, 0.0)
                 ):
        self.x = vertex.x
        self.y = vertex.y
        self.z = vertex.z
        self.nx = normal.x
        self.ny = normal.y
        self.nz = normal.z
        self.u1 = tex1.u
        self.v1 = tex1.v
        self.u2 = tex2.u
        self.v2 = tex2.v