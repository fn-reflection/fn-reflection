# pylint: disable=missing-docstring,invalid-name
import requests
import pandas as pd


def _useragentcheck():
    requests.get("https://httpbin.org/get")


def _headercheck(headers=None):
    url = "https://www.whatismybrowser.com/detect/what-http-headers-is-my-browser-sending"
    res = requests.get(url, headers=headers)
    return pd.read_html(res.text)[0].set_index(0)[1].to_dict()


def pretendget(url):
    reqheader = {
        "User-Agent":
        ("Mozilla/5.0 (iPhone; CPU iPhone OS 9_3 like Mac OS X) "
         "AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 "
         "Mobile/13E188a Safari/601.1"),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}
    return requests.get(url, headers=reqheader)
