# -*- coding: utf-8 -*-
# Contains implementation of Wavefront .OBJ importer
# Copyright (c) 2014 Tomasz Kapuściński

import re

import modelformats
import geometry


class ObjFormat(modelformats.ModelFormat):
    description: str = 'Wavefront .OBJ format'

    def get_extension(self) -> str:
        return 'obj'

    def read(self, filename: str, model: geometry.Model, params: dict[str, str]) -> bool:
        # lists with parsed vertex attributes
        vertex_coords: list[geometry.VertexCoord] = []
        tex_coords: list[geometry.TexCoord] = []
        normals: list[geometry.Normal] = []
        materials: list[geometry.Material] = {}

        # read file
        input_file = open(filename, 'r')

        flipX = 1.0
        flipY = 1.0
        flipZ = 1.0

        if modelformats.get_param(params, 'flipX') is not None:
            flipX = -1.0

        if modelformats.get_param(params, 'flipY') is not None:
            flipY = -1.0

        if modelformats.get_param(params, 'flipZ') is not None:
            flipZ = -1.0

        flipOrder = (flipX * flipY * flipZ) < 0

        # parse lines
        while True:
            line = input_file.readline()

            if len(line) == 0:
                break

            if line[len(line)-1] == '\n':
                line = line[:len(line)-1]

            parts = line.split(' ')

            if parts[0] == 'mtllib':
                name = parts[1]
                materials = read_mtl_file(name)
            elif parts[0] == 'v':
                vertex_coords.append(geometry.VertexCoord(flipX * float(parts[1]), flipY * float(parts[2]), flipZ * float(parts[3])))
            elif parts[0] == 'vt':
                tex_coords.append(geometry.TexCoord(float(parts[1]), 1 - float(parts[2])))
            elif parts[0] == 'vn':
                normals.append(geometry.Normal(flipX * float(parts[1]), flipY * float(parts[2]), flipZ * float(parts[3])))
            elif parts[0] == 'usemtl':
                current_material = materials[parts[1]]
            elif parts[0] == 'f':
                polygon = []

                # parse vertices
                for i in range(1, len(parts)):
                    elements = parts[i].split('/')

                    vert_coord = vertex_coords[int(elements[0]) - 1]
                    normal = normals[int(elements[2]) - 1]

                    if elements[1] == '':
                        tex_coord = geometry.TexCoord(0.0, 0.0)
                    else:
                        tex_coord = tex_coords[int(elements[1]) - 1]

                    polygon.append(geometry.Vertex(
                        vert_coord, normal, tex_coord))

                # triangulate polygon
                new_triangles = geometry.triangulate(polygon, flipOrder)

                # save vertices
                for triangle in new_triangles:
                    triangle.material = current_material
                    model.triangles.append(triangle)

        input_file.close()

        return True

    def write(self, filename: str, model: geometry.Model, params: dict[str, str]) -> bool:
        model_file = open(filename, 'w')
        materials_filename = filename

        if materials_filename.find('.obj'):
            materials_filename = materials_filename.replace('.obj', '.mtl')

        materials_file = open(materials_filename, 'w')

        materials: list[geometry.Material] = []
        vertex_coords: list[geometry.VertexCoord] = []
        tex_coords: list[geometry.TexCoord] = []
        normals: list[geometry.Normal] = []

        faces: list[list[int, str]] = []

        flipX = 1.0
        flipY = 1.0
        flipZ = 1.0

        if modelformats.get_param(params, 'flipX') is not None:
            flipX = -1.0

        if modelformats.get_param(params, 'flipY') is not None:
            flipY = -1.0

        if modelformats.get_param(params, 'flipZ') is not None:
            flipZ = -1.0

        flipOrder = (flipX * flipY * flipZ) < 0

        materials_file.write('# Materials\n')

        for triangle in model.triangles:
            mat = triangle.material

            if triangle.material not in materials:
                materials.append(mat)

                name = 'Material_{}_[{}]'.format(len(materials), geometry.decode_state(mat.state))

                mat.name = name
                materials_file.write('\n')
                materials_file.write('newmtl {}\n'.format(name))

                if mat.texture1 != '':
                    materials_file.write('map_Kd {}\n'.format(mat.texture1))

                materials_file.write('Ns 96.078431\n')
                materials_file.write('Ka {} {} {}\n'.format(
                    mat.ambient[0], mat.ambient[1], mat.ambient[2]))
                materials_file.write('Kd {} {} {}\n'.format(
                    mat.diffuse[0], mat.diffuse[1], mat.diffuse[2]))
                materials_file.write('Ks {} {} {}\n'.format(
                    mat.specular[0], mat.specular[1], mat.specular[2]))
                materials_file.write('Ni 1.000000\n')
                materials_file.write('d 1.000000\n')
                materials_file.write('illum 2\n')
            else:
                for mater in materials:
                    if mat == mater:
                        mat = mater

            face: list[list[int, str]] = []

            for vertex in triangle.vertices:
                vertex_coord = geometry.VertexCoord(
                    vertex.x, vertex.y, vertex.z)
                tex_coord = geometry.TexCoord(vertex.u1, vertex.v1)
                normal = geometry.Normal(vertex.nx, vertex.ny, vertex.nz)

                # looking for vertex coordinate
                vertex_coord_index = -1

                for i in range(len(vertex_coords)):
                    if vertex_coord == vertex_coords[i]:
                        vertex_coord_index = i

                if vertex_coord_index == -1:
                    vertex_coord_index = len(vertex_coords)
                    vertex_coords.append(vertex_coord)

                # looking for texture coordinate
                tex_coord_index = -1

                for i in range(len(tex_coords)):
                    if tex_coord == tex_coords[i]:
                        tex_coord_index = i

                if tex_coord_index == -1:
                    tex_coord_index = len(tex_coords)
                    tex_coords.append(tex_coord)

                # looking for normal
                normal_index = -1

                for i in range(len(normals)):
                    if normal == normals[i]:
                        normal_index = i

                if normal_index == -1:
                    normal_index = len(normals)
                    normals.append(normal)

                for mat in materials:
                    if mat == triangle.material:
                        mat_name = mat.name

                vertex_indices = [vertex_coord_index + 1,
                                  tex_coord_index + 1, normal_index + 1, mat_name]

                face.append(vertex_indices)

            faces.append(face)

        # write vertex coordinates
        model_file.write('mtllib {}\n'.format(materials_filename))

        for v in vertex_coords:
            model_file.write('v {} {} {}\n'.format(flipX * v.x, flipY * v.y, flipZ * v.z))

        for t in tex_coords:
            model_file.write('vt {} {}\n'.format(t.u, t.v))

        for n in normals:
            model_file.write('vn {} {} {}\n'.format(flipX * n.x, flipY * n.y, flipZ * n.z))

        mat_name = ''

        model_file.write('s off\n')

        # write faces
        for f in faces:
            name = f[0][3]

            if name != mat_name:
                model_file.write('usemtl {}\n'.format(name))
                mat_name = name

            model_file.write('f')

            if flipOrder:
                model_file.write(' {}/{}/{}'.format(f[0][0], f[0][1], f[0][2]))
                model_file.write(' {}/{}/{}'.format(f[2][0], f[2][1], f[2][2]))
                model_file.write(' {}/{}/{}'.format(f[1][0], f[1][1], f[1][2]))
            else:
                for v in f:
                    model_file.write(' {}/{}/{}'.format(v[0], v[1], v[2]))

            model_file.write('\n')

        model_file.close()
        materials_file.close()

        return True


# state regex pattern
state_pattern = re.compile(r'^.+(\[(.+?)\])$')


# reads Wavefront .MTL material file
def read_mtl_file(filename: str) -> list[geometry.Material]:
    materials: list[geometry.Material] = {}

    input_file = open(filename, 'r')

    while True:
        line = input_file.readline()

        if len(line) == 0:
            break

        if line[len(line)-1] == '\n':
            line = line[:len(line)-1]

        parts = line.split(' ')

        if parts[0] == 'newmtl':
            current_material = geometry.Material()

            match = state_pattern.match(parts[1])

            if match is not None:
                current_material.state = geometry.encode_state(match.group(2))

            materials[parts[1]] = current_material
        elif parts[0] == 'Ka':
            for i in range(3):
                current_material.ambient[i] = float(parts[i+1])
        elif parts[0] == 'Kd':
            for i in range(3):
                current_material.diffuse[i] = float(parts[i+1])
        elif parts[0] == 'Ks':
            for i in range(3):
                current_material.specular[i] = float(parts[i+1])
        elif parts[0] == 'map_Kd':
            current_material.texture1 = parts[1]

    input_file.close()

    return materials


modelformats.register_format('obj', ObjFormat())
modelformats.register_extension('obj', 'obj')