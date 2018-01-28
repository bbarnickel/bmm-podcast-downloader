import logging
import http.client as hc

from bmmapi import MinimalBmmApi
from watcher import PodcastWatcher


def toggle_debug_log():
    hc.HTTPConnection.debuglevel = 1
    hc.HTTPSConnection.debuglevel = 1

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True


def main():
    api = MinimalBmmApi('https://<api-address>')
    api.authenticate('<username>', '<password>')
    # print('Token:', api.token)

    watcher = PodcastWatcher(api, '<path-to-target-directory>')
    watcher.checkPodcastTracks(1, ['de', 'nb'])  # checks german and norwegian


if __name__ == "__main__":
    # toggle_debug_log()
    main()
