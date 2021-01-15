import time

def to_batch(a, size=100):
    """Transform a list into list of list. Each element of the new list is a
    list with size=100 (except the last one).
    """
    r = []
    qt, rm = divmod(len(a), size)
    i = -1
    for i in range(qt):
        r.append(a[i * size:(i + 1) * size])
    if rm != 0:
        r.append(a[(i + 1) * size:])
    return r

def batch_fetch_users(api, uids):
    """ Fast check the status of specified accounts.
    Parameters
    ---------------
        api: tweepy API instance
        uids: account ids

    Returns
    ----------
    Tuple (active_uids, inactive_uids).
        `active_uids` is a list of active users and
        `inactive_uids` is a list of inactive uids,
            either supended or deactivated.
    """
    try:
        users = api.lookup_users(user_ids=uids,
                                 include_entities=False)
        active_uids = [str(u.id) for u in users]
        inactive_uids = list(set(uids) - set(active_uids))
        return users, inactive_uids
    except tweepy.TweepError as e:
        error_code = e.api_code
        if error_code == 17:
            return [], uids
        else:
            # Unexpected error
            print("Unknown error", e)
            raise e

def fetch_users(api, uids):
    active_users = []
    inactive_uids = []
    for batch_uids in to_batch(uids, size=100):
        try:
            users, inactive = batch_fetch_users(api, batch_uids)
            active_users += users
            inactive_uids += inactive
        except tweepy.TweepError as e:
            print("Failed", e)
            print("Waiting 3 minutes")
            time.sleep(180)
            return active_users, inactive_uids
        
    return active_users, inactive_uids

def get_users(type):
    if (type == "missing_active_uids"):
        known_users = set()
        with open("./data/fetch_users/inactive_uids_retweets_2.txt", "r") as f:
            for uid in f.readlines():
                known_users.add(uid.replace("\n", ""))

        unknown_users = set()
        with open("./data/fetch_users/missing_active_user_ids.txt", "r") as f:
            for uid in f.readlines():
                unknown_users.add(uid.replace("\n", ""))

    return known_users, unknown_users



if __name__ == '__main__':
    ## Set up dependencies and credentials

    import csv
    import tweepy
    from dotenv import load_dotenv
    import os
    import json
    import pandas as pd
    import networkx as nx
    from collections import defaultdict

    load_dotenv()
    CREDENTIALS = os.getenv("TWITTER_CREDENTIALS")

    configs = []
    with open("./" + CREDENTIALS) as f:
        for ind, line in enumerate(f):
            configs.append(json.loads(line)) 
    credential = 0
    config = configs[credential]

    auth = tweepy.OAuthHandler(config['consumer_key'], config['consumer_secret'])
    auth.set_access_token(config['access_token'], config['access_token_secret'])

    api = tweepy.API(auth)

    TYPE = "missing_active_uids"

    if (TYPE == "retweets"):
        print("Loading dataframes...")
        known_users = set(
            pd.read_pickle('./notebooks/df_users_with_clustering.pickle')
            .sort_values("followers_count", ascending=False).index.values)
        df_retweets = pd.read_pickle('./data/dataframes/16-dec/df_retweets.pickle')

        print("Loading known/unknown users...")
        with open("./data/fetch_users/users_retweets.jsonl", "r") as f:
            for line in f.readlines():
                user = json.loads(line)
                known_users.add(str(user["id"]))

        def add_user(user_id):
            if (user_id not in known_users):
                unknown_users.add(user_id)

        for i, user1, user2 in df_retweets[["user", "retweetedFrom_user"]].itertuples():
            add_user(user1)
            add_user(user2)
    else:
        known_users, unknown_users = get_users(TYPE)

    print("Total user ids:", len(known_users.union(unknown_users)))
    users_to_check = list(unknown_users)
    print("Known users:", len(known_users))
    print("Checking users:", len(unknown_users))

    i = 0
    inactive_counter = 0
    print("Fetching users...")
    for batch in to_batch(users_to_check, 1000):
        active_users, inactive_uids = fetch_users(api, batch)

        with open("./data/fetch_users/users_retweets_2.jsonl", "a") as f:
            for user in active_users:
                f.write(json.dumps(user._json) + "\n")

        with open("./data/fetch_users/inactive_uids_retweets_2.txt", "a") as f:
            for uid in inactive_uids:
                f.write(str(uid)+ "\n") 
        
        inactive_counter += len(inactive_uids)

        i += len(batch)
        print("Processed {}/{} users".format(i, len(users_to_check)))
        print("Inactive users seen:", inactive_counter)