import os
import subprocess

import requests
from loguru import logger

DOWNLOADER_LIST = ["aria2c", "curl", "self", "wget"]


def download_file(url: str, dest: str):
    USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        "AppleWebKit/537.36 (KHTML, like Gecko)"
        "Chrome/84.0.4147.68 Safari/537.36"
    )

    if len(os.path.dirname(dest)) > 0:
        os.makedirs(os.path.dirname(dest), exist_ok=True)

    try:
        if os.path.isfile(dest) and os.path.getsize(dest) == 0:  # pragma: no cover
            os.remove(dest)
    except FileNotFoundError:
        pass

    try:
        with open(dest, "xb") as handle:
            headers = {"User-Agent": USER_AGENT}
            response = requests.get(url, stream=True, timeout=160, headers=headers)
            if response.status_code != requests.Response.ok:
                response.raise_for_status()

            for data in response.iter_content(chunk_size=8192):
                handle.write(data)
            handle.close()
    except FileExistsError:
        pass
    except requests.exceptions.RequestException:
        logger.error(f"File {dest} not found on Server {url}".format(dest))
        pass

    if os.path.getsize(dest) == 0:  # pragma: no cover
        os.remove(dest)


def external_downloader(dir: str, filename: str, url: str, name: str):
    parameters = {
        "aria2": [
            "aria2c",
            "-c",
            "-s",
            f'--dir="{dir}"',
            f'--out="{filename}"',
            f'"{url}"',
        ],
        "wget": ["wget", "-nv", "-c", "-O", os.path.join(dir, filename), url,],
        "curl": [
            "curl",
            f'"{url}"',
            "--output",
            f'"{os.path.join(dir, filename)}"',
            "--silent",
        ],
    }

    return parameters.get(name)
