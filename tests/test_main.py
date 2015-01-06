import pytest
import responses
import mock

from release_news import (
    get_version_from_heise,
    get_version_from_ftp_files)


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
