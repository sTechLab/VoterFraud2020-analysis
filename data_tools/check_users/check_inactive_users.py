import csv
import tweepy
from dotenv import load_dotenv
import os
import json
import pandas as pd
from collections import defaultdict
import time
import sys

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

def check_inactive(api, uids):
    """ Check inactive account, one by one.
    Parameters
    ---------------
    uids : list
        A list of inactive account

    Returns
    ----------
        Yield tuple (uid, reason). Where `uid` is the account id,
        and `reason` is a string.
    """
    for uid in uids:
        try:
            u = api.get_user(user_id=uid)
            print('This user %r should be inactive', uid)
            yield (uid, dict(api_code=-1, reason='User is active'))
        except tweepy.TweepError as response:
            if ("Rate limit exceeded" in response.reason):
                raise response
            yield (uid, dict(api_code=response.api_code, reason=response.reason))

def map_type_to_filenames(data_type):
    return (
        "./data/fetch_users/inactive_uids_{}.txt".format(data_type),
        "./data/fetch_users/inactive_user_reason_{}.jsonl".format(data_type)
    )

if __name__ == '__main__':
    ## Set up dependencies and credentials

    load_dotenv()
    # CREDENTIALS = os.getenv("TWITTER_CREDENTIALS")

    try:
        print(sys.argv)
        uids_filename, reasons_filename = map_type_to_filenames(sys.argv[1])
        CREDENTIALS = sys.argv[2]
    except:
        print("Supply data type and twitter credentials filename as command-line argument!")
        print("Example: python check_inactive_users.py tweets private/credentials")
        exit()

    

    configs = []
    with open("./" + CREDENTIALS) as f:
        for ind, line in enumerate(f):
            configs.append(json.loads(line)) 
    credential = 0
    config = configs[credential]

    auth = tweepy.OAuthHandler(config['consumer_key'], config['consumer_secret'])
    auth.set_access_token(config['access_token'], config['access_token_secret'])

    api = tweepy.API(auth)
    
    known_users = set()
    with open(reasons_filename, "r") as f:
        for line in f.readlines():
            inactive_user = json.loads(line)
            known_users.add(inactive_user["user_id"])

    with open(uids_filename, "r") as inactive_uids:
        all_inactive_users = inactive_uids.read().split("\n")
        print("Inactive users:", len(all_inactive_users))
        users_to_check = [user_id for user_id in all_inactive_users if user_id not in known_users and user_id != ""]
        print("Known reasons:", len(all_inactive_users) - len(users_to_check))
        print("Checking users:", len(users_to_check))
        i = 0
        for batch in to_batch(users_to_check, 10):
            reasons = []
            try:
                for uid, response in check_inactive(api, batch):
                    reasons.append({
                        "user_id": uid,
                        "code": response["api_code"],
                        "reason": response["reason"]
                    })
            
                with open(reasons_filename, "a") as f:
                    for reason in reasons:
                        f.write(json.dumps(reason) + "\n")

                i += len(batch)
                print("Processed {}/{} user ids".format(i, len(users_to_check)))
            except Exception as e:
                if ("Rate limit exceeded" in e.reason):
                    print("Rate limited, waiting 1 minute")
                    time.sleep(60 * 1)
        print("Done!")