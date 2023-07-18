from museums.settings import (
    BRIGHT_DATA_ENABLED,
    BRIGHT_DATA_ZONE_USERNAME,
    BRIGHT_DATA_ZONE_PASSWORD,
)

from w3lib.http import basic_auth_header

import random


class BrightDataDownloaderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def process_request(self, request, spider):
        if not BRIGHT_DATA_ENABLED:
            return None

        request.meta["proxy"] = "http://zproxy.lum-superproxy.io:22225"

        username = BRIGHT_DATA_ZONE_USERNAME + "-session-" + str(random.random())

        request.headers["Proxy-Authorization"] = basic_auth_header(
            username, BRIGHT_DATA_ZONE_PASSWORD
        )