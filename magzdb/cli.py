"""Console script for magzdb."""
import argparse
import signal
import sys

from loguru import logger

from magzdb.magzdb import Magzdb
from magzdb.version import __version__


def handler(signum, frame):
    exit(0)


def main():
    """Console script for magzdb."""
    parser = argparse.ArgumentParser(description="Magzdb.org Downloader")

    parser.add_argument(
        "-V",
        "--version",
        action="version",
        help="Print program version and exit",
        version=__version__,
    )

    parser.add_argument(
        "-i",
        "--id",
        help="ID of the Magazine to Download. eg. http://magzdb.org/j/<ID>.",
        metavar="MAGAZINE_ID",
        required=True,
        type=str,
    )

    parser.add_argument(
        "-e",
        "--editions",
        help="Select Edition",
        metavar="EDITION",
        nargs="*",
        type=str,
    )

    parser.add_argument(
        "-f", "--filter", help="Use filter. See README#Filters", type=str, default=None,
    )

    parser.add_argument(
        "-l", "--latest", action="store_true", help="Download only latest edition.",
    )

    parser.add_argument(
        "-P",
        "--directory-prefix",
        help="Download directory.",
        metavar="DIRECTORY_PREFIX",
        type=None,
    )

    parser.add_argument(
        "--downloader",
        help="Use External downloader (RECOMMENDED). Currently supported: aria2, wget",
        metavar="DOWNLOADER",
        choices=["aria2", "wget", "curl", "self"],
        default="self",
    )

    parser.add_argument(
        "--debug", help="Print debug information.", action="store_true",
    )

    parser.add_argument(
        "--skip-download", help="Don't download files.", action="store_true",
    )

    args = parser.parse_args()

    if args.downloader == "self":
        logger.warning("Use of external downloader like wget or aria2 is recommended")

    dl = Magzdb(
        directory_prefix=args.directory_prefix,
        downloader=args.downloader,
        debug=args.debug,
        skip_download=args.skip_download,
    )

    signal.signal(signal.SIGINT, handler)

    dl.download(
        id=args.id,
        editions=args.editions or list(),
        latest_only=args.latest,
        filter=args.filter,
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
