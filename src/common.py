def progress_bar(current, total):
    percent = 100 * (current / total)

    bar = chr(9608) * int(percent) + chr(9617) * int(100 - percent)

    print(f'\r {current} / {total} |{bar}| {percent:.1f}%', end='\r')


def split_by_thousands(number):
    return '{:,}'.format(number).replace(',', ' ')


ROLES = {
    'dev': ['96'],
    'analytics': ['156', '10', '150', '164', '148'],
    'dev_ops': ['160'],
    'data_science': ['165'],
    'qa': ['124'],
    'sys_admin': ['113'],
    'managment': ['36', '73', '104', '157', '107'],
    'design': ['25', '34'],
    'info_sec': ['116'],
    'support': ['121']
}
