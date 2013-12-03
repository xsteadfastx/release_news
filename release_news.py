import os
import sys
from sendclient import sendmessage
from ftplib import FTP


class release_news:
        def __init__(self, softwarename, serveradress, serverdir):
                self.softwarename = softwarename
                self.serveradress = serveradress
                self.serverdir = serverdir

        def getnewlatest(self):
                ftp = FTP(self.serveradress)
                ftp.login()
                ftp.cwd(self.serverdir)
                filelist = ftp.nlst()
                newlatest = filelist[0]
                return newlatest

        def getoldlatest(self):
                tmpfile = self.softwarename+".tmp"
                if os.path.exists(tmpfile):
                        tempfile = open(tmpfile, "r+")
                else:
                        tempfile = open(tmpfile, "w")
                        tempfile.write(self.softwarename)
                        tempfile.close()
                        tempfile = open(tmpfile, "r+")
                tempinput = tempfile.readlines()
                tempfile.close()
                oldlatest = tempinput[0]
                return oldlatest

        def check(self):
                newlatest = self.getnewlatest()
                oldlatest = self.getoldlatest()
                print newlatest
                print oldlatest
                if newlatest != oldlatest:
                        newversionmessage = "New Version: "+self.getnewlatest()
                        #sendmessage(fromjid, password, tojid, newversionmessage)
                        print newversionmessage
                else:
                        tmpfile = self.softwarename+".tmp"
                        tempfile = open(tmpfile, "r+")
                        tempfile.seek(0)
                        tempfile.write(newlatest)
                        tempfile.truncate()
                        print "alles alt"
                        tempfile.close()

if __name__ == "__main__":
        if len(sys.argv) < 3:
                print "Syntax: release_news.py FROMJID PASSWORD TOJID"
                sys.exit(0)
        fromjid = sys.argv[1]
        password = sys.argv[2]
        tojid = sys.argv[3]

        firefox = release_news('firefox', 'ftp.mozilla.org', 'pub/firefox/releases/latest/win32/de/')
        firefox.check()
