# -*- coding: utf-8 -*-
# Implements Colobot model formats
# Copyright (c) 2014 Tomasz Kapuściński

import geometry
import modelformats


class ColobotNewTextFormat(modelformats.ModelFormat):
    description: str

    def __init__(self):
        self.description = 'Colobot New Text format'

    def get_extension(self) -> str:
        return 'txt'

    def read(self, filename: str, model: geometry.Model, params: dict[str, str]) -> bool:
        input_file = open(filename, 'r')

        triangle = geometry.Triangle()
        materials: list[geometry.Material] = []

        while True:
            line = input_file.readline()

            # eof
            if len(line) == 0:
                break

            # comments are ignored
            if line[0] == '#':
                continue

            # remove eol
            if line[len(line)-1] == '\n':
                line = line[:len(line)-1]

            values = line.split(' ')
            cmd = values[0]

            if cmd == 'version':
                model.version = int(values[1])
            elif cmd == 'triangles':
                continue
            elif cmd == 'p1':
                triangle.vertices[0] = modelformats.parse_vertex(values)
            elif cmd == 'p2':
                triangle.vertices[1] = modelformats.parse_vertex(values)
            elif cmd == 'p3':
                triangle.vertices[2] = modelformats.parse_vertex(values)
            elif cmd == 'mat':
                triangle.material = modelformats.parse_material(values)
            elif cmd == 'tex1':
                triangle.material.texture = values[1]
            elif cmd == 'tex2':
                triangle.material.texture2 = values[1]
            elif cmd == 'var_tex2':
                continue
            elif cmd == 'lod_level':
                triangle.material.lod = int(values[1])
            elif cmd == 'state':
                triangle.material.state = int(values[1])

                mat_final: geometry.Material = None

                for mat in materials:
                    if triangle.material == mat:
                        mat_final = mat

                if mat_final is None:
                    mat_final = triangle.material
                    materials.append(mat_final)

                triangle.material = mat_final

                model.triangles.append(triangle)
                triangle = geometry.Triangle()

        input_file.close()

        return True

    def write(self, filename: str, model: geometry.Model, params: dict[str, str]) -> bool:
        output_file = open(filename, 'w')

        version = 2

        if 'version' in params:
            version = int(params['version'])

        # write header
        output_file.write('# Colobot text model\n')
        output_file.write('\n')
        output_file.write('### HEAD\n')
        output_file.write('version ' + str(version) + '\n')
        output_file.write('total_triangles ' +
                          str(len(model.triangles)) + '\n')
        output_file.write('\n')
        output_file.write('### TRIANGLES\n')

        # write triangles
        for triangle in model.triangles:
            # write vertices
            for i in range(3):
                vertex = triangle.vertices[i]
                output_file.write('p{} c {} {} {}'.format(
                    i+1, vertex.x, vertex.y, vertex.z))
                output_file.write(' n {} {} {}'.format(
                    vertex.nx, vertex.ny, vertex.nz))
                output_file.write(' t1 {} {}'.format(vertex.u1, vertex.v1))
                output_file.write(' t2 {} {}\n'.format(vertex.u2, vertex.v2))

            mat = triangle.material

            dirt = 'N'
            dirt_texture = ''

            if 'dirt' in params:
                dirt = 'Y'
                dirt_texture = params['dirt']

            output_file.write('mat dif {} {} {} {}'.format(
                mat.diffuse[0], mat.diffuse[1], mat.diffuse[2], mat.diffuse[3]))
            output_file.write(' amb {} {} {} {}'.format(
                mat.ambient[0], mat.ambient[1], mat.ambient[2], mat.ambient[3]))
            output_file.write(' spc {} {} {} {}\n'.format(
                mat.specular[0], mat.specular[1], mat.specular[2], mat.specular[3]))
            output_file.write('tex1 {}\n'.format(mat.texture))
            output_file.write('tex2 {}\n'.format(dirt_texture))
            output_file.write('var_tex2 {}\n'.format(dirt))

            if version == 1:
                output_file.write('lod_level 0\n')

            output_file.write('state ' + str(mat.state) + '\n')
            output_file.write('\n')

        output_file.close()

        return True


modelformats.register_format('new_txt', ColobotNewTextFormat())

modelformats.register_extension('txt', 'new_txt')
