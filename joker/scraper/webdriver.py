#!/usr/bin/env python3
# coding: utf-8

import time

import selenium.webdriver
from selenium.webdriver import Firefox, Chrome, Safari, Opera
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.remote.webdriver import WebDriver

from joker.scraper.parser import ExtendedSoup
from joker.scraper.utils import until_success


class WebDriverExtendedMixin(WebDriver):
    @staticmethod
    def sleep(seconds=1):
        time.sleep(seconds)

    def scroll_to_bottom(self):
        self.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def scroll_down(self, measure):
        measure = int(measure)
        self.execute_script("window.scrollBy(0, {});".format(measure))

    def set_element_attribute(self, element, key, value):
        js = "arguments[0].setAttribute('{}', '{}')".format(key, value)
        self.execute_script(js, element)

    def select_one(self, selector, retry=5, sleep=5):
        return until_success(
            self.find_element_by_css_selector,
            retry, sleep, selector,
        )

    def select(self, selector, retry=3, sleep=5):
        return until_success(
            self.find_elements_by_css_selector,
            retry, sleep, selector,
        )

    def remove_scripts(self):
        js = """
        var c = document.getElementsByTagName('script');
        for(var i=0, n=c.length; i<n; i++){c[0] && c[0].replaceWith('');}
        """
        self.execute_script(js)

    def get_html(self, script=False, comment=False):
        if not script or not comment:
            soup = ExtendedSoup(self.page_source)
            if not script:
                soup.remove_scripts()
            if not comment:
                soup.remove_comments()
            return str(soup)
        return self.page_source

    def save_html(self, path: str, **kwargs):
        with open(path, 'w') as fout:
            fout.write(self.get_html(**kwargs))

    def save_page_source(self, path: str):
        with open(path, 'w') as fout:
            fout.write(self.page_source)

    def screenshot_element(self, selector: str, outpath: str, retry=3, sleep=5):
        el = self.select_one(selector, retry, sleep)
        return el.screenshot(outpath)


class FirefoxExtended(Firefox, WebDriverExtendedMixin):
    pass


class ChromeExtended(Chrome, WebDriverExtendedMixin):
    pass


class SafariExtended(Safari, WebDriverExtendedMixin):
    pass


class OperaExtended(Opera, WebDriverExtendedMixin):
    pass


def get_simplistic_driver():
    prof = selenium.webdriver.FirefoxProfile()
    prof.set_preference('permissions.default.image', 2)
    prof.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
    prof.set_preference("media.volume_scale", "0.0")
    return selenium.webdriver.Firefox(firefox_profile=prof)


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


def get_extended_firfox(headless=False, proxy=5, image=True, flash=True):
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
    return FirefoxExtended(firefox_profile=prof, options=opts)
