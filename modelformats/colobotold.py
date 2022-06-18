import struct

import geometry
from modelformats import ModelFormat, register_format, register_extension

class ColobotOldFormat(ModelFormat):
    description: str = 'Colobot Old Binary format'

    def get_extension(self):
        return 'mod'

    def read(self, filename, model, params):
        input_file = open(filename, 'rb', encoding='utf8')

        # read header
        version_major = struct.unpack('=i', input_file.read(4))[0]
        version_minor = struct.unpack('=i', input_file.read(4))[0]

        triangle_count = struct.unpack('=i', input_file.read(4))[0]

        if version_major != 1 or version_minor != 2:
            print(f'Unsupported format version: {version_major}.{version_minor}')
            return False

        # read and ignore padding
        input_file.read(40)

        materials = []

        for index in range(triangle_count):
            triangle = geometry.Triangle()

            # used, selected, 2 byte padding
            input_file.read(4)

            for vertex in triangle.vertices:
                # position, normal, uvs
                floats = struct.unpack('=ffffffffff', input_file.read(40))

                vertex.x = floats[0]
                vertex.y = floats[1]
                vertex.z = floats[2]

                vertex.nx = floats[3]
                vertex.ny = floats[4]
                vertex.nz = floats[5]

                vertex.u1 = floats[6]
                vertex.v1 = floats[7]

                vertex.u2 = floats[8]
                vertex.v2 = floats[9]

            # material colors
            floats = struct.unpack('=fffffffffffffffff',
                                   input_file.read(17 * 4))

            mat = triangle.material

            for i in range(4):
                mat.diffuse[i] = floats[0 + i]
                mat.ambient[i] = floats[4 + i]
                mat.specular[i] = floats[8 + i]

            # texture name
            chars = input_file.read(20)

            for i in range(20):
                if chars[i] == '\0':
                    mat.texture1 = struct.unpack(f'={i}s', chars[:i])[0]
                    break

            values = struct.unpack('=ffiHHHH', input_file.read(20))

            mat.state = values[2]
            dirt = values[3]

            if dirt != 0:
                mat.texture2 = f'dirty{dirt:02d}.png'

            # optimizing materials
            replaced = False

            for material in materials:
                if mat == material:
                    triangle.material = material
                    replaced = True
                    break

            if not replaced:
                materials.append(mat)

            model.triangles.append(triangle)
            # end of triangle

        input_file.close()

        return True

    def write(self, filename, model, params):
        output_file = open(filename, 'wb')

        # write header
        output_file.write(b'\x01\x00\x00\x00'                      # version major
                          b'\x02\x00\x00\x00')                      # version minor
        output_file.write(struct.pack('i', len(model.triangles)))   # total triangles

        # padding
        output_file.write(b'\x00' * 40)

        # triangles
        for triangle in model.triangles:
            output_file.write(b'\x01'       # used
                              b'\x00'       # selected ?
                              b'\x00\x00')   # padding (2 bytes)

            # write vertices
            for vertex in triangle.vertices:
                output_file.write(struct.pack('=fff', vertex.x, vertex.y, vertex.z))       # vertex coord
                output_file.write(struct.pack('=fff', vertex.nx, vertex.ny, vertex.nz))    # normal
                output_file.write(struct.pack('=ff', vertex.u1, vertex.v1))                # tex coord 1
                output_file.write(struct.pack('=ff', vertex.u2, vertex.v2))                # tex coord 2

            # material info
            mat = triangle.material
            output_file.write(struct.pack('=ffff', *mat.diffuse))        # diffuse color
            output_file.write(struct.pack('=ffff', *mat.ambient))        # ambient color
            output_file.write(struct.pack('=ffff', *mat.specular))       # specular color
            output_file.write(b'\x00' * 20)                              # emissive color and power

            # texture name
            output_file.write(mat.texture1.encode('utf-8'))

            # texture name padding
            output_file.write(b'\x00' * (20 - len(mat.texture1)))

            dirt = 0

            if 'dirt' in params:
                dirt = int(params['dirt'])

            output_file.write(struct.pack('=ff', 0.0, 10000.0))     # rendering range
            output_file.write(struct.pack('i', mat.state))          # state
            output_file.write(struct.pack('=H', dirt))              # dirt texture
            output_file.write(b'\x00' * 6)                          # reserved

        output_file.close()

        return True

register_format('colobot', ColobotOldFormat())
register_format('old', ColobotOldFormat())

register_extension('mod', 'old')