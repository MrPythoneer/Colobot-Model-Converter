# -*- coding: utf-8 -*-
# Implements Colobot geometry specification
# Copyright (c) 2014 Tomasz Kapuściński

class Normal:
    x: float
    y: float
    z: float

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, other: 'Normal'):
        return (abs(self.x - other.x) < 1e-3) and (abs(self.y - other.y) < 1e-3) and (abs(self.z - other.z) < 1e-3)

    def __ne__(self, other: 'Normal'):
        return not self == other