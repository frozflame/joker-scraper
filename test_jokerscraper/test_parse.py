#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals

from joker.scraper.parser import asnum, asint
from bs4 import BeautifulSoup


def _make_soup(s):
    html = '<a id="a">{}</a>'.format(s)
    soup = BeautifulSoup(html, 'lxml')
    return soup.select_one('a#a')


def test():
    tag = _make_soup('2')
    assert asnum(tag) == 2
    assert isinstance(asnum(tag), int)

    tag = _make_soup('#2.')
    assert asnum(tag) == 2.
    assert isinstance(asnum(tag), float)
    assert asint(tag) is None

    tag = _make_soup('2')
    assert asint(tag) == 2
    assert isinstance(asnum(tag), int)


if __name__ == '__main__':
    test()