import os
from collections.abc import Generator
import zipfile
from contextlib import contextmanager
from io import BufferedWriter
import tempfile
import requests
import logging

LOGGER = logging.getLogger(__name__)

# https://stackoverflow.com/questions/7184793/how-to-download-a-crx-file-from-the-chrome-web-store-for-a-given-id
EXTENSION_ID = "colmpcmlmokfplanmjmnnahkkpgmmbjl"
CHROME_EXT_DOWNLOAD_URL = f"https://clients2.google.com/service/update2/crx?response=redirect&prodversion=126.0.6478.270&acceptformat=crx2,crx3&x=id%3D{EXTENSION_ID}%26uc"

def download_extension_to_unpacked() -> tempfile.TemporaryDirectory:
    with download_extension_to_tempfile() as f:
        temp_dir = tempfile.TemporaryDirectory()
        with zipfile.ZipFile(f.name, "r") as zip_file:
            zip_file.extractall(temp_dir.name)
            LOGGER.debug("extracted crx to directory: " + temp_dir.name)
            return temp_dir


@contextmanager
def download_extension_to_tempfile() -> Generator[BufferedWriter, None, None]:
    r = requests.get(CHROME_EXT_DOWNLOAD_URL)
    LOGGER.debug("downloaded chrome extension from " + CHROME_EXT_DOWNLOAD_URL)
    tf = open(os.path.join(tempfile.gettempdir(), os.urandom(24).hex()), "wb")
    _ = tf.write(r.content)
    LOGGER.debug("wrote chrome extension to temp file at: " + tf.name)
    try:
        yield tf
    finally:
        tf.close()
