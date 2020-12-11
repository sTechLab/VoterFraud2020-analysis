import json
import pandas as pd
import os
import re
import requests
from collections import defaultdict
from multiprocessing import Pool
import multiprocessing
from datetime import datetime
import time
from urllib.parse import urlparse
import json
import numpy as np
import signal


def timeout(func, args=(), kwargs={}, timeout_duration=1, default=None):
    class TimeoutError(Exception):
        pass

    def handler(signum, frame):
        raise TimeoutError()

    # set the timeout handler
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(timeout_duration)
    try:
        result = func(*args, **kwargs)
    except TimeoutError as exc:
        result = default
    finally:
        signal.alarm(0)

    return result


def resolve_url(url):
    try:
        r = requests.get(url)
    except requests.exceptions.MissingSchema:
        url = "http://" + url
        return resolve_url(url)
    except requests.exceptions.Timeout:
        # Maybe set up for a retry, or continue in a retry loop
        history = [{"error": "timeout"}]
        return history
    except requests.exceptions.TooManyRedirects:
        # Tell the user their URL was bad and try a different one
        history = [{"error": "too many redirects"}]
        return history
    except requests.exceptions.RequestException as e:
        history = [{"error": "request exception"}]
        return history
    except:
        history = [{"error": "other exception"}]
        return history

    history = []
    for i in r.history:
        parsed_uri = urlparse(i.url)
        history.append(
            {"status_code": i.status_code, "url": i.url, "domain": parsed_uri.netloc}
        )
    parsed_uri = urlparse(r.url)
    history.append(
        {"status_code": r.status_code, "url": r.url, "domain": parsed_uri.netloc}
    )

    return history


with open(
    "./notebooks/data_export/url_stats/all_urls.json", "r", encoding="utf-8"
) as f:
    url_map = json.load(f)


def expand_url_map(url_map, limit=None):
    expanded_url_map = {}
    urls = url_map.keys() if limit is None else list(url_map.keys())[:limit]
    N = len(urls)
    for i, url in enumerate(urls):
        url_info = url_map[url].copy()
        url_expansion = timeout(resolve_url, (url,), timeout_duration=60, default=None)
        if url_expansion is None:
            url_expansion = [{"error": "process timeout"}]
        url_info["expansion_history"] = url_expansion
        expanded_url_map[url] = url_info
        if i % 50 == 0:
            print("{}/{}".format(i, N))

    return expanded_url_map

def process_urls(urls):
    current_worker = multiprocessing.current_process().name
    filename = "./data/expanded_urls/run-2/{}.json".format(current_worker)
    print("I'm {}. processing {} urls".format(current_worker, len(urls)))
    try:
        with open(filename, "r") as f:
            expanded_url_map = json.load(f)
    except:
        expanded_url_map = {}

    for url, url_info in urls:
        url_expansion = timeout(resolve_url, (url,), timeout_duration=60, default=None)
        if url_expansion is None:
            url_expansion = [{"error": "process timeout"}]
        url_info["expansion_history"] = url_expansion
        expanded_url_map[url] = url_info

    with open(filename, "w") as f:
        f.write(json.dumps(expanded_url_map) + "\n")
    print("{} Done. Wrote {} urls to file.".format(current_worker, len(urls)))


print(datetime.now())
if __name__ == "__main__":
    n_threads = 30
    urls = list(url_map.items())
    per_run = 50
    to_process = np.array_split(urls, len(urls) / 50)
    p = Pool(n_threads)
    p.map(process_urls, to_process)