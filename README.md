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
usage: magzdb [-h] [-V] -i MAGAZINE_ID [-e [EDITION [EDITION ...]]]
              [-f FILTER] [-l] [-P DIRECTORY_PREFIX] [--downloader DOWNLOADER]
              [--debug]

Magzdb.org Downloader

required arguments:
  -i MAGAZINE_ID, --id MAGAZINE_ID
                        ID of the Magazine to Download. eg. http://magzdb.org/j/<ID>.

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         Print program version and exit
  -e [EDITION [EDITION ...]], --editions [EDITION [EDITION ...]]
                        Select Edition
  -f FILTER, --filter FILTER
                        Use filter. See README#Filters
  -l, --latest          Download only latest edition.
  -P DIRECTORY_PREFIX, --directory-prefix DIRECTORY_PREFIX
                        Download directory.
  --downloader DOWNLOADER
                        Use External downloader (RECOMMENDED). Currently supported: aria2, wget
  --debug               Print debug information.
```

### Usage Examples

#### Download all editions

```bash
$ magzdb -i 1826
```

#### Filters

You can supply filter using `-f`, for example to download issues between
`4063895` and `4063901`, you can write as

```bash
$ magzdb -i 1826 -f "eid > 4063895 and eid < 4063901"
```

You can use any of `eid`, `year`, `issue` the fields in the filter expression.

##### More examples of filter expression

- `eid > 4063895 and eid < 4063901` or `eid >= 4063895 and eid <= 4063901`
- `eid >= 4063895` or `eid != 4063895`
- `year >= 2018`, `year <= 2018`, `year == 2018` or even `year != 2018`
- `year >= 2018 and issue >= 10`

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

> This is recommended since internal downloader does not support resuming interrupted downloads.
