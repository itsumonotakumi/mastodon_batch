#!/bin/env python3.6

import time
from datetime import datetime
from mastodon import Mastodon

CLIENT_CRED = 'clientcred.txt'
ACCESS_TOKEN = 'apptoken.txt'
API_URL = 'https://pawoo.net'
USER_LIST = 'following_accounts.csv'
LOG_FILE = 'unfollow_not_mutual.log'
TIMEWAIT = 5


def login():
    ''' Login to mastodon and create mastodon object '''

    mastodon = Mastodon(
        client_id=CLIENT_CRED,
        access_token=ACCESS_TOKEN,
        api_base_url=API_URL
    )
    return mastodon


def is_mutual(mstdn, userid):
    ''' Check if mutual user '''

    rel = (mstdn.account_relationships(userid))[0]
    if rel['followed_by'] is True or rel['following'] is False:
        return(True)
    else:
        return(False)


def write_log(text):
    ''' Write text to log file '''
    with open(LOG_FILE, 'a') as f:
        f.write(text)


def main():
    # Initializition of Mastodon
    mastodon = login()

    nowday = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    write_log('—-- Unfollow process start at {} ---\n'.format(nowday))

    # Fetch account id number
    with open(USER_LIST) as f:
        name_list = f.readlines()

    count_all = 0
    count_proc = 0
    for account_name in name_list:
        res_text = ''
        count_all += 1
        full_name = '@' + account_name[:-1]

        try:
            userid = (mastodon.search(q=full_name))['accounts'][0]['id']
        except IndexError:
            res_text = 'Not found'

        # Check relation and unfollow
        if res_text is '' and is_mutual(mastodon, userid) is False:
            if (mastodon.account_unfollow(userid))['following']:
                res_text = 'Failed to unfollow'
            else:
                res_text = 'Unfollowed'
                count_proc += 1
        elif res_text is '':
            res_text = 'Not unfollow'

        write_log('{}: [{}] -> {}\n'.format(full_name, userid, res_text))

        # Interval time of requests
        time.sleep(TIMEWAIT)

    nowday = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    write_log('—-- Unfollow process end at {} ---\n'.format(nowday))
    write_log('Unfollowed: {}users\n'.format(count_proc))
    write_log('Not unfollowed: {}users\n'.format(count_all - count_proc))


if __name__ == '__main__':
    main()
