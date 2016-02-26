#!/usr/bin/env python2

import sys, os
import re
import json
import pylast

# Config file format:
#################################################
#   api-key=XXXXXXXXXXXXXXXXXXXXXXXXXXX
#   api-secret=XXXXXXXXXXXXXXXXXXXXXXXXXXX
#################################################
CONFIG_FILE = "./lastfm_config"
SEED_USERS_FILE = "./seed_users.txt"
USERS_FILE = "./users_sanitized.txt"
PROCESSED_USERS_FILE = "./users_processed.txt"
SAVED_TRACKS_FILE = "./tracks.json"

TRACK_LIMIT = 5
TAG_LIMIT = 5

TITLE_KEY = "title"
ARTIST_KEY = "artist"
TAGS_KEY = "tags"

def main():
    network = load_network(CONFIG_FILE)
    if network == None:
        sys.exit(1)

    usernames = []
    if os.path.exists(USERS_FILE):
        usernames = load_saved_usernames(USERS_FILE)

    # Fallback: start with seed usernames
    if len(usernames) < 1:
        usernames = load_seed_usernames(SEED_USERS_FILE)

    if len(usernames) < 1:
        print "Usernames could be loaded"
        sys.exit(1)

    n_usernames = len(usernames)
    processed_tracks = []

    processed_users = []
    start_index = 0
    if os.path.exists(PROCESSED_USERS_FILE):
        processed_users = load_saved_usernames(PROCESSED_USERS_FILE)
        start_index = len(processed_users)

    for i in range(start_index, n_usernames):
        username = usernames[i]
        print "-> (%d/%d) Processing tracks for: %s" % (i+1, n_usernames, username)
        tracks = [track for track in get_user_tracks(network, username) if track not in processed_tracks]
        # Remove duplicates
        tracks = list(set(tracks))

        track_infos = []

        for track in tracks:
            title, artist_name, tags = process_track(track)
            track_infos.append({ TITLE_KEY : title, ARTIST_KEY : artist_name, TAGS_KEY : tags})
            processed_tracks.append(track)

        save_trackinfos(SAVED_TRACKS_FILE, track_infos)
        processed_users.append(username)
        save_processed_user(PROCESSED_USERS_FILE, username)

def load_network(config_file):
    api_key, api_secret = load_config(config_file)

    if not api_key or not api_secret:
        return None

    return pylast.LastFMNetwork(api_key=api_key, api_secret=api_secret)
        
def load_config(config_file):
    api_key = None
    api_secret = None

    api_key_match = re.compile(r'api-key\s*=\s*(.+)')
    api_secret_match = re.compile(r'api-secret\s*=\s*(.+)')

    with open(config_file, 'r') as f:
        for line in f:
            result = api_key_match.search(line)
            if result:
                api_key = result.group(1)
                continue
            result = api_secret_match.search(line)
            if result:
                api_secret = result.group(1)
                continue

    return (api_key, api_secret)

def load_seed_usernames(filename):
    usernames = []

    user_profile_match = re.compile(r'http://www.last.fm/user/(.*)')

    with open(filename, 'r') as f:
        for line in f:
            result = user_profile_match.search(line.rstrip())
            if result:
                usernames.append(result.group(1))

    return usernames

def load_saved_usernames(filename):
    usernames = []

    with open(filename, 'r') as f:
        for line in f:
            usernames.append(line.rstrip())

    return usernames

def save_trackinfos(filename, track_infos):
    with open(filename, 'a') as f:
        for track_info in track_infos:
            f.write("%s\n" % (json.dumps(track_info)))

def save_processed_user(filename, username):
    with open(filename, 'a') as f:
        f.write("%s\n" % (username))

def get_user_tracks(network, username):
    tracks = []
    user = pylast.User(username, network=network)
    if user:
        try:
            for track in user.get_top_tracks(limit=TRACK_LIMIT):
                tracks.append(track.item)
        except Exception:
            pass

    return tracks

def process_track(track):
    title = ""
    artist_name = ""
    tag_names = []

    try:
        title = track.get_name()
        artist = track.get_artist()
        if artist:
            artist_name = artist.get_name()

        top_tags = track.get_top_tags(limit=TAG_LIMIT)
        tag_names = map(lambda top_tag: top_tag.item.get_name(), top_tags)
    except Exception:
        title = ""
        artist = ""
        tag_names = []

    return (title, artist_name, tag_names)

if __name__ == "__main__":
    main()
