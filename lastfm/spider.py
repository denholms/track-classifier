#!/usr/bin/env python2

from scrapy.spiders import Spider
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
import re

DOMAIN = "web.archive.org"
URL = "https://%s/%s" % (DOMAIN, "web/20150512025123/http://www.last.fm/community/users/active")

USERS_FILE = "users.txt"

class LastFMSpider(Spider):
    name = DOMAIN
    allowed_domains = [DOMAIN]
    start_urls = [
        URL
    ]
    download_delay = 0.25 # 250ms of delay
#    download_delay = 2.5 # 2.5s of delay

    def parse(self, response):
        le = LinkExtractor()
        user_profiles = []
        for link in le.extract_links(response):
            result = re.search(r'.*(http://www.last.fm/user/.*)', link.url)
            if result:
                user_profiles.append(result.group(1))

        for user_profile in user_profiles:
            print user_profile
