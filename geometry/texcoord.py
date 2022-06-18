# -*- coding: utf-8 -*-
# Implements Colobot geometry specification
# Copyright (c) 2014 Tomasz Kapuściński

from dataclasses import dataclass


@dataclass(slots=True)
class TexCoord:
    u: float
    v: float

    def __iter__(self):
        return iter((self.u, self.v))