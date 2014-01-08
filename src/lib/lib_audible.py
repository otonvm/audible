#! python3
# -*- coding: utf-8 -*-

import re
import os
import sys
import time
import urllib.error
import urllib.request

try:
    import lib.lib_exceptions as lib_exceptions
    import lib.lib_utils as lib_utils
except ImportError as err:
    print("Cannot start module {}.".format(__file__), file=sys.stderr)
    print("Reason: {}.".format(err.msg), file=sys.stderr)
    raise SystemExit(1)

try:
    from bs4 import BeautifulSoup
except ImportError:
    raise ImportError("Unable to import BeautifulSoup!") from None

try:
    import html5lib  # used by bs, not needed directly
except ImportError:
    raise ImportError("Unable to import html5lib!") from None
del html5lib


def log(*msg):
    print(msg, file=sys.stderr)


class Metadata:
    def __init__(self):
        #private variables:
        self._url = None
        self._soup = None
        self._title = None
        self._title_raw = str()
        self._author = None
        self._author_span = None
        self._narrator_span = None
        self._narrator = None
        self._series_tuple = tuple()
        self._runtime = str()
        self._runtime_sec = None
        self._date_span = None
        self._date_obj = time.struct_time
        self._date = str()
        self._content_div = None
        self._content_div_list = list()
        self._description = None
        self._copyright = None

#---PRIVATE METHODS:
    def _test_soup(self):
        if not self._soup.body:
            raise lib_exceptions.BS4Exception("Cannot parse document structure.")

    def _load_soup(self, path, url):
        soup_dmp_path = os.path.join(path, "soup.dmp")
        if os.path.exists(soup_dmp_path):
            #soup_dmp = lib_utils.load_pickle(path)
            soup_dmp = None
            try:
                if soup_dmp[0] == url:
                    self._soup = soup_dmp[1]
                    log("loaded soup")
                    return True
                else:
                    try:
                        os.remove(soup_dmp_path)
                    except:
                        pass
            except:
                pass
        else:
            pass
        return False

    def _write_soup(self, path, url):
        soup_dmp = (url, self._soup)
        #lib_utils.dump_pickle(os.path.join(path, "soup.dmp"), soup_dmp)

    def _http_download(self, url, path=None):
        try:
            html = urllib.request.urlopen(url).read()
        except urllib.error.HTTPError as err:
            raise lib_exceptions.HTTPException("The server couldn't fulfill the request, \
                                            reason: {}".format(err.code)) from None
        except urllib.error.URLError as err:
            raise lib_exceptions.URLException("Failed to reach server, reason: {}".format(err.reason)) from None
        else:
            self._soup = BeautifulSoup(html, "html5lib")
            self._test_soup()

    def _local_file(self, file_path):
        try:
            with open(file_path, encoding='utf-8') as file:
                self._soup = BeautifulSoup(file, "html5lib")
                self._test_soup()
        except FileExistsError:
            raise lib_exceptions.FileError("Requested file inaccessible or already open.") from None
        except OSError:
            raise lib_exceptions.FileError("Could not open requested file.") from None

    def _set_title_raw(self):
        self._title_raw = self._soup.find('h1', {'class': 'adbl-prod-h1-title'}).string.strip()

    def _set_title(self):
        if not self._title_raw:
            self._set_title_raw()

        title_regex = re.search(r"^([\w\s']+)", self._title_raw)

        if title_regex:
            self._title = title_regex.group(1)
        else:
            raise lib_exceptions.RegExException("Could not extract title.") from None

    def _set_author_span(self):
        self._author_span = self._soup.find('li', {'class': 'adbl-author-row'})
        self._author_span = self._author_span.find('span', {'class': 'adbl-prod-author'})

    def _parse_author_span(self):
        if not self._author_span:
            self._set_author_span()

        #get all text from div and create list:
        author_span_list = self._author_span.text.strip().split(',')
        #strip unnecessary space from each string:
        author_span_list = [s.strip() for s in author_span_list]

        self._author = ', '.join(author_span_list)

    def _set_author(self):
        self._parse_author_span()

    def _set_narrator_span(self):
        self._narrator_span = self._soup.find('li', {'class': 'adbl-narrator-row'})
        self._narrator_span = self._narrator_span.find('span', {'class': 'adbl-prod-author'})

    def _parse_narrator_span(self):
        if not self._narrator_span:
            self._set_narrator_span()

        #get all text from div and create list:
        narrator_span_list = self._narrator_span.text.strip().split(',')
        #strip unnecessary space from each string:
        narrator_span_list = [s.strip() for s in narrator_span_list]

        self._narrator = ', '.join(narrator_span_list)

    def _set_narrator(self):
        self._parse_narrator_span()

    def _set_series_tuple(self):
        series = self._soup.find('div', {'class': 'adbl-series-link'})

        if series:
            series_name = series.a.string.strip()

            series_no = series.find('span', {'class': 'adbl-label'}).string.strip()
            series_no_match = re.search(r'^,\s\S+\s(\d+)$', series_no)

            if series_no_match:
                series_no = series_no_match.group(1)
            else:
                raise lib_exceptions.RegExException("Could not determine series position number.")

            self._series_tuple = (series_name, int(series_no))
        else:
            self._series_tuple = None

    def _set_series_tuple_from_title(self):
        if not self._title_raw:
            self._set_title_raw()

        exp = re.compile(r"^[\w\s]+:\s([\w\s']+),\sBook\s(\d)$")
        match = exp.match(self._title_raw)

        if match:
            series_title = match.group(1)
            series_no = int(match.group(2))

            self._series_tuple = (series_title, series_no)
        else:
            self._series_tuple = None

    def _set_runtime(self):
        self._runtime = self._soup.find('span', {'class': 'adbl-run-time'}).string.strip()

    def _regex_runtime(self):
        if not self._runtime:
            self._set_runtime()

        #match string like:
        #    23 hrs 45 mins
        #    15 hrs
        #returns an iterator of matches in sequence
        exp = re.compile(r'^(\d+)|\s(\d+)')
        match = re.findall(exp, self._runtime)

        #filter through tuples for actual results producing a list of either one or two entries:
        runtime_match_results = [l[0] or l[1] for l in match if l]

        if runtime_match_results:
            if len(runtime_match_results) == 1: # only hrs
                hrs = int(runtime_match_results[0])

                self._runtime_sec = hrs * 60 * 60
            elif len(runtime_match_results) == 2: # both hrs and mins
                hrs = int(runtime_match_results[0])
                mins = int(runtime_match_results[1])

                self._runtime_sec = (hrs * 60 * 60) + (mins * 60)
            else:
                raise lib_exceptions.RegExException("Could not convert runtime string into secconds.")


    def _set_date_span(self):
        self._date_span = self._soup.find('span', {"class": "adbl-date adbl-release-date"})

    def _set_date(self):
        if not self._date_span:
            self._set_date_span()

        date_text = self._date_span.text.strip()
        self._date_obj = time.strptime(date_text, "%m-%d-%y")


    def _set_content_div(self):
        self._content_div = self._soup.find('div', {"class": "adbl-content"})

    def _parse_content_div(self):
        if not self._content_div:
            self._set_content_div()

        #get all text from div and create list:
        content_div_list = self._content_div.text.strip().split('\n')
        #strip unnecessary space from each string:
        content_div_list = [s.strip() for s in content_div_list]
        #filter out all empty strings:
        content_div_list = [s for s in content_div_list if len(s) > 0]

        self._content_div_list = content_div_list

    def _set_description(self):
        if len(self._content_div_list) == 0:
            self._parse_content_div()
        self._description = ''.join([s for s in self._content_div_list if s[0] != '©'])

    def _set_copyright(self):
        if len(self._content_div_list) == 0:
            self._parse_content_div()
        self._copyright = self._content_div_list[-1]
        self._copyright = re.sub(r'\s\(P\)', '; Ⓟ', self._copyright)
        self._copyright = re.sub(r';;', ';', self._copyright)


