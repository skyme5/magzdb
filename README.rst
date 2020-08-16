==============================
magzdb - magzdb.org Downloader
==============================


.. image:: https://img.shields.io/pypi/v/magzdb.svg
        :target: https://pypi.python.org/pypi/magzdb

.. image:: https://img.shields.io/travis/skyme5/magzdb.svg
        :target: https://travis-ci.com/skyme5/magzdb

.. image:: https://pyup.io/repos/github/skyme5/magzdb/shield.svg
     :target: https://pyup.io/repos/github/skyme5/magzdb/
     :alt: Updates


Installation
------------

Install using pip

.. code-block:: bash

   pip install magzdb


Usage
-----

    usage: magzdb [-h] [-V] -i MAGAZINE_ID [-e [EDITION [EDITION ...]]] [-l] [-P DIRECTORY_PREFIX]

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         Print program version and exit
      -i MAGAZINE_ID, --id MAGAZINE_ID
                            ID of the Magazine to Download. eg. http://magzdb.org/j/<ID>.
      -e EDITION, --editions EDITION
                            Select Edition (you can specify multiple editions)
      -l, --latest          Download only latest edition.
      -P DIRECTORY_PREFIX, --directory-prefix DIRECTORY_PREFIX
                            Download directory.


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
