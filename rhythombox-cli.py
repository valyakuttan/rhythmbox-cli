#!/usr/bin/env python3

import time
import fnmatch
import itertools
import subprocess

import utils


def play():
    return rhythmbox('--play')


def pause():
    return rhythmbox('--pause')


def addtracks(tracks):
    return rhythmbox('--enqueue', tracks)


def rhythmbox(option, files=None):
    program = "rhythmbox-client"
    files = map(str, files) if files else []
    cmd = [program, option] + list(files)
    subprocess.call(cmd)
    return cmd


def music_files(path):

    def is_music_file(path):
        mp3 = "*.[Mm][Pp]3"
        return fnmatch.fnmatch(path, mp3)

    return filter(is_music_file, utils.all_files(path))


def write_tracks(tracks):
    f = open('current.txt', 'w')
    contents = '\n'.join(tracks) + '\n'
    f.write(contents)


def main():
    music_path = "~/Music"
    n = 1934
    max_records = 5
    m = 4 + utils.randint() % max_records
    rands = [utils.randint() % n for _ in range(m)]

    xs = music_files(music_path)
    count = max(rands) + 1
    files = list(itertools.islice(xs, 0, count))
    tracks = sorted(files[i] for i in set(rands))

    addtracks(tracks)
    time.sleep(5)
    play()
    time.sleep(5)
    write_tracks(tracks)

if __name__ == "__main__":
    main()
