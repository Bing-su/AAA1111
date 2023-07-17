from httpx import URL, Timeout

from aaa1111 import AAA1111


def test_base_url():
    api = AAA1111(host="example.com", port=3333, https=True)
    assert str(api.base_url) == "https://example.com:3333"
    api.base_url = URL("http://example.com")
    assert str(api.base_url) == "http://example.com"
    api.base_url = "https://example.com"
    assert isinstance(api.base_url, URL)
    api.base_url = api.base_url.join("/test")
    assert str(api.client.base_url) == "https://example.com/test/"
    assert str(api.aclient.base_url) == "https://example.com/test/"
    del api


def test_timeout():
    api = AAA1111(client_kwargs={"timeout": 10})
    assert api.client.timeout.connect == 10
    assert api.aclient.timeout.connect == 10
    api.timeout = Timeout(20)
    assert api.client.timeout.connect == 20
    assert api.aclient.timeout.read == 20
    api.timeout = Timeout(connect=10, read=20, write=30, pool=40)
    assert api.timeout.connect == 10
    assert api.timeout.pool == 40
    del api


def test_defaults():
    api = AAA1111(defaults={"prompts": "masterpiece"})
    assert api.defaults["prompts"] == "masterpiece"
