import os
import sys
from sendclient import SendMessage
from ftplib import FTP
from distutils.version import LooseVersion


class release_news:
        def __init__(self, FTPMethod, SoftwareName, ServerAdress, ServerDir):
                self.FTPMethod = FTPMethod
                self.SoftwareName = SoftwareName
                self.ServerAdress = ServerAdress
                self.ServerDir = ServerDir

        def GetNewLatest(self):
                if self.FTPMethod == 'latest':
                        ftp = FTP(self.ServerAdress)
                        ftp.login()
                        ftp.cwd(self.ServerDir)
                        FileList = ftp.nlst()
                        NewLatest = FileList[0]
                        return NewLatest
                elif self.FTPMethod == 'sort':
                        ftp = FTP(self.ServerAdress)
                        ftp.login()
                        ftp.cwd(self.ServerDir)
                        FileList = ftp.nlst()
                        SortList = sorted(FileList, key=LooseVersion)
                        NewLatest = SortList[-1]
                        return NewLatest
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

        firefox = release_news('latest', 'firefox', 'ftp.mozilla.org', 'pub/firefox/releases/latest/win32/de/')
        firefox.check()

        thunderbird = release_news('latest', 'thunderbird', 'ftp.mozilla.org', 'pub/thunderbird/releases/latest-esr/win32/de/')
        thunderbird.check()

        acrobatreader = release_news('sort', 'acrobatreader', 'ftp.adobe.com', 'pub/adobe/reader/win/11.x')
        acrobatreader.check()
