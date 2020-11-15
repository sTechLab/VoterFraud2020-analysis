import os
import json
import time
import pandas as pd
import streamlit as st


def print_progress(filename, progress, start_time, percentage=None):
    percentage_str = "({}%): ".format(round(percentage * 100)) if percentage else ""
    print(
        "{}{} lines in {} processed ({} sec)".format(
            percentage_str, progress, filename, time.time() - start_time
        )
    )


def parse_value(v):
    val = None
    if "arrayValue" in v:
        val = []
        if "values" in v["arrayValue"]:
            for item in v["arrayValue"]["values"]:
                val.append(parse_value(item))
    elif "nullValue" in v:
        val = None
    else:
        val = list(v.values())[0]
    return val


def parse_dataflow_export(directory, output_file, parse_item=None):
    start_time = time.time()
    if (os.path.exists(output_file)):
        print("{} already exists!")
        return
    for filename in os.listdir(directory):
        print("Processing {}".format(filename))
        processed = 0
        batch_time = time.time()

        with open(os.path.join(directory, filename), "r") as r:
            for line in r:
                raw = json.loads(line)
                raw = raw["properties"]
                data = {}
                for k, v in raw.items():
                    data[k] = parse_value(v)

                if parse_item:
                    data = parse_item(data)

                with open(output_file, "a") as w:
                    w.write(json.dumps(data) + "\n")
                processed += 1
                if processed % 10000 == 0:
                    print_progress(filename, processed, batch_time)
                    batch_time = time.time()

            print("Done processing {}".format(filename))
            print_progress(filename, processed, batch_time)
    print("Procesed all files in {}sec".format(time.time() - start_time))


def load_parsed_data(
    filename, include_cols=None, exclude_cols=None, parse_item=None, verbose=True, limit=None
):
    line_count = sum(1 for line in open(filename))
    total = limit if limit and limit < line_count else line_count
    print("Loading {} json lines".format(line_count))
    progress = 0
    start_time = time.time()
    batch_time = start_time
    json_data = []
    with open(filename) as r:
        for line in r:
            if (limit and progress >= limit):
                break

            data = json.loads(line)

            if parse_item:
                data = parse_item(data)
            
            if include_cols:
                parsed_data = {}
                for k, v in data.items():
                    if k in include_cols:
                        parsed_data[k] = v
                json_data.append(parsed_data)
            elif exclude_cols:
                parsed_data = {}
                for k, v in data.items():
                    if k not in exclude_cols:
                        parsed_data[k] = v
                json_data.append(parsed_data)
            else:
                json_data.append(data)

            progress += 1
            if progress % 100000 == 0 and verbose:
                print_progress(filename, progress, batch_time, progress / total)
                batch_time = time.time()   

    print("Done loading {}".format(filename))
    print_progress(filename, progress, start_time)

    return pd.DataFrame(json_data)


def load_crawled_terms(filename):
    crawled_terms = []
    with open(filename) as r:
        for line in r:
            crawled_terms.append(line.replace("\n", ""))

    return crawled_terms

