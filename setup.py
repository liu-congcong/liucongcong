#!/usr/bin/env python3
from setuptools import setup, find_packages


def main():
    setup(
        name = 'liucongcong',
        version = '1.0',
        url = 'https://github.com/liu-congcong/liucongcong/',
        author = 'Liucongcong',
        author_email = 'congcong_liu@icloud.com',
        license = 'GPLv3',
        description = 'Something I like',
        packages = find_packages(),
        package_data = {
            '': ['LICENSE'],
        },
    )


if __name__ == '__main__':
    main()
