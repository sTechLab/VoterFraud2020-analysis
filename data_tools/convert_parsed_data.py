import pandas as pd
import os
import sys
import json
import csv

parsed_export_dir = "./data/parsed-export/14-feb/"
final_export_dir = "./data/final-export/14-feb/"


def load_chunks(directory, dtype={}):
    print("Loading chunks from {}...".format(directory))
    chunk_dfs = []
    for name in sorted(os.listdir(directory)):
        sub_directory = os.path.join(directory, name)
        if os.path.isdir(sub_directory):
            for filename in sorted(os.listdir(sub_directory)):
                with open(os.path.join(sub_directory, filename), "r", encoding="utf-8") as f:
                    chunk = pd.read_csv(f, encoding="utf-8", dtype=dtype)
                    chunk_dfs.append(chunk)
        elif name.endswith(".csv"):
            chunk = pd.read_csv(
                os.path.join(directory, name),
                encoding="utf-8",
                dtype=dtype
            )
            chunk_dfs.append(chunk)

    return pd.concat(chunk_dfs)


if "tweets" in sys.argv:
    df_tweets = load_chunks("./data/hydrated/tweets", {
        "tweet_id": "str",
        "tweet_count": "int32", 
        "quote_count": "int32"
    })
    print("Creating lookup for tweets")
    tweet_id_lookup = set(df_tweets["tweet_id"])

    user_community_lookup = load_chunks("./data/hydrated/users", {
        "user_id": "str",
        "user_community": "Int64",
        "followers_count": "Int64"
    }).set_index("user_id")[["user_community", "user_active_status"]]


    print("Parsing tweets...")
    n_written = 0
    n_dups = 0

    with open(final_export_dir + "tweets.csv", "w", newline='') as f_out:
        f_out.write("tweet_id,user_community,user_active_status,retweet_count_metadata,quote_count_metadata,retweet_count_by_community_0,quote_count_by_community_0,retweet_count_by_community_1,quote_count_by_community_1,retweet_count_by_community_2,quote_count_by_community_2,retweet_count_by_community_3,quote_count_by_community_3,retweet_count_by_community_4,quote_count_by_community_4,retweet_count_by_suspended_users,quote_count_by_suspended_users,user_id,quote_tweet,hashtags,has_media,timestamp,text,urls,resolved_urls\n")
        tweet_writer = csv.writer(f_out, delimiter=',')
        with open(parsed_export_dir + "parsed_tweets.json", "r") as f_in:
            for line in f_in:
                data = json.loads(line)
                tweet_id = data["datastore_id"]
                user_id = data["user"]

                if (tweet_id not in tweet_id_lookup):
                    tweet_writer.writerow([
                        tweet_id,
                        user_community_lookup.loc[user_id]["user_community"] if user_id in user_community_lookup.index else "",
                        user_community_lookup.loc[user_id]["user_active_status"] if user_id in user_community_lookup.index else "",
                        data["retweet_count"],
                        data["quote_count"],
                        "",#retweet_count_by_community_0
                        "",#quote_count_by_community_0
                        "",#retweet_count_by_community_1
                        "",#quote_count_by_community_1
                        "",#retweet_count_by_community_2
                        "",#quote_count_by_community_2
                        "",#retweet_count_by_community_3
                        "",#quote_count_by_community_3
                        "",#retweet_count_by_community_4
                        "",#quote_count_by_community_4
                        "",#retweet_count_by_suspended_users
                        "",#
                        user_id,
                        data["quote_tweet"],
                        data["hashtags"],
                        data["hasMedia"],
                        data["timestamp"],
                        data["text"],
                        data["urls"],
                        "" #resolve_urls
                    ])
                    n_written += 1
                else:
                    n_dups += 1

        print("Found {:,} dups".format(n_dups))  # 203,824
        print("Wrote {:,} tweets".format(n_written))  # 13,278,947

elif "retweets" in sys.argv:
    df_published_retweets = load_chunks("./data/hydrated/retweets", {
        "user_id": "str",
        "retweeted_id": "str"
    })
    print("Creating lookup for retweets")
    retweet_ids = set([rt_id + "-" + user_id
                       for idx, rt_id, user_id
                       in df_published_retweets[["retweeted_id", "user_id"]].itertuples()])
    print("Parsing retweets...")
    n_written = 0
    n_dups = 0
    with open(final_export_dir + "retweets.csv", "w") as f_out:
        f_out.write("retweeted_id,user_id,timestamp\n")
        with open(parsed_export_dir + "parsed_retweets.json", "r") as f_in:
            for line in f_in:
                data = json.loads(line)
                rt_id = data["retweeted"]
                user_id = data["user"]
                timestamp = data["timestamp"]
                if (rt_id + "-" + user_id not in retweet_ids):
                    f_out.write("{},{},{}\n".format(
                        rt_id,
                        user_id,
                        timestamp
                    ))
                    n_written += 1
                else:
                    n_dups += 1

    print("Found {:,} dups".format(n_dups))  # 52,582
    print("Wrote {:,} retweets".format(n_written))  # 3,366,608


elif "users" in sys.argv:
    df_published_users = load_chunks("./data/hydrated/users", {
        "user_id": "str",
        "user_community": "Int64",
        "followers_count": "Int64"
    }).set_index("user_id")
    df_published_users.info()
    published_user_ids = set(df_published_users.index)
    
    print("Loading parsed users...")
    json_data = []
    with open(parsed_export_dir + "parsed_users.json", "r") as f_in:
        for line in f_in:
            data = json.loads(line)
            json_data.append(data)
    
    df_users = pd.DataFrame(json_data).rename(columns={
        "datastore_id": "user_id"
    }).set_index("user_id")[["name", "handle", "created_at", "verified", "description", "followers_count", "location"]].astype({
        "followers_count": "float"
    }).astype({
        "followers_count": "Int64"
    })

    new_user_ids = set(df_users.index)

    df_joined_users = df_published_users.join(df_users, how='outer', rsuffix="_new")

    print("New user count: {}".format(df_joined_users.shape[0])) # 2,857,618

for col in ["name", "handle", "created_at", "verified", "description", "followers_count", "location"]:
    df_joined_users[col] = df_joined_users.apply(lambda u: u[col + "_new"] if pd.isna(u[col]) else u[col], axis=1)

for col in ["name", "handle", "created_at", "verified", "description", "followers_count", "location"]:
    df_joined_users.drop(col + "_new", inplace=True, axis=1)
    
    # Make sure counts are integers / null
    df_joined_users = df_joined_users.astype({
        "retweet_count_by_community_0": "Int64",
        "quote_count_by_community_0": "Int64",
        "retweet_count_by_community_1": "Int64",
        "quote_count_by_community_1": "Int64",
        "retweet_count_by_community_2": "Int64",
        "quote_count_by_community_2": "Int64",
        "retweet_count_by_community_3": "Int64",
        "quote_count_by_community_3": "Int64",
        "retweet_count_by_community_4": "Int64",
        "quote_count_by_community_4": "Int64",
        "retweet_count_by_suspended_users": "Int64",
        "quote_count_by_suspended_users": "Int64",
    })
    df_joined_users.to_csv(final_export_dir + "users.csv", index_label="user_id", encoding="utf-8")