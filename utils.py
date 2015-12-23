
import json
import functools
import os
import os.path


def store_as_json(dct, file_name):
    f = open(file_name, 'w')
    json.dump(dct, f)


def load_from_json(file_name):
    f = open(file_name, 'r')
    return json.load(f)


def text_hash(text):
    def churn(b, c):
        return b * 31 + ord(c)
    return functools.reduce(churn, text, 29)


def randint():
    return int.from_bytes(os.urandom(20), byteorder="big")


def tidy_names(path,
               directory_name_transformer=None,
               file_name_transformer=None):
    """Tidy names in the whole directory tree starting from 'path'
    """

    p = os.path.expanduser(path)
    for x in os.listdir(p):
        full_name = os.path.join(p, x)
        if os.path.isdir(full_name):
            tidy_names(full_name,
                       directory_name_transformer,
                       file_name_transformer)

            if directory_name_transformer:
                s = directory_name_transformer(x)
                new_name = os.path.join(p, s)
                os.replace(full_name, new_name)

        if os.path.isfile(full_name) and file_name_transformer:
            s = file_name_transformer(x)
            new_name = os.path.join(p, s)
            os.replace(full_name, new_name)


def all_files(path):
    "all files in the directory structure starting from 'path'"
    p = os.path.expanduser(path)

    def to_list(f):
        subpath = os.path.join(p, f)
        if os.path.isdir(subpath):
            return all_files(subpath)
        elif os.path.isfile(subpath):
            return [subpath]
        else:
            return []

    return (f for x in os.listdir(p) for f in to_list(x))
