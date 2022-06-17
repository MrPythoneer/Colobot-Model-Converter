# -*- coding: utf-8 -*-
# Implements Colobot geometry specification
# Copyright (c) 2014 Tomasz Kapuściński

class Material:
    texture: str
    texture2: str
    ambient: list[float]
    diffuse: list[float]
    specular: list[float]
    state: int
    version: int
    lod: int

    def __init__(self):
        self.texture = ''
        self.texture2 = ''
        self.ambient = [0.0, 0.0, 0.0, 0.0]
        self.diffuse = [0.8, 0.8, 0.8, 0.0]
        self.specular = [0.5, 0.5, 0.5, 0.0]
        self.state = 0
        self.version = 2
        self.lod = 0

    def __eq__(self, other: 'Material'):
        if self.texture != other.texture:
            return False
        if self.texture2 != other.texture2:
            return False
        if self.state != other.state:
            return False
        if self.lod != other.lod:
            return False

        for i in range(4):
            if abs(self.ambient[i] - other.ambient[i]) > 1e-3:
                return False
            if abs(self.diffuse[i] - other.diffuse[i]) > 1e-3:
                return False
            if abs(self.specular[i] - other.specular[i]) > 1e-3:
                return False

        return True

    def __ne__(self, other: 'Material'):
        return not self == other
