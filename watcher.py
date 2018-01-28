import os.path
import json


class PodcastWatcher:
    def __init__(self, bmm_api, path):
        self.api = bmm_api
        self.path = path
        self.db = {}
        self._readDb()

    def _readDb(self):
        try:
            with open(os.path.join(self.path, 'database.json'), 'r') as fin:
                self.db = json.load(fin)
        except Exception:
            pass

    def _writeDb(self):
        try:
            with open(os.path.join(self.path, 'database.json'), 'w') as fout:
                json.dump(self.db, fout)
        except Exception:
            pass

    def _getDownloadFilename(self, url):
        _, part = url.rsplit('/', 1)
        if '?' in part:
            fn, _ = part.split('?', 1)
            return fn
        return part

    def _dbContains(self, pid, lang, trid, rts):
        p_db = self.db.get(pid)
        if not p_db:
            return False

        l_db = p_db.get(lang)
        if not l_db:
            return False

        for tr in l_db:
            db_id = tr.get('id')
            db_rts = tr.get('recorded_at')
            if db_id == trid and db_rts == rts:
                return True

        return False

    def _getDownloadUrl(self, track):
        media = track.get('media', [])
        for medium in media:
            type = medium.get('type')
            if type != 'audio':
                continue
            files = medium.get('files', [])
            if len(files) > 0:
                file_obj = files[0]
                return file_obj.get('url')
        return None  # vllt Fehler loggen?

    def _tryDownload(self, track):
        download_url = self._getDownloadUrl(track)
        if not download_url:
            return False

        title = track.get('title')

        filename = self._getDownloadFilename(download_url)
        target_path = os.path.join(self.path, filename)

        print("Downloading '{0}' from {1} to {2}...".format(
            title, download_url, target_path))
        self.api.download(download_url, target_path)
        print("Download complete!")

        return True

    def _updateDb(self, pid, lang, id, rts):
        if pid not in self.db:
            self.db[pid] = {}
        p_db = self.db.get(pid)

        if lang not in p_db:
            p_db[lang] = []
        l_db = p_db.get(lang)

        item = {"id": id, "recorded_at": rts}
        l_db.append(item)

    def checkPodcastTracks(self, podcast_id, languages):
        count = 0
        for language in languages:
            self.api.setLanguage(language)
            tracks = self.api.podcastTracks(podcast_id)
            print("Retrieved {0} last tracks for language '{1}' "
                  "for podcast {2}.".format(
                        len(tracks), language, podcast_id))
            pid = str(podcast_id)
            for track in tracks:
                id = track.get('id')
                rts = track.get('recorded_at')
                title = track.get('title')
                print("Checking '{0}'...".format(title))
                if not self._dbContains(pid, language, id, rts):
                    if self._tryDownload(track):
                        self._updateDb(pid, language, id, rts)
                        self._writeDb()
                        count += 1
                else:
                    print("No update needed.")

        print("Downloaded {0} files total.".format(count))
