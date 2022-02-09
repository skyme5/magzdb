#!/usr/bin/env python
"""Tests for `magzdb` package."""
import os
import shutil
import unittest

import pytest

from magzdb import Magzdb
from magzdb.magzdb import Magzdb


class TestMagzdb(unittest.TestCase):
    """Tests for `magzdb` package."""

    def setUp(self):
        """Set up test fixtures"""
        self.data_dir = ".test-data"
        self.title = "Nature"
        self.magzdb = Magzdb(directory_prefix=self.data_dir, debug=True)
        self.magzdbDLWget = Magzdb(
            directory_prefix=self.data_dir, downloader="wget", debug=True
        )
        self.magzdbDLAria2 = Magzdb(
            directory_prefix=self.data_dir, downloader="aria2c", debug=True
        )
        self.magzdbDLCurl = Magzdb(
            directory_prefix=self.data_dir, downloader="curl", debug=True
        )
        self.magzdbNoDL = Magzdb(
            directory_prefix=self.data_dir,
            downloader="wget",
            debug=True,
            skip_download=True,
        )

    def tearDown(self):
        """Tear down test fixtures."""
        self.magzdb.request.close()
        self.magzdbDLWget.request.close()
        self.magzdbDLAria2.request.close()
        self.magzdbDLCurl.request.close()
        self.magzdbNoDL.request.close()
        if os.path.isdir(os.path.join(self.data_dir)):
            shutil.rmtree(os.path.join(self.data_dir))

    def test_download(self):
        """Test download."""
        self.magzdb.download(id="2249", editions=["2716361"])
        self.magzdb.download(id="2490", editions=["3694138"])

    def test_download_latest(self):
        """Test download."""
        self.magzdb.download(id="2249", editions=["2716361"], latest_only=True)

    def test_download_wget(self):
        """Test download."""
        self.magzdbDLWget.download(id="2249", editions=["2716361"])

    def test_download_aria2c(self):
        """Test download."""
        self.magzdbDLAria2.download(id="2249", editions=["2716361"])

    def test_download_curl(self):
        """Test download."""
        self.magzdbDLCurl.download(id="2249", editions=["2716361"])

    def test_issue_count(self):
        """Test download."""
        title, editions = self.magzdb.get_editions(id="1826")
        self.assertTrue(len(editions) >= 2441)
        self.assertEqual(title, self.title)

    def test_issue_filter(self):
        """Test download."""
        self.magzdbNoDL.download(id="2249", filter="eid == 2716361")
