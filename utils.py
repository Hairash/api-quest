from random import randint, shuffle
from const import file_names, extensions


def generate_file_list(num, extra=[]):
    file_list = extra
    for _ in range(num):
        file_name_idx = randint(0, len(file_names) - 1)
        file_name = file_names[file_name_idx]
        extension_idx = randint(0, len(extensions) - 1)
        extension = extensions[extension_idx]
        file_list.append(f'{file_name}.{extension}')
    shuffle(file_list)
    return file_list
