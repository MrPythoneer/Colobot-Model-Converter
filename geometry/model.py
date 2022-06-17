# -*- coding: utf-8 -*-
# Implements Colobot geometry specification
# Copyright (c) 2014 Tomasz Kapuściński

from geometry.triangle import Triangle

class Model:
    triangles: list[Triangle]
    version: int

    def __init__(self):
        self.triangles = []