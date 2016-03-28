#!/usr/bin/env python2

import sys, os
import re
import json

import pyechonest
import pyechonest.song as echo_song
from pyechonest import config

# Config file format:
#################################################
#   api-key=XXXXXXXXXXXXXXXXXXXXXXXXXXX
#################################################
CONFIG_FILE="./echonest_config"
TRACKS_FILE="./tracks.json"
PROCESSED_TRACKS_FILE="./tracks_processed.json"

ARTIST_KEY="artist"
TITLE_KEY="title"
TAGS_KEY="tags"

LIMIT=20

def main():
    api_key = load_config(CONFIG_FILE)
    if not api_key:
        print "Failed to load config"
        sys.exit(1)

    config.ECHO_NEST_API_KEY=api_key

    tracks = load_tracks(TRACKS_FILE)

    n_tracks = len(tracks)
    if n_tracks < 1:
        print "No tracks loaded"
        sys.exit(1)

    processed_tracks = []
    start_index = 0
    if os.path.exists(PROCESSED_TRACKS_FILE):
        processed_tracks = load_tracks(PROCESSED_TRACKS_FILE)
        start_index = len(processed_tracks)

    print "==> Number of tracks:" , n_tracks
    print "==> Number of pre-processed tracks:" , start_index

    for i in range(start_index, n_tracks):
        if i > start_index+LIMIT:
            break

        track = tracks[i]
        print "-> (%d/%d) Processing %s - %s" % (i, n_tracks, track.get(ARTIST_KEY), track.get(TITLE_KEY))

        try:
            results = echo_song.search(artist=track.get(ARTIST_KEY), title=track.get(TITLE_KEY), buckets=['audio_summary'], results=1)
            if not results:
                print "No results found for %s - %s" % (track.get(ARTIST_KEY), track.get(TITLE_KEY))
                continue

            for song in results:
                if song.audio_summary:
                    # Save audio_summary with track in a new file, as a json object
                    track.update(song.audio_summary)
                    save_track(PROCESSED_TRACKS_FILE, track)

        except Exception:
            print "Echo Nest API error, exiting..."
            sys.exit(1)

def load_config(config_file):
    api_key = None

    api_key_match = re.compile(r'api-key\s*=\s*(.+)')

    with open(config_file, 'r') as f:
        for line in f:
            result = api_key_match.search(line)
            if result:
                api_key = result.group(1)
                continue

    return api_key

def load_tracks(filename):
    tracks = []
    with open(filename, 'r') as f:
        for line in f:
            try:
                track = json.loads(line)
                if track:
                    tracks.append(track)
            except Exception:
                pass

    return tracks

def save_track(filename, track):
    with open(filename, 'a') as f:
        f.write("%s\n" % (json.dumps(track)))

if __name__ == "__main__":
    main()
