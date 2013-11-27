import os
import sys
import xmpp
from sendclient import sendmessage
from ftplib import FTP


def check_firefox():
        ftp = FTP('ftp.mozilla.org')
        ftp.login()
        ftp.cwd('pub/firefox/releases/latest/win32/de/')
        filelist = ftp.nlst()
        newlatest = filelist[0]
        if os.path.exists("firefox.tmp"):
                tempfile = open("firefox.tmp", "r+")
        else:
                tempfile = open("firefox.tmp", "w")
                tempfile.write("firefox")
                tempfile.close()
                tempfile = open("firefox.tmp", "r+")
        tempinput = tempfile.readlines()
        oldlatest = tempinput[0]
        if newlatest == oldlatest:
                return False
        else:
                tempfile.seek(0)
                tempfile.write(newlatest)
                tempfile.truncate()
                return True
        tempfile.close()

if __name__ == "__main__":
        if len(sys.argv) < 3:
                print "Syntax: release_news.py FROMJID PASSWORD TOJID"
                sys.exit(0)
        fromjid = sys.argv[1]
        password = sys.argv[2]
        tojid = sys.argv[3]
        if check_firefox():
                tempfile = open("firefox.tmp", "r")
                newlatest = tempfile.readlines()
                newversionmessage = "New Version: "+newlatest[0]
                sendmessage(fromjid, password, tojid, newversionmessage)
                tempfile.close()
        else:
                pass
