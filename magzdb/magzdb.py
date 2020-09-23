"""Main module."""
import os
import re
import subprocess
from unittest import case

import requests
from loguru import logger


class Magzdb:
    """Magzdb Downloader."""

    def __init__(
        self, directory_prefix=str, downloader=str, debug=False, skip_download=False,
    ):
        """Set global options.

        Args:
            directory_prefix (str, optional): Directory prefix for downloading. Defaults to current directory.
            downloader (str, optional): One of self, aria2, wget. Defaults to self.
            debug (bool, optional): logger.error debug information. Defaults to False.
        """
        self.directory_prefix = directory_prefix or os.getcwd()
        self.downloader = downloader
        self.debug = debug
        self.skip_download = skip_download

        self.REGEX_TITLE = re.compile(
            r"""<title>(?P<title>[^|]+)\|\s+magzDB</title>""",
            flags=re.IGNORECASE | re.MULTILINE,
        )
        self.REGEX_EDITION = re.compile(
            r"""<a\s*href="\/num\/(?P<id>\d+)"\s*title="(?P<year>\d+)\s*№[\[\(]?(?P<issue>\d+)[\]\)]?(\s*\((?P<edition>[\w]+)\))?"><span\s*style="background-color""",
            flags=re.IGNORECASE | re.MULTILINE,
        )

        self.EDITION_DOWNLOAD_PAGE = "http://magzdb.org/num/{}/dl"
        self.EDITION_DOWNLOAD_URL = "http://magzdb.org/file/{}/dl"
        self.USER_AGENT = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            "AppleWebKit/537.36 (KHTML, like Gecko)"
            "Chrome/84.0.4147.68 Safari/537.36"
        )

        self.reaponse_ok = requests.Response.ok
        self.request = requests.Session()

    def _print(self, msg: str):
        """logger.error debug information."""
        if self.debug:
            logger.debug(msg)

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
                headers = {"User-Agent": self.USER_AGENT}
                response = self.request.get(
                    url, stream=True, timeout=160, headers=headers
                )
                if response.status_code != self.reaponse_ok:
                    response.raise_for_status()

                self._print("Downloading to {}".format(dest))
                for data in response.iter_content(chunk_size=8192):
                    handle.write(data)
                handle.close()
        except FileExistsError:
            pass
        except requests.exceptions.RequestException:
            logger.error("File {} not found on Server {}".format(dest, url))
            pass

        if os.path.getsize(dest) == 0:
            os.remove(dest)

    def _html_regex(self, url, regex):
        try:
            docstring = self.request.get(url, allow_redirects=False).text
            return re.search(regex, docstring)
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
            allowed_tokens = "eid year issue and or < <= > >= =="
            number = re.compile(r"^[-+]?([1-9]\d*|0)$")
            return " ".join(
                [
                    e
                    for e in re.split(r"\s+", filter_str.lower())
                    if e in allowed_tokens or re.match(number, e)
                ]
            )

        def eval_filter(filter_str, params):
            eid, year, issue, *_ = params
            filter = filter_str.replace("eid", eid)
            filter = filter.replace("year", year)
            filter = filter.replace("issue", issue)
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

            return (title, editions)
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
        self, id: str, editions=list(), latest_only=bool, filter=None,
    ):
        """Download Editions."""
        title, all_editions = self.get_editions(id=id)
        title = self.get_valid_filename(title)
        directory = os.path.join(self.directory_prefix, title)

        selected_editions = self.apply_filter(all_editions, editions, filter)

        logger.info("Found {} editions of {}".format(len(selected_editions), title))

        for edition in list(reversed(selected_editions)):
            eid, year, issue, *_ = edition

            logger.info("Downloading year {} issue {}".format(year, issue))
            self._print("Issue ID: {}".format(eid))

            try:
                download_link_id = self._html_regex(
                    self.EDITION_DOWNLOAD_PAGE.format(eid),
                    r"""<a\s*href\=\.\.\/file\/(?P<id>\d+)/dl>""",
                ).group("id")
                self._print("Download Link ID: {}".format(download_link_id))

                download_url = self._html_regex(
                    self.EDITION_DOWNLOAD_URL.format(download_link_id),
                    r'''<a href="(?P<url>[^"]*\.\w+)"''',
                ).group("url")
                self._print("Download URL: {}".format(download_url))
            except AttributeError:
                logger.error(
                    "Download Url not found for http://magzdb.org/num/{}/dl".format(eid)
                )
                continue

            filename = self.get_valid_filename(download_url.split("/")[-1])
            filepath = os.path.join(directory, filename)

            if self.downloader != "self":

                def downloader_command(dir, filename, url):
                    return {
                        "aria2": 'aria2c -c --dir="{}" --out="{}" "{}"'.format(
                            dir, filename, url
                        ),
                        "wget": 'wget -c -O "{}/{}" "{}"'.format(dir, filename, url),
                    }[self.downloader]

                command = downloader_command(directory, filename, download_url)
                self._print(command)
                if self.skip_download is False:
                    subprocess.run(command)
            else:
                if self.skip_download is False:
                    self._download_file(download_url, filepath)

            if latest_only:
                return
