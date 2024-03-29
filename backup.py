#!/usr/bin/env python3

import io
import os
import sys
import glob
import json
import subprocess as sp
from os import path

import youtube_dl

HELP = f'''USAGE: {sys.argv[0]} [OPTIONS] [<PLAYLIST>]

OPTIONS:
    -d       download audio
    -u       update all playlists
    --no-git do not pull / commit / push

EXAMPLE: {sys.argv[0]} https://www.youtube.com/playlist?list=PLYhpjQWFnzXX360eOz0n7yvvURf8UHqtx
'''

YTDL_OPTIONS_PLAYLIST = ['--flat-playlist', '-J']
YTDL_OPTIONS_DOWNLOAD = [
    '-i',
    '-x',
    '--audio-format', 'opus',
    '--audio-quality', '0',
    # todo: thumbnail
    '-o', path.join(
        'playlists',
        '%(playlist)s - %(playlist_id)s',
        '%(title)s - %(id)s.%(ext)s'
    )
]


def ytdl(options):
    try:
        youtube_dl.main(options)
    except SystemExit as e:  # yt.main calls sys.exit
        if e.code != 0:
            raise e


def pull():
    p = sp.run(['git', 'pull'], stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
    if p.returncode != 0:
        print('git pull returned with an error', file=sys.stderr)
        exit(1)


def push():
    sp.run(['git', 'add', '.'], stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
    sp.run(['git', 'commit', '-m', 'PLAYLIST UPDATE'], stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
    sp.run(['git', 'push'], stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)


def backup(playlist, download=False, no_git=False):
    if not no_git:
        pull()

    options = YTDL_OPTIONS_PLAYLIST[:]
    options.append(playlist)
    sys.stdout = stdout_buf = io.StringIO()
    ytdl(options)
    sys.stdout = sys.__stdout__

    info = json.loads(stdout_buf.getvalue())
    playlist_dir = path.join('playlists', f'{info["title"]} - {info["id"]}')
    os.makedirs(playlist_dir, exist_ok=True)
    with open(path.join(f'{playlist_dir}', 'playlist.jsonl'), 'w') as f:
        jsonl = '\n'.join([json.dumps(entry) for entry in info["entries"]])
        f.write(jsonl)

    if download:
        options = YTDL_OPTIONS_DOWNLOAD[:]
        options.append('--download-archive')
        options.append(path.join(f'{playlist_dir}', '.archive'))
        options.append(playlist)
        ytdl(options)

    if not no_git:
        push()

    print(f'{info["title"]} backup done')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(HELP)
        exit(1)

    download = '-d' in sys.argv
    update = '-u' in sys.argv
    no_git = '--no-git' in sys.argv
    playlist = sys.argv[-1] if 'youtube.com' in sys.argv[-1] else None

    if update and playlist is None:
        playlists = [f.split(' - ')[-1] for f in glob.glob(path.join('playlists', '*'))]
        for playlist in playlists:
            backup(playlist, download, no_git)
    else:
        backup(playlist, download, no_git)
