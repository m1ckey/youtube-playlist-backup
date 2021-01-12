# YouTube Playlist Backup

This Python script uses [youtube-dl](https://github.com/ytdl-org/youtube-dl) to track all changes of a YouTube playlist in git.  
The main purpose is that you know which videos are affected if they become _unavailable_.

Optionally, it can download the audio media. These files are for obvious reasons not tracked in git.

## Installation

- [Duplicate](https://github.com/m1ckey/youtube-playlist-backup/generate) this template and clone the new repository to your machine.
- `pip install -r requirements.txt`
- `./backup.py`

## Auto Update with GitHub Actions
![auto update](../../workflows/Playlist%20Update/badge.svg)

You can use the configured GitHub Action to update your tracked playlists weekly.
