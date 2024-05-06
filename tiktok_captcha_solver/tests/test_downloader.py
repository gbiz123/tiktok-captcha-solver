from ..downloader import download_image_b64


def test_download_image_b64():
    result = download_image_b64("https://fastly.picsum.photos/id/237/536/354.jpg")
    assert len(result) > 1


