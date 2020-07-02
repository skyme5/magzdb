"""Main module."""
import os
import re

import requests


class Magzdb:
    """Magzdb Downloader."""

    def __init__(self, directory_prefix=str, editions=list, latest=bool, id=str):
        """Global options."""
        self.directory_prefix = directory_prefix or os.getcwd()
        self.editions = editions
        self.latest = latest
        self.id = id
        self.REGEX_TITLE = re.compile(
            r"""<h1><a href=/j/\d+><b>(?P<title>[^<]+)</b></a></h1>""",
            flags=re.IGNORECASE | re.MULTILINE,
        )
        self.REGEX_EDITION = re.compile(
            r"""<a\s*href="\/num\/(?P<id>\d+)"\s*title="(?P<year>\d+)\s*№[^\"]*">\s*<span\s*style="background-color:\s*[^"]*"\s*>(?P<edition>\d+)""",
            flags=re.IGNORECASE | re.MULTILINE,
        )
        self.EDITION_DOWNLOAD_PAGE = "http://magzdb.org/num/{}/dl"
        self.EDITION_DOWNLOAD_URL = "http://magzdb.org/file/{}/dl"
        self.reaponse_ok = requests.Response.ok
        self.request = requests.Session()

    def _download_file(self, url: str, dest: str):
        if not os.path.exists(os.path.dirname(dest)):
            os.makedirs(os.path.dirname(dest), exist_ok=True)

        try:
            if os.path.getsize(dest) == 0:
                os.remove(dest)
        except FileNotFoundError:
            pass

        try:
            with open(dest, "xb") as handle:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.68 Safari/537.36"
                }
                response = self.request.get(
                    url, stream=True, timeout=160, headers=headers
                )
                if response.status_code != self.reaponse_ok:
                    response.raise_for_status()

                print("Downloading to {}".format(dest))
                for data in response.iter_content(chunk_size=4194304):
                    handle.write(data)
                handle.close()
        except FileExistsError:
            pass
        except requests.exceptions.RequestException:
            print("File {} not found on Server {}".format(dest, url))
            pass

        if os.path.getsize(dest) == 0:
            os.remove(dest)

    def _html_regex(self, url, regex):
        try:
            docstring = self.request.get(url).text
            return re.search(regex, docstring)
        except re.error as e:
            print(e)
            raise Exception("REGEX URL error.")
        except requests.ConnectionError as e:
            print(e)
            raise Exception("Connection error encountered.")
        except requests.HTTPError as e:
            print(e)
            raise Exception("HTTP Error encountered.")

    def get_valid_filename(self, s):
        """
        Return the given string converted to a string that can be used for a clean
        filename. Remove leading and trailing spaces; convert other spaces to
        underscores; and remove anything that is not an alphanumeric, dash,
        underscore, or dot.
        >>> get_valid_filename("john's portrait in 2004.jpg")
        'johns_portrait_in_2004.jpg'
        """
        s = str(s).strip().replace(" ", "_")
        return re.sub(r"(?u)[^-\w.]", "", s)

    def get_editions(self) -> (str, list):
        """Get Editions for `id`."""
        try:
            docstring = self.request.get("http://magzdb.org/j/" + self.id).text
            title = re.search(self.REGEX_TITLE, docstring).group("title")
            editions = re.findall(self.REGEX_EDITION, docstring)
            return (title, editions)
        except re.error as e:
            print(e)
            raise Exception("REGEX error.")
        except requests.ConnectionError as e:
            print(e)
            raise Exception("Connection error encountered.")
        except requests.HTTPError as e:
            print(e)
            raise Exception("HTTP Error encountered.")

    def download(self):
        """Download Editions."""
        title, editions = self.get_editions()
        title = self.get_valid_filename(title)
        directory = os.path.join(self.directory_prefix, title)

        for edition in list(reversed(editions)):
            eid, _, _ = edition
            download_page_url = self.EDITION_DOWNLOAD_PAGE.format(eid)
            download_id = self._html_regex(
                download_page_url,
                r"<a\s*href\=\.\.\/file\/(?P<id>\d+)/dl>\[file\.magzdb\.org\]</a>",
            ).group("id")
            download_direct_url = self._html_regex(
                self.EDITION_DOWNLOAD_URL.format(download_id),
                r"href=\"(?P<url>http://file\.magzdb\.org/ul/[^\"]*)\"",
            ).group("url")
            filename = self.get_valid_filename(download_direct_url.split("/")[-1])
            filepath = os.path.join(directory, filename)
            self._download_file(download_direct_url, filepath)
            if self.latest:
                exit(0)
