import pytest
import responses
import mock

from release_news import (
    get_version_from_heise,
    get_version_from_ftp_files,
    get_version_from_ftp_dir)


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
