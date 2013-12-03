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
                tmpfile = self.softwarename+".tmp"
                tempfile = open(tmpfile, "r+")
                if newlatest != oldlatest:
                        newversionmessage = "New Version: "+newlatest
                        notification(newversionmessage)
                        tempfile.seek(0)
                        tempfile.write(newlatest)
                        tempfile.truncate()
                else:
                        pass 
                tempfile.close()

def notification(message):
        fromjid = sys.argv[1]
        password = sys.argv[2]
        tojid = sys.argv[3]

        sendmessage(fromjid, password, tojid, message)

if __name__ == "__main__":
        if len(sys.argv) < 3:
                print "Syntax: release_news.py FROMJID PASSWORD TOJID"
                sys.exit(0)

        firefox = release_news('firefox', 'ftp.mozilla.org', 'pub/firefox/releases/latest/win32/de/')
        firefox.check()
