# -*- coding: utf-8 -*-
# Implements Colobot geometry specification
# Copyright (c) 2014 Tomasz Kapuściński

class TexCoord:
    u: float
    v: float

    def __init__(self, u: float, v: float):
        self.u = u
        self.v = v

    def __eq__(self, other: 'TexCoord'):
        return abs(self.u - other.u) < 1e-3 and abs(self.v - other.v) < 1e-3

    def __ne__(self, other: 'TexCoord'):
        return not self == other
