# -*- coding: utf-8 -*-
# Implements Colobot model formats
# Copyright (c) 2014 Tomasz Kapuściński

import geometry
import modelformats


class ColobotNewTextFormat(modelformats.ModelFormat):
    description: str = 'Colobot New Text format'
    ext: str = 'txt'

    def read(self, filename: str, model: geometry.Model, params: dict[str, str]) -> bool:
        input_file = open(filename, 'r', encoding='utf8')

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
                triangle.material.texture1 = values[1]
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
        output_file = open(filename, 'w', encoding='utf8')

        version = 2

        if 'version' in params:
            version = int(params['version'])

        # write header
        output_file.write('# Colobot text model\n'
                          '\n'
                          '### HEAD\n'
                          'version %s\n'
                          'total_triangles %d\n'
                          '\n'
                          '### TRIANGLES\n'
                          % (version, len(model.triangles)))

        # write triangles
        for triangle in model.triangles:
            # write vertices
            for i in range(3):
                vertex = triangle.vertices[i]
                output_file.write(
                    'p%d c %f %f %f'
                    ' n %f %f %f'
                    ' t1 %f %f'
                    ' t2 %f %f\n'
                    % (i+1, vertex.x, vertex.y, vertex.z,
                       vertex.nx, vertex.ny, vertex.nz,
                       vertex.u1, vertex.v1,
                       vertex.u2, vertex.v2))

            mat = triangle.material

            dirt = 'N'
            dirt_texture = ''

            if 'dirt' in params:
                dirt = 'Y'
                dirt_texture = params['dirt']

            output_file.write(
                'mat dif %f %f %f %f'
                ' amb %f %f %f %f'
                ' spc %f %f %f %f\n'
                'tex1 %s\n'
                'tex2 %s\n'
                'var_tex2 %c\n'
                % (*mat.diffuse, *mat.ambient, *mat.specular,
                    mat.texture1, mat.texture2, dirt))

            if version == 1:
                output_file.write('lod_level 0\n')

            output_file.write('state %d\n\n' % mat.state)

        output_file.close()

        return True


modelformats.register_format('new_txt', ColobotNewTextFormat())

modelformats.register_extension('txt', 'new_txt')
