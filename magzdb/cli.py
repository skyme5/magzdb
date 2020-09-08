"""Console script for magzdb."""
import argparse
import sys

from magzdb.magzdb import Magzdb
from magzdb.version import __version__


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
        help="Use External downloader. Currently supported: aria2, wget",
        metavar="DOWNLOADER",
        choices=["aria2", "wget", "self"],
        default="self",
    )

    parser.add_argument(
        "--debug", help="Print debug information.", action="store_true",
    )

    args = parser.parse_args()

    dl = Magzdb(
        directory_prefix=args.directory_prefix,
        editions=args.editions,
        latest=args.latest,
        id=args.id,
        downloader=args.downloader,
        debug=args.debug,
    )
    dl.download()

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
