# -*- coding: utf-8 -*-
# Model format base implementation
# Copyright (c) 2014 Tomasz Kapuściński

import geometry

formats: dict[str, 'ModelFormat'] = {}
extensions: dict[str, str] = {}


# base class for formats
class ModelFormat:
    description: str

    def get_extension(self) -> str:
        return None

    def read(self, filename: str, model: geometry.Model, params: dict[str, str]) -> bool:
        print('Reading not implemented')
        return False

    def write(self, filename: str, model: geometry.Model, params: dict[str, str]) -> bool:
        print('Writing not implemented')
        return False

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


# registers format
def register_format(name: str, fmt: ModelFormat) -> None:
    formats[name] = fmt

# registers filename extension that translates to given format


def register_extension(ext: str, name: str) -> None:
    extensions[ext] = name


def get_format(name: str) -> ModelFormat:
    if name in formats:
        return formats[name]
    else:
        return None


def get_format_by_extension(extension: str) -> ModelFormat:
    if extension is None:
        return None

    if extension in extensions:
        return formats[extensions[extension]]


def get_extension(filename: str) -> str:
    if '.' in filename:
        parts = filename.split('.')
        return parts[len(parts)-1]
    else:
        return None


def read(fmt: str, filename: str, model: geometry.Model, params: dict[str, str]) -> bool:
    model_format: ModelFormat = get_format(fmt)

    if model_format is None:
        print('Unknown format: ' + fmt)
        return False
    else:
        return model_format.read(filename, model, params)


def write(fmt: str, filename: str, model: geometry.Model, params: dict[str, str]) -> bool:
    model_format = get_format(fmt)

    if model_format is None:
        print('Unknown format: ' + fmt)
        return False

    return model_format.write(filename, model, params)


def convert(in_format: str, in_filename: str, in_params: dict[str, str], out_format: str, out_filename: str, out_params: dict[str, str]) -> bool:
    if in_filename is None:
        print('Input file not specified.')
        return False

    if out_filename is None:
        print('Output file not specified.')
        return False

    if 'directory' in in_params:
        in_filename = in_params['directory'] + '/' + in_filename

    if 'directory' in out_params:
        out_filename = out_params['directory'] + '/' + out_filename

    model = geometry.Model()

    completed = read(in_format, in_filename, model, in_params)
    if not completed:
        return

    completed = write(out_format, out_filename, model, out_params)
    if not completed:
        return

    print(f'{in_filename} -> {out_filename}')


def convert_list(file_list: list[str], in_format: str, in_params: dict[str, str], out_format: str, out_params: dict[str, ]) -> None:
    in_filename = ''
    out_filename = ''

    in_modelformat = get_format(in_format)
    out_modelformat = get_format(out_format)

    if in_modelformat is None:
        print('Unknown input format: ' + in_format)
        return

    if out_modelformat is None:
        print('Unknown output format: ' + out_format)
        return

    in_directory = ''
    if 'directory' in in_params:
        in_directory = in_params['directory'] + '/'

    out_directory = ''
    if 'directory' in out_params:
        out_directory = out_params['directory'] + '/'

    for pair in file_list:
        # parse input string
        if ':' in pair:
            parts = pair.split(':')
            in_filename = parts[0]
            out_filename = parts[1]
        else:
            index = pair.rfind('.')

            if index == -1:
                filename_part = pair
            else:
                filename_part = pair[:index]

            extension = out_modelformat.get_extension()

            if extension is None:
                print(f'Cannot convert file {pair}, unknown output format.')
                continue

            in_filename = pair
            out_filename = filename_part + '.' + extension

        # append directory path
        in_filename = in_directory + in_filename
        out_filename = out_directory + out_filename

        # convert format
        model = geometry.Model()

        in_modelformat.read(in_filename, model, in_params)
        out_modelformat.write(out_filename, model, out_params)

        print('{in_filename} -> {out_filename}')

    if len(file_list) == 0:
        print('Batch list empty. No files converted.')


def print_formats():
    for format in formats.keys():
        print('{:<16}{}'.format(format, formats[format].description))


def print_extensions():
    for ext in extensions.keys():
        format = extensions[ext]
        desc = formats[format].description

        print('{:<8}{}'.format(ext, desc))


# returns parameter value
def get_param(params: dict[str, str], name: str, default: str = None) -> str:
    if name in params:
        return params[name]
    else:
        return default


register_format('default', DefaultModelFormat())
