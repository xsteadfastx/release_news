import os
from ftplib import FTP

def check_firefox():
        ftp = FTP('ftp.mozilla.org')
        ftp.login()
        ftp.cwd('pub/firefox/releases/latest/win32/de/')
        filelist = ftp.nlst()
        newlatest =  filelist[0]
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
                print 'IS GLEICH'
        else:
                print 'NICHT GLEICH'
                print newlatest
                print oldlatest
                tempfile.seek(0)
                tempfile.write(newlatest)
                tempfile.truncate()
        tempfile.close()
        return

if __name__ == "__main__":
        check_firefox()