#---PUBLIC METHODS:
    def reset(self):
        self._soup = None

    def http_page(self, url, path=None):
        """
        Method that downloads all contents from a web page.

        url: has to start with "http://www.audible.com/pd/"
        path: optional path to save and load backups of data
        """
        if self.is_url_valid(url):
            #no soup object exists:
            if not self._soup:
                #a path was provided and loading from pickle worked:
                if path and self._load_soup(path, url):
                    pass #we're done
                else:
                    #no data available so it has to be downloaded:
                    self._http_download(url)
                    if path: #a path was provided so a backup can be made
                        self._write_soup(path, url)
        else:
            raise lib_exceptions.URLException("{} provided is invalid. \
                                           It has to be in the form of http://www.audible.com/pd/*")

    @staticmethod
    def is_url_valid(url):
        try:
            return url.startswith("http://www.audible.com/pd/")
        except:
            return False

    def local_html(self, html_file):
        if not self._soup:
            self._local_file(html_file)

    @property
    def title(self):
        self._set_title()
        return self._title

    @property
    def title_raw(self):
        self._set_title()
        return self._title_raw

    @property
    def authors(self):
        self._set_author()
        return self._author

    @property
    def narrators(self):
        self._set_narrator()
        return self._narrator

    def series(self, try_title=False):
        if try_title:
            self._set_series_tuple_from_title()
        else:
            self._set_series_tuple()
        return self._series_tuple

    @property
    def runtime_string(self):
        self._set_runtime()
        return self._runtime

    @property
    def runtime_sec(self):
        self._regex_runtime()
        return self._runtime_sec

    @property
    def date_obj(self):
        self._set_date()
        return self._date_obj

    @property
    def date_utc(self):
        self._set_date()
        return time.strftime("%Y-%m-%dT%H:%M:%SZ", self._date_obj)

    @property
    def description(self):
        self._set_description()
        return self._description

    @property
    def copyright(self):
        self._set_copyright()
        return self._copyright

