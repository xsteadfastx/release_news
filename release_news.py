from bs4 import BeautifulSoup
from ftplib import FTP
from distutils.version import LooseVersion
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
import requests
import json
import sleekxmpp
import click
import re


class SendMsg(sleekxmpp.ClientXMPP):

    def __init__(self, jid, password, recipient, message):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        self.recipient = recipient
        self.msg = message

        self.add_event_handler('session_start', self.start, threaded=True)

    def start(self, event):
        self.send_presence()
        self.get_roster()

        self.send_message(mto=self.recipient,
                          mbody=self.msg,
                          mtype='chat')

        self.disconnect(wait=True)


def send_msg(jid, password, recipient, message):
    xmpp = SendMsg(jid, password, recipient, message)
    xmpp.register_plugin('xep_0030')
    xmpp.register_plugin('xep_0199')
    if xmpp.connect():
        xmpp.process(block=True)


def get_version_from_heise(url):
    '''Extract version from Heise downloads.
    '''
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    return soup.find(property='og:title')['content']


def get_version_from_ftp_dir(url):
    '''Extract version from FTP directory.
    '''
    url = urlparse(url)
    ftp = FTP(url.netloc)
    ftp.login()
    ftp.cwd(url.path)

    # only add version to dirlist if it has a number in it
    dirlist = [i for i in ftp.nlst() if re.search(r'.*[0-9].*', i)]

    ftp.close()
    return sorted(dirlist, key=LooseVersion)[-1]


def get_version_from_ftp_files(url):
    '''Extract version from FTP files.
    '''
    url = urlparse(url)
    ftp = FTP(url.netloc)
    ftp.login()
    ftp.cwd(url.path)

    # only add version to filelist if it has a number in it
    filelist = [i for i in ftp.nlst() if re.search(r'.*[0-9.*]', i)]

    ftp.close()
    return filelist[0]


class ReleaseNews(object):

    def __init__(self, versions_file='versions.json'):
        self.check_list = []
        self.versions_file = versions_file

        # try to open version.json file
        try:
            with open(self.versions_file, 'r') as f:
                self.version_dict = json.load(f)

        # if there is no versions.json file
        except IOError:
            self.version_dict = {}

    def _safe(self):
        '''Safe version json file to remember everything.
        '''
        with open(self.versions_file, 'w') as f:
            json.dump(self.version_dict, f)

    def check_this(self, func):
        '''Decorator to add function to check list.
        '''
        self.check_list.append(func)

    def checker(self, jid, password, recipient):
        '''The checker itself.
        '''
        for func in self.check_list:
            update_information = func()
            saved_version = self.version_dict.get(func.__name__)

            latest_version = update_information['version']

            if saved_version != latest_version:
                message = 'New Version for {}: {}'.format(
                    func.__name__, update_information['url'])

                send_msg(jid, password, recipient, message)

                self.version_dict[func.__name__] = latest_version

        # safe versions.json file
        self._safe()


# init release_news
release_news = ReleaseNews()


def return_check_this(get_version_from, url):
    '''Returns dict for check this functions.
    '''
    return {'version': get_version_from,
            'url': url}


@release_news.check_this
def jre():
    url = 'http://www.heise.de/download/java-runtime-environment-jre.html'
    return return_check_this(get_version_from_heise(url), url)


@release_news.check_this
def firefox():
    url = 'ftp://ftp.mozilla.org/pub/firefox/releases/latest/win32/de/'
    return return_check_this(get_version_from_ftp_files(url), url)


@release_news.check_this
def thunderbird():
    url = 'ftp://ftp.mozilla.org/pub/thunderbird/releases/latest-esr/win32/de/'
    return return_check_this(get_version_from_ftp_files(url), url)


@release_news.check_this
def acrobat_reader():
    url = 'ftp://ftp.adobe.com/pub/adobe/reader/win/11.x'
    return return_check_this(get_version_from_ftp_dir(url), url)


@release_news.check_this
def flash():
    url = 'http://www.heise.de/download/adobe-flash-player.html'
    return return_check_this(get_version_from_heise(url), url)


@release_news.check_this
def sevenzip():
    url = 'http://www.heise.de/download/7-zip.html'
    return return_check_this(get_version_from_heise(url), url)


@release_news.check_this
def tightvnc():
    url = 'http://www.heise.de/download/tightvnc.html'
    return return_check_this(get_version_from_heise(url), url)


@click.command()
@click.option('--jid',
              '-j',
              help='JID to log into XMPP Server.',
              prompt=True)
@click.option('--password',
              '-p',
              help='Password for XMPP Server.',
              prompt=True)
@click.option('--recipient',
              '-r',
              help='Recipient to send notification to.',
              prompt=True)
def main(jid, password, recipient):
    # run the checker
    release_news.checker(jid, password, recipient)


if __name__ == '__main__':
    main()
