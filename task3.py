from math import log
from zipfile import ZipFile
from collections import namedtuple

from task2 import logger

file_record = namedtuple('FileRecord', ['name', 'size'])


@logger()
def size_str(size_in_bytes):
    if size_in_bytes > 0:
        size = {0: 'B', 1: 'KB', 2: 'MB', 3: 'GB'}
        extent = min(int(log(size_in_bytes, 1024)), 3)
        return f'{round(size_in_bytes / 1024 ** extent)} {size[extent]}'
    else:
        return '0 B'


@logger()
def is_in_collection(folder, source):
    for r in source:
        if isinstance(r, dict):
            if folder in r:
                return r
    return None


@logger()
def print_structure(files_dict, indent=4, level=0):
    for a in files_dict:
        if isinstance(a, dict):
            print(f'{" "*indent*level}{list(a.keys())[0]}:')
            print_structure(list(a.values()), indent, level+1)
        elif isinstance(a, list):
            print_structure(a, indent, level)
        elif isinstance(a, file_record):
            print(f'{" "*indent*level}{a.name} - {a.size}')


@logger()
def get_file_structure_of_zip(archive_name):
    result = []
    with ZipFile(archive_name) as zip:
        for a in zip.filelist:
            path = a.filename.split('/')
            current = result
            for folder in path[:-1]:
                element = is_in_collection(folder, current)
                if element is None:
                    element = {folder: []}
                    current.append(element)
                current = element[folder]
            if not a.is_dir():
                current.append(file_record(path[-1], size_str(a.file_size)))
    return result


if __name__ == '__main__':

    zipfile_structure = get_file_structure_of_zip('data.zip')
    print_structure(zipfile_structure, indent=2)
