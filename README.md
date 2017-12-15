# Mastodon batch scripts

Unfollow scripts for batch processing at Mastodon.

## Requirements

* Python >= 3.6
* [Mastodon.py](https://github.com/halcy/Mastodon.py)

## Preparations

1. Creates a new OAuth app and get client id and access token.
2. The values of client id and access token save text files.
3. Change some variable in each script. 

```
CLIENT_CRED = '{client id file path}'
ACCESS_TOKEN = '{access token file path}'
API_URL = 'https://{mastodon instance host}'
USER_LIST = 'following_accounts.csv'
LOG_FILE = '{log file path}'
```

## Warning

Always set the TIMEWAIT value to 5 or more. Otherwise you could put a heavy load on the instance.

## unfollow_list.py

Script to unfollow all users in list file.

### Usage

```
$ python unfollow_list.py
```

## unfollow_dead_user.py

Script to unfollow users below:
* All users who have not toot since the specified date
* All users who have never touched

### Usage

```
$ python unfollow_list.py
```


## unfollow_not_mutual.py

Script to unfollow all users who are not following each other.

### Usage

```
$ python unfollow_list.py
```

## Author

[itsumonotakumi@pawoo.net](https://pawoo.net/@itsumonotakumi)