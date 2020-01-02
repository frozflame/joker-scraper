#!/usr/bin/env python3
# coding: utf-8

from __future__ import division, print_function

import pickle
import threading
import time
import traceback

import selenium.webdriver
from selenium.webdriver.firefox.options import Options


def get_simplistic_driver():
    prof = selenium.webdriver.FirefoxProfile()
    prof.set_preference('permissions.default.image', 2)
    prof.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
    prof.set_preference("media.volume_scale", "0.0")
    return selenium.webdriver.Firefox(firefox_profile=prof)


def until_success(func, retry, sleep, *args, **kwargs):
    for ix in reversed(range(retry + 1)):
        try:
            return func(*args, **kwargs)
        except Exception:
            time.sleep(sleep)
            if ix == 0:
                raise


def get_firfox_driver(headless=False, proxy=5, image=True, flash=True):
    opts = Options()
    opts.headless = headless
    prof = selenium.webdriver.FirefoxProfile()
    # http://kb.mozillazine.org/Network.proxy.type
    prof.set_preference("network.proxy.type", proxy)
    if not image:
        prof.set_preference('permissions.default.image', 2)
    if not flash:
        prof.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
    prof.update_preferences()
    return selenium.webdriver.Firefox(firefox_profile=prof, options=opts)


class Browser(object):
    def __init__(self, driver):
        self.driver = driver

    def get(self, url, extractor=None):
        self.driver.get(url)
        if extractor is None:
            return self.driver.page_source
        return extractor(self)

    def get_many(self, urls, extractor=None):
        return [self.driver.get(url, extractor) for url in urls]

    def select_one(self, selector, retry=5, sleep=5):
        return until_success(
            self.driver.find_element_by_css_selector,
            retry, sleep, selector,
        )

    def select(self, selector, retry=3, sleep=5):
        return until_success(
            self.driver.find_elements_by_css_selector,
            retry, sleep, selector,
        )

    # def fetch_image(self, url):
    #     self.driver.get(url)

    def close_all_but(self, handle):
        for h in self.driver.window_handles:
            if h != handle:
                self.driver.switch_to.window()

    def scroll_to_bottom(self):
        dr = self.driver
        dr.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def scroll_down(self, measure):
        dr = self.driver
        measure = int(measure)
        dr.execute_script("window.scrollBy(0, {});".format(measure))

    def dump_cookies(self, path):
        dr = self.driver
        pickle.dump(dr.get_cookies(), open(path, "wb"))

    def load_cookies(self, path):
        dr = self.driver
        cookies = pickle.load(open(path, "rb"))
        for cookie in cookies:
            dr.add_cookie(cookie)

    def set_element_attribute(self, element, key, value):
        js = "arguments[0].setAttribute('{}', '{}')".format(key, value)
        self.driver.execute_script(js, element)

    def debug_selector(self, sl, **kwargs):
        elements = self.select(sl)
        kwargs.setdefault('sep', '\t')
        if not elements:
            print('-', 'NotFound', sl, **kwargs)
            return
        for i, elem in enumerate(elements[:3]):
            si = '{}/{}'.format(i, len(elements))
            tx = ' '.join(elem.text.splitlines())[:100]
            print('-', si, repr(sl), tx, **kwargs)


BrowserManager = Browser


class BrowserPool(object):
    def __init__(self, size=3, driver_maker=None, extractor=None):
        # self.thrpool = multiprocessing.pool.ThreadPool(size)
        if driver_maker is None:
            driver_maker = get_simplistic_driver
        self.browsers = [Browser(driver_maker()) for _ in range(size)]
        self.extractor = extractor

    @staticmethod
    def _get(br, urls, results):
        while urls:
            url = urls.pop()
            try:
                results[url] = br.get(url)
            except BaseException:
                results[url] = traceback.format_exc()

    def map(self, urls):
        urls = list(urls)
        rev_urls = urls[::-1]
        results = {}
        threads = []
        for br in self.browsers:
            thr = threading.Thread(target=self._get, args=(br, urls, results))
            thr.start()
            threads.append(thr)
        for thr in threads:
            thr.join()
        return [results[url] for url in rev_urls]

