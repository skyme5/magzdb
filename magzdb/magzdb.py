"""Main module."""
import os
import re
import subprocess

import requests
from loguru import logger

from magzdb.downloader import download_file
from magzdb.downloader import DOWNLOADER_LIST
from magzdb.downloader import external_downloader


class Magzdb:
    """Magzdb Downloader."""

    def __init__(
        self,
        directory_prefix=None,
        downloader="self",
        debug=False,
        skip_download=False,
    ):
        """Set global options.

        Args:
            directory_prefix (str): Directory prefix for downloading. Defaults to current directory.
            downloader (str): One of self, aria2, wget. Defaults to self.
            debug (bool, optional): logger.error debug information. Defaults to False.
            skip_download (bool, optional): skip downloading
        """
        self.directory_prefix = directory_prefix or os.getcwd()
        self.downloader = downloader if downloader in DOWNLOADER_LIST else "self"
        self.debug = debug
        self.skip_download = skip_download

        self.REGEX_TITLE = re.compile(
            r"""<title>(?P<title>[^|]+)\|\s+magzDB</title>""",
            flags=re.IGNORECASE | re.MULTILINE,
        )
        self.REGEX_EDITION = re.compile(
            r"""<a\s*href="\/num\/(?P<id>\d+)"\s*title="(?P<year>\d+)[^"]+"><span style="background-color""",
            flags=re.IGNORECASE | re.MULTILINE,
        )

        self.EDITION_DOWNLOAD_PAGE = "http://magzdb.org/num/{}/dl"
        self.EDITION_DOWNLOAD_URL = "http://magzdb.org/file/{}/dl"

        self.reaponse_ok = requests.Response.ok
        self.request = requests.Session()

    def _print(self, msg: str):
        """logger.error debug information."""
        if self.debug:
            logger.debug(msg)

    def _html_regex(self, url, regex):
        try:
            docstring = self.request.get(url, allow_redirects=False).text
            return [a for a in re.findall(regex, docstring) if a]
        except re.error as e:
            logger.error(e)
            raise Exception("REGEX URL error.")
        except requests.ConnectionError as e:
            logger.error(e)
            raise Exception("Connection error encountered.")
        except requests.HTTPError as e:
            logger.error(e)
            raise Exception("HTTP Error encountered.")

    def apply_filter(self, all_editions, editions, filter: str):
        """Apply filter to list of editions.

        Args:
            all_editions ([Tuple]): List of Tuples containing eid, year and issue information
            editions ([str]): List of eid
            filter (str): Filter expression
        """

        def prepare_filter(filter_str):
            """Sanitize filter expression.

            Args:
                filter_str (str): Input filter expression

            Returns:
                str: Safe filter expression
            """
            allowed_tokens = "eid year and or < <= > >= =="
            number = re.compile(r"^[-+]?([1-9]\d*|0)$")
            return " ".join(
                [
                    e
                    for e in re.split(r"\s+", filter_str.lower())
                    if e in allowed_tokens or re.match(number, e)
                ]
            )

        def eval_filter(filter_str, params):
            eid, year, *_ = params
            filter = filter_str.replace("eid", eid)
            filter = filter.replace("year", year)
            return eval(filter)

        if editions is not None and len(editions) > 0:
            return [e for e in all_editions if e[0] in editions]

        if filter is not None:
            filter = prepare_filter(filter)
            self._print("Filter prepared: `{}`".format(filter))
            return [e for e in all_editions if eval_filter(filter, e)]

        return all_editions

    def get_valid_filename(self, s):
        """Return the given string converted to a string that can be used for a clean filename.

        Remove leading and trailing spaces; convert other spaces to
        underscores; and remove anything that is not an alphanumeric, dash,
        underscore, or dot.
        >>> get_valid_filename("john's portrait in 2004.jpg")
        'johns_portrait_in_2004.jpg'
        """
        s = str(s).strip().replace(" ", "_")
        return re.sub(r"(?u)[^-\w.]", "", s)

    def get_editions(self, id: str):
        """Get title and editions for `id`.

        If list of editions is provided then returns only those.

        Args:
            id (str): Magazine ID

        Raises:
            Exception: re.error
            Exception: requests.ConnectionError
            Exception: requests.HTTPError

        Returns:
            Tuple[str, list]: Tuple of title and editions found from magzdb
        """
        try:
            docstring = self.request.get("http://magzdb.org/j/" + id).text
            title = re.search(self.REGEX_TITLE, docstring).group("title")
            editions = re.findall(self.REGEX_EDITION, docstring)

            return (title.strip(), editions)
        except re.error as e:
            logger.error(e)
            raise Exception("REGEX error.")
        except requests.ConnectionError as e:
            logger.error(e)
            raise Exception("Connection error encountered.")
        except requests.HTTPError as e:
            logger.error(e)
            raise Exception("HTTP Error encountered.")

    def download(
        self, id: str, editions=list(), latest_only=False, filter=None,
    ):
        """Download Editions."""
        title, all_editions = self.get_editions(id=id)
        title = self.get_valid_filename(title)
        directory = os.path.join(self.directory_prefix, title)

        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        selected_editions = self.apply_filter(all_editions, editions, filter)

        logger.info("Found {} editions of {}".format(len(selected_editions), title))

        if latest_only:
            selected_editions = selected_editions[-1:]

        for edition in list(reversed(selected_editions)):
            eid, year, *_ = edition

            logger.info("Downloading year {} id {}".format(year, eid))

            for dowload_id in self._html_regex(
                self.EDITION_DOWNLOAD_PAGE.format(eid),
                r"""<a\s*href\=\.\.\/file\/(?P<id>\d+)/dl>""",
            ):
                self._print("Download Link ID: {}".format(dowload_id))

                download_url_list = self._html_regex(
                    self.EDITION_DOWNLOAD_URL.format(dowload_id),
                    r'''<a href=\"(?P<url>http[^\"]*(?:\.\w+)?)"''',
                )

                if not download_url_list:
                    continue

                download_url = download_url_list[0]

                self._print("Download URL: {}".format(download_url))

                filename = self.get_valid_filename(download_url.split("/")[-1])
                filepath = os.path.join(directory, filename)

                if self.downloader == "self":
                    if not self.skip_download:
                        download_file(download_url, filepath)
                else:
                    if not self.skip_download:
                        subprocess.call(
                            external_downloader(
                                directory, filename, download_url, self.downloader
                            )
                        )
