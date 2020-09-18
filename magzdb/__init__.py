"""Top-level package for magzdb."""
# For relative imports to work in Python 3.6
import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from magzdb.magzdb import Magzdb

__all__ = ["Magzdb"]
