# YouTube Playlist Backup

This Python script uses [youtube-dl](https://github.com/ytdl-org/youtube-dl) to store all changes of a YouTube playlist in git.  
The main purpose is that you know which videos are affected if they become _unavailable_.

Optionally, it can download the audio media. These files are for obvious reasons not tracked in git.

## Installation

- Fork this repository and clone the forked repo to your machine.
- `pip install -r requirements.txt`
- `./backup.py`

## Auto Update with GitHub Actions
![auto update](../../workflows/Playlist%20Update/badge.svg)

You can use the configured GitHub Action to update your tracked playlists weekly.
