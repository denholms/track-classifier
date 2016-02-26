#!/usr/bin/env python2

import sys, os
import pylast
import re

# Config file format:
#################################################
#   api-key=XXXXXXXXXXXXXXXXXXXXXXXXXXX
#   api-secret=XXXXXXXXXXXXXXXXXXXXXXXXXXX
#################################################
CONFIG_FILE = "./lastfm_config"
SEED_USERS_FILE = "./seed_users.txt"
SAVED_USERS_FILE = "./users.txt"

# How many levels of friends to recurse down
LEVELS = 2

def main():
    network = load_network(CONFIG_FILE)
    if network == None:
        sys.exit(1)

    new_usernames = []
    if os.path.exists(SAVED_USERS_FILE):
        new_usernames = load_saved_usernames(SAVED_USERS_FILE)

    # Fallback: start with seed usernames
    if len(new_usernames) < 1:
        new_usernames = load_seed_usernames(SEED_USERS_FILE)

    if len(new_usernames) < 1:
        print "Usernames could be loaded"
        sys.exit(1)

    processed = []
    for i in range(LEVELS):
        print "==> Processing level" , i
        usernames = [username for username in new_usernames if username not in processed]
        # Remove duplicates
        usernames = list(set(usernames))

        new_usernames = []

        for username in usernames:
            print "-> Getting friends for:" , username
            friends = process_user(network, username)
            new_usernames.extend(friends)
            print "-> Saving friends for:" , username
            save_usernames(SAVED_USERS_FILE, friends)
            processed.append(username)

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

def save_usernames(filename, usernames):
    with open(filename, 'a') as f:
        for username in usernames:
            f.write(username)
            f.write('\n')

def process_user(network, username):
    friendnames = []
    user = pylast.User(username, network=network)
    if user:
        try:
            for friend in user.get_friends():
                friendnames.append(friend.get_name())
        except Exception:
            pass

    return friendnames

if __name__ == "__main__":
    main()
