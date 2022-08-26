#!/usr/bin/python3.6

import time
from datetime import datetime
from mastodon import Mastodon

CLIENT_CRED = 'clientcred.txt'
ACCESS_TOKEN = 'apptoken.txt'
API_URL = 'https://{Instance FQDN}'
USER_LIST = 'following_accounts.csv'
LOG_FILE = 'unfollow_list.log'
EXPIREDAY = 30
TIMEWAIT = 5


def login():
    ''' Login to mastodon and create mastodon object '''

    mastodon = Mastodon(
        client_id=CLIENT_CRED,
        access_token=ACCESS_TOKEN,
        api_base_url=API_URL
    )
    return mastodon


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
        userid = None
        count_all += 1
        full_name = '@' + account_name[:-1]

        try:
            userid = (mastodon.search(q=full_name))['accounts'][0]['id']
        except IndexError:
            write_log('{}: -> Not found\n'.format(full_name))
            time.sleep(TIMEWAIT)
            continue

        res = mastodon.account_unfollow(userid)
        if res['following'] is False:
            res_text = 'Unfollowed'
            count_proc += 1
        else:
            res_text = 'Failed to unfollow'

        write_log('{}: [{}] -> {}\n'.format(full_name, userid, res_text))

        # Interval time of requests
        time.sleep(TIMEWAIT)

    nowday = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    write_log('—-- Unfollow process end at {} ---\n'.format(nowday))
    write_log('Unfollowed: {}users\n'.format(count_proc))
    write_log('Not unfollowed: {}users\n'.format(count_all - count_proc))


if __name__ == '__main__':
    main()
