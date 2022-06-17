# -*- coding: utf-8 -*-
# Implements Colobot model formats
# Copyright (c) 2014 Tomasz Kapuściński

import geometry
from modelformats.model import ModelFormat
from modelformats import get_extension, get_format_by_extension, register_format

# default model format -- chooses format based on filename extension
class DefaultModelFormat(ModelFormat):
    description: str

    def __init__(self):
        self.description = 'Default model format'

    def read(self, filename: str, model: geometry.Model, params: dict[str, str]) -> bool:
        ext = get_extension(filename)
        format = get_format_by_extension(ext)

        if format is None:
            print('Unknown default format. File ' + filename + ' cannot be processed.')
            return False

        return format.read(filename, model, params)

    def write(self, filename: str, model: geometry.Model, params: dict[str, str]) -> bool:
        ext = get_extension(filename)
        format = get_format_by_extension(ext)

        if format is None:
            print('Unknown default format. File ' + filename + ' cannot be processed.')
            return False

        return format.write(filename, model, params)


register_format('default', DefaultModelFormat())