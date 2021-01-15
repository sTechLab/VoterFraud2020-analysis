import logging

import tweepy

logger = logging.getLogger(__name__)


def to_bulk(a, size=100):
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


def fast_check(api, uids):
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
        active_uids = [u.id for u in users]
        inactive_uids = list(set(uids) - set(active_uids))
        return active_uids, inactive_uids
    except tweepy.TweepError as e:
        if e[0]['code'] == 50 or e[0]['code'] == 63:
            logger.error('None of the users is valid: %s', e)
            return [], inactive_uids
        else:
            # Unexpected error
            raise


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
            logger.warning('This user %r should be inactive', uid)
            yield (u, dict(code=-1, message='OK'))
        except tweepy.TweepyError as e:
            yield (uid, e[0][0])


def check_one_block(api, uids):
    """Check the status of user for one block (<100). """
    active_uids, inactive_uids = fast_check(api, uids)
    inactive_users_status = list(check_inactive(api, inactive_uids))
    return active_uids, inactive_users_status


def check_status(api, large_uids):
    """Check the status of users for any size of users. """
    active_uids = []
    inactive_users_status = []
    for uids in to_bulk(large_uids, size=100):
        au, iu = check_one_block(api, uids)
        active_uids += au
        inactive_users_status += iu
    return active_uids, inactive_users_status


def main(twitter_crendient, large_uids):
    """ The main function to call check_status. """
    # First prepare tweepy API
    auth = tweepy.OAuthHandler(twitter_crendient['consumer_key'],
                               twitter_crendient['consumer_secret'])
    auth.set_access_token(twitter_crendient['access_token'],
                          twitter_crendient['access_token_secret'])
    api = tweepy.API(auth, wait_on_rate_limit=True)
    # Then, call check_status
    active_uids, inactive_user_status = check_status(api, large_uids)