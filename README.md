<p>
  <div align="center">
  <h1>
    magzdb - magzdb.org Downloader<br /> <br />
    <a href="https://pypi.python.org/pypi/magzdb">
      <img
        src="https://img.shields.io/pypi/v/magzdb.svg"
        alt="Python Package"
      />
    </a>
    <a href="https://pypi.python.org/pypi/magzdb">
      <img
        src="https://img.shields.io/github/workflow/status/skyme5/magzdb/build"
        alt="CI"
      />
    </a>
    <a href="https://codecov.io/gh/skyme5/magzdb">
      <img
        src="https://img.shields.io/pypi/pyversions/magzdb"
        alt="Python Versions"
      />
    </a>
    <a href="https://github.com/psf/black">
      <img
        src="https://img.shields.io/badge/code%20style-black-000000.svg"
        alt="The Uncompromising Code Formatter"
      />
    </a>
    <a href="https://pepy.tech/project/magzdb">
      <img
        src="https://static.pepy.tech/badge/magzdb"
        alt="Monthly Downloads"
      />
    </a>
    <a href="https://opensource.org/licenses/MIT">
      <img
        src="https://img.shields.io/badge/License-MIT-blue.svg"
        alt="License: MIT"
      />
    </a>
  </h1>
  </div>
</p>

### Installation

Install using pip

```bash
$ pip install magzdb
```


### Usage

```text
usage: magzdb [-h] [-V] -i MAGAZINE_ID [-e [EDITION [EDITION ...]]] [-l] [-P DIRECTORY_PREFIX] [--downloader DOWNLOADER] [--debug]

Magzdb.org Downloader

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         Print program version and exit
  -i MAGAZINE_ID, --id MAGAZINE_ID
                        ID of the Magazine to Download. eg. http://magzdb.org/j/<ID>.
  -e [EDITION [EDITION ...]], --editions [EDITION [EDITION ...]]
                        Select Edition
  -l, --latest          Download only latest edition.
  -P DIRECTORY_PREFIX, --directory-prefix DIRECTORY_PREFIX
                        Download directory.
  --downloader DOWNLOADER
                        Use External downloader. Currently supported: aria2, wget
  --debug               Print debug information.
```

### Usage Examples

#### Download all editions

```bash
$ magzdb -i 1826
```

#### Download only latest edition

```bash
$ magzdb -i 1826 -l
```

#### Download only latest edition with custom location `magazine`

```bash
$ magzdb -i 1826 -l -P magazine
```

#### Use external downloader

```bash
$ magzdb -i 1826 -l -P magazine --downloader wget
```
