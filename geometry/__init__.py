# -*- coding: utf-8 -*-
# Implements Colobot geometry specification
# Copyright (c) 2014 Tomasz Kapuściński


from geometry.material import Material
from geometry.model import Model
from geometry.texcoord import TexCoord
from geometry.triangle import Triangle
from geometry.vector3d import Vector3D
from geometry.vertex import Vertex

Normal = Vector3D
VertexCoord = Vector3D


def triangulate(vertices: list[Vertex], flip_order: bool = False) -> list[Triangle]:
    """Triangulates polygon"""
    result: list[Triangle] = []

    first = vertices[0]
    third = vertices[1]

    count = len(vertices)

    for i in range(2, count):
        second = third
        third = vertices[i]

        triangle = Triangle()

        # reverses order
        if flip_order:
            second, third = third, second

        triangle.vertices[0] = first
        triangle.vertices[1] = second
        triangle.vertices[2] = third

        result.append(triangle)

    return result


def encode_state(state: str) -> int:
    """Encodes state to number"""
    result = 0

    for st in state.split(','):
        value = state_to_number.get(st, 0)
        result |= value

    return result


def decode_state(state: int) -> str:
    """Decodes state from number"""
    labels: list[str] = []

    if state != 0:
        for i in range(21):
            mask = 1 << i
            if (state & mask) != 0:
                labels.append(state_to_string[mask])
    else:
        labels.append('normal')

    return ','.join(labels)


def add_state(text: str, number: int) -> None:
    state_to_number[text] = number
    state_to_string[number] = text


# state dictionary
state_to_number: dict[str, int] = {}
state_to_string: dict[int, str] = {}


add_state('normal', 0)                      # standard texture
add_state('ttexture_black', 1 << 0)         # black texture is transparent
add_state('ttexture_white', 1 << 1)         # white texture is transparent
add_state('ttexture_diffuse', 1 << 2)       # transparent texture
add_state('wrap', 1 << 3)                   # wrap mode
add_state('clamp', 1 << 4)                  # clamp mode
add_state('light', 1 << 5)                  # completely bright
add_state('dual_black', 1 << 6)             # dual black ?
add_state('dual_white', 1 << 7)             # dual white ?
add_state('part1', 1 << 8)                  # part 1
add_state('part2', 1 << 9)                  # part 2
add_state('part3', 1 << 10)                 # part 3
add_state('part4', 1 << 11)                 # part 4
add_state('2face', 1 << 12)                 # render both faces
add_state('alpha', 1 << 13)                 # alpha channel is transparency
add_state('second', 1 << 14)                # use second texture
add_state('fog', 1 << 15)                   # render fog
add_state('tcolor_black', 1 << 16)          # black color is transparent
add_state('tcolor_white', 1 << 17)          # white color is transparent
add_state('text', 1 << 18)                  # used for rendering text
add_state('opaque_texture', 1 << 19)        # opaque texture
add_state('opaque_color', 1 << 20)          # opaque color
