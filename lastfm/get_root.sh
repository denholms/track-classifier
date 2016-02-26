#!/bin/bash

OUTPUT_FILE="seed_users.txt"

scrapy runspider spider.py 2>&1 | grep -e "last.fm/user" | sort -u > "$OUTPUT_FILE"
