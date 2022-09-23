import secrets
import collections.abc

from django.contrib.auth.models import AnonymousUser


def make_random_string(length=10, allowed_chars='abcdefghjkmnpqrstuvwxyz'
                                                'ABCDEFGHJKLMNPQRSTUVWXYZ'
                                                '23456789'):
    return ''.join(secrets.choice(allowed_chars) for i in range(length))


def clip_text(string, max_length):
    if len(string) > max_length:
        return string[0:max_length]

    return string


def pluralize(number, text):
    if number == 1:
        return text
    else:
        return text + "s"


def compute_usernames(user, usernames):
    in_view = []

    if not isinstance(user, AnonymousUser):
        if user.username in usernames:
            in_view.append(user.username)

    for username in usernames:
        if username in in_view:
            continue

        in_view.append(username)
        if len(in_view) >= 3:
            break

    if len(usernames) > 3:
        in_view.append((usernames - 3).__str__())

    return in_view


def format_file_size(size):
    power = 2 ** 10
    n = 0
    power_labels = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return size, power_labels[n] + 'B'


def update_dict(d, u):
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = update_dict(d.get(k, {}), v)
        else:
            d[k] = v
    return d
