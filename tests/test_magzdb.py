#!/usr/bin/env python
"""Tests for `magzdb` package."""
import os
import shutil
import unittest
from unittest.case import skip

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
        self.magzdbNoDL.request.close()
        if os.path.isdir(os.path.join(self.data_dir)):
            shutil.rmtree(os.path.join(self.data_dir))

    def test_download(self):
        """Test download."""
        self.magzdb.download(id="2249", editions=["2716361"])

    def test_download_wget(self):
        """Test download."""
        self.magzdbDLWget.download(id="2249", editions=["2716361"])

    def test_issue_count(self):
        """Test download."""
        title, editions = self.magzdb.get_editions(id="1826")
        self.assertTrue(len(editions) >= 2441)
        self.assertEqual(title, self.title)

    def test_issue_filter(self):
        """Test download."""
        self.magzdbNoDL.download(id="2249", filter="eid == 2716361")
