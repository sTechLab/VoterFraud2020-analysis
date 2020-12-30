from pathlib import Path
import gzip

data_dirs = [
    "data/coverage-test-us-pres/2020-11-13/hydrated",
    "data/coverage-test-us-pres/2020-11-06/hydrated",
]


def main():
    for data_dir in data_dirs:
        print("In datadir: {}".format(data_dir))
        total_tweet_count = 0
        total_hydrated_count = 0
        for path in Path(data_dir).iterdir():
            if path.name.endswith(".txt"):
                hydrated_filepath = str(path).replace(".txt", ".jsonl.gz")
                tweet_count = tweet_linecount(path)
                hydrated_count = hydrated_linecount(hydrated_filepath)
                if tweet_count != hydrated_count:
                    print(
                        "{} contains {} tweets, {} hydrated".format(
                            path.name, tweet_count, hydrated_count
                        )
                    )
                total_tweet_count += tweet_count
                total_hydrated_count += hydrated_count

        print(
            "Missing {} tweets in {} ({:,.1f}% hydrated)".format(
                total_tweet_count - total_hydrated_count,
                data_dir,
                (total_hydrated_count / total_tweet_count) * 100,
            )
        )


def _reader_generator(reader):
    b = reader(1024 * 1024)
    while b:
        yield b
        b = reader(1024 * 1024)


def tweet_linecount(fname):
    """
    Counts number of lines in file
    """
    f = open(fname, "rb")
    f_gen = _reader_generator(f.raw.read)
    return sum(buf.count(b"\n") for buf in f_gen)


def hydrated_linecount(fname):
    line_count = 0
    with gzip.open(fname) as zipfile:
        for line in zipfile:
            line_count += 1
    return line_count


if __name__ == "__main__":
    main()
