import pytest
import responses
import mock
import json
import tempfile
import os

from release_news import (
    get_version_from_heise,
    get_version_from_ftp_files,
    get_version_from_ftp_dir,
    ReleaseNews,
    return_check_this)


@pytest.fixture
def heise_html():
    return '''
<html>
<head>
<meta property="og:locale" content="de_DE" />
<meta property="og:site_name" content="heise Download" />
<meta property="og:title" content="Firefox 34.0.5" />
<meta property="og:type" content="website" />
<meta property="og:url" content="http://www.heise.de/download/firefox.html" />
</head>
</body>
'''


@pytest.fixture
def ftp_filelist():
    return ['Firefox Setup 34.0.5.exe', 'Firefox Setup Stub 34.0.5.exe']


@pytest.fixture
def ftp_dirlist():
    return ['11.0.00', '11.0.02', '11.0.03', '11.0.04', '11.0.10', 'QFE']


@pytest.fixture
def versions_json(request):
    '''Empty versions.json tempfile.
    '''
    versions_tempfile = tempfile.mktemp()

    def fin():
        if os.path.exists(versions_tempfile):
            os.remove(versions_tempfile)

    request.addfinalizer(fin)
    return versions_tempfile


@pytest.fixture
def versions_json_content(request):
    '''versions.json tempfile with json content.
    '''
    versions_tempfile = tempfile.mktemp()

    content = {"jre": "Java Runtime Environment (JRE) 8u25",
               "firefox": "Firefox Setup 34.0.5.exe",
               "acrobat_reader": "11.0.10"}

    with open(versions_tempfile, 'w') as f:
        json.dump(content, f)

    def fin():
        os.remove(versions_tempfile)

    request.addfinalizer(fin)
    return versions_tempfile


@responses.activate
def test_get_version_from_heise(heise_html):
    '''version string from heise
    '''
    url = 'http://www.heise.de/download/firefox.html'
    responses.add(responses.GET,
                  url,
                  body=heise_html,
                  status=200)

    assert get_version_from_heise(url) == 'Firefox 34.0.5'


@mock.patch('ftplib.FTP.nlst')
def test_get_version_from_ftp_files(mock_nlst, ftp_filelist):
    '''version string from ftp filelist
    '''
    mock_nlst.return_value = ftp_filelist

    url = 'ftp://ftp.mozilla.org/pub/firefox/releases/latest/win32/de/'

    assert get_version_from_ftp_files(url) == 'Firefox Setup 34.0.5.exe'


@mock.patch('ftplib.FTP.nlst')
def test_get_version_from_ftp_dir(mock_nlst, ftp_dirlist):
    '''version string from ftp dirlist
    '''
    mock_nlst.return_value = ftp_dirlist

    url = 'ftp://ftp.adobe.com/pub/adobe/reader/win/11.x'

    assert get_version_from_ftp_dir(url) == '11.0.10'


@mock.patch('release_news.send_msg')
@responses.activate
def test_ReleaseNews(mock_send_msg,
                     versions_json,
                     versions_json_content,
                     heise_html):
    url = 'http://www.heise.de/download/firefox.html'
    responses.add(responses.GET,
                  url,
                  body=heise_html,
                  status=200)

    release_news = ReleaseNews(versions_file=versions_json_content)

    assert release_news.version_dict == {
        u'jre': u'Java Runtime Environment (JRE) 8u25',
        u'firefox': u'Firefox Setup 34.0.5.exe',
        u'acrobat_reader': u'11.0.10'}

    release_news = ReleaseNews(versions_file=versions_json)

    assert release_news.version_dict == {}

    @release_news.check_this
    def firefox():
        url = 'http://www.heise.de/download/firefox.html'
        return return_check_this(get_version_from_heise(url), url)

    release_news.checker('test@test.tld', 'test', 'recipient@test.tld')

    assert release_news.version_dict == {'firefox': u'Firefox 34.0.5'}


def test_return_check_this():
    url = 'http://www.heise.de/download/firefox.html'
    version = 'Firefox 34.0.5'
    expect = {'version': version,
              'url': url}

    assert return_check_this(version, url) == expect
