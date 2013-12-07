import os
import sys
import requests
from sendclient import SendMessage
from ftplib import FTP
from distutils.version import LooseVersion
from bs4 import BeautifulSoup


class release_news:
        def __init__(self, CheckMethod, SoftwareName, ServerAdress, ServerDir):
                self.CheckMethod = CheckMethod
                self.SoftwareName = SoftwareName
                self.ServerAdress = ServerAdress
                self.ServerDir = ServerDir

        def GetNewLatestFTPDir(self):
                ftp = FTP(self.ServerAdress)
                ftp.login()
                ftp.cwd(self.ServerDir)
                FileList = ftp.nlst()
                SortList = sorted(FileList, key=LooseVersion)
                NewLatest = SortList[-1]
                return NewLatest

        def GetNewLatestFTPFile(self):
                ftp = FTP(self.ServerAdress)
                ftp.login()
                ftp.cwd(self.ServerDir)
                FileList = ftp.nlst()
                NewLatest = FileList[0]
                return NewLatest

        def GetNewLatestHeise(self):
                request = requests.get(self.ServerAdress)
                SiteContent = request.text
                soup = BeautifulSoup(SiteContent)
                FindVersion = soup.find_all(property="og:title")
                for found in FindVersion:
                        version = found.get('content')
                NewLatest = version
                return NewLatest

        def GetNewLatest(self):
                if self.CheckMethod == 'ftpfile':
                         return self.GetNewLatestFTPFile()
                elif self.CheckMethod == 'ftpdir':
                        return self.GetNewLatestFTPDir()
                elif self.CheckMethod == 'heise':
                        return self.GetNewLatestHeise()
                else:
                        pass

        def GetOldLatest(self):
                TempFilename = self.SoftwareName+".tmp"
                if os.path.exists(TempFilename):
                        TempFile = open(TempFilename, "r+")
                else:
                        TempFile = open(TempFilename, "w")
                        TempFile.write(self.SoftwareName)
                        TempFile.close()
                        TempFile = open(TempFilename, "r+")
                TempInput = TempFile.readlines()
                TempFile.close()
                OldLatest = TempInput[0]
                return OldLatest

        def check(self):
                NewLatest = self.GetNewLatest()
                OldLatest = self.GetOldLatest()
                TempFileName = self.SoftwareName+".tmp"
                TempFile = open(TempFileName, "r+")
                if NewLatest != OldLatest:
                        if self.CheckMethod == 'heise':
                                NewVersionMessage = "New %s Version: %s %s" % (self.SoftwareName, NewLatest, self.ServerAdress)
                        else:
                                NewVersionMessage = "New %s Version: %s ftp://%s/%s" % (self.SoftwareName, NewLatest, self.ServerAdress, self.ServerDir)
                        notification(NewVersionMessage)
                        TempFile.seek(0)
                        TempFile.write(NewLatest)
                        TempFile.truncate()
                else:
                        pass
                TempFile.close()

def notification(message):
        FromJID = sys.argv[1]
        password = sys.argv[2]
        ToJID = sys.argv[3]

        SendMessage(FromJID, password, ToJID, message)

if __name__ == "__main__":
        if len(sys.argv) < 3:
                print "Syntax: release_news.py FROMJID PASSWORD TOJID"
                sys.exit(0)

        firefox = release_news('ftpfile', 'firefox', 'ftp.mozilla.org', 'pub/firefox/releases/latest/win32/de/')
        firefox.check()

        thunderbird = release_news('ftpfile', 'thunderbird', 'ftp.mozilla.org', 'pub/thunderbird/releases/latest-esr/win32/de/')
        thunderbird.check()

        acrobatreader = release_news('ftpdir', 'acrobatreader', 'ftp.adobe.com', 'pub/adobe/reader/win/11.x')
        acrobatreader.check()

        jre = release_news('heise', 'jre', 'http://www.heise.de/download/java-runtime-environment-jre.html', 'none')
        jre.check()

        flash = release_news('heise', 'flash', 'http://www.heise.de/download/adobe-flash-player.html', 'none')
        flash.check()
