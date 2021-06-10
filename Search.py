from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication
import requests,re,sys,time,win32gui,win32api,win32con
from bs4 import BeautifulSoup
from untitled import Ui_Form

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon('D://UI//ico.ico'))
        self.ui.pushButton.clicked.connect(self.pushButton_Click_Search)#搜尋
        self.ui.pushButton_2.clicked.connect(self.pushButton_Click_Copy1)#複製1
        self.ui.pushButton_3.clicked.connect(self.pushButton_Click_Copy2)#複製2
        self.ui.pushButton_4.clicked.connect(self.pushButton_Click_Paste)#貼上
        self.header={
            'Connection': 'keep-alive',
            'DNT': '1',
            'Host': 'www.bimiacg.net',
            'Referer': 'http://www.bimiacg.net/bangumi/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
            }
        self.header2={
                'DNT': '1',
                'Range': 'bytes=0-',
                'Host': '49.234.56.246',
                'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
                }
    
    def pushButton_Click_Search(self):
        URL=self.ui.lineEdit.text().strip()
        self.ui.lineEdit.clear()
        try:
            Referer=re.compile(r'\d+/play').findall(URL)[0]
        except:
            self.ui.lineEdit_2.clear()
            self.ui.lineEdit_3.setText('網址輸入錯誤')
        Referer=re.sub('/play', '', Referer)
        if re.compile(r'www.bimiacg.net').findall(URL)!=[]:
            Referer='http://www.bimiacg.net/bangumi/'+Referer
        elif re.compile(r'm.bimibimi.cc').findall(URL)!=[]:
            Referer='http://m.bimibimi.cc/bangumi/'+Referer
            self.header["Host"]='m.bimibimi.cc'
        elif re.compile(r'www.bimiacg.com').findall(URL)!=[]:
            Referer='http://www.bimiacg.com/bangumi/'+Referer
            self.header["Host"]='www.bimiacg.com'
        else:
            Referer=re.compile('http[s:]*//\w+.\w+.\w+/').findall(URL)[0]+Referer
            self.header["Host"]=re.compile('\w+.\w+.\w+').findall(URL)[0]
            
        self.header["Referer"]=Referer
        try:
            r = requests.get(URL,headers=self.header)
            script = BeautifulSoup(r.text,"html.parser").find_all('div','play-player')
            uid=re.compile(r'"url":".+"').findall(str(script))[0]
            uid=re.sub('","url_next":.+', '', uid)
            uid=re.sub('"url":"', '', uid)
            VideoHtml='http://49.234.56.246/danmu/play.php?url='+uid+'&myurl='+URL
            self.ui.lineEdit_2.setText(VideoHtml)
            r = requests.get(VideoHtml,headers=self.header2)
            soup = BeautifulSoup(r.text,"html.parser")
            script = soup.select("video")
            uid=re.compile(r'src=".+"').findall(str(script))[0]
            uid=re.sub('" type.+', '', uid)
            VideoHtml2=re.sub('src="', '', uid)
            self.ui.lineEdit_3.setText(VideoHtml2)
        except Exception as err:
            try:
                VideoHtml='http://49.234.56.246/danmu/m3u8.php?url='+uid+'&myurl='+URL
                self.ui.lineEdit_2.setText(VideoHtml)
                r = requests.get(VideoHtml,headers=self.header2)
                soup = BeautifulSoup(r.text,"html.parser")
                script = soup.select("video")
                uid=re.compile(r'src=".+"').findall(str(script))[0]
                uid=re.sub('" type.+', '', uid)
                VideoHtml2=re.sub('src="', '', uid)
                self.ui.lineEdit_3.setText(VideoHtml2)
            except:
                self.ui.lineEdit_2.clear()
                self.ui.lineEdit_3.setText('錯誤: '+str(err))
        
    def pushButton_Click_Copy1(self):
        QApplication.clipboard().setText(self.ui.lineEdit_2.text())
    def pushButton_Click_Copy2(self):
        QApplication.clipboard().setText(self.ui.lineEdit_3.text())
    def pushButton_Click_Paste(self):
        QApplication.clipboard().setText(self.ui.lineEdit_2.text())
        handle = win32gui.FindWindow(None,"VRChat")
        win32gui.SetForegroundWindow(handle)
        time.sleep(.1)
        win32api.keybd_event(0x11, 0, 0, 0)
        time.sleep(.05)
        win32api.keybd_event(0x56, 0, 0, 0)
        win32api.keybd_event(0x56, 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(.05)
        win32api.keybd_event(0x11, 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(.1)
        win32api.keybd_event(0x0D, 0, 0, 0)
        win32api.keybd_event(0x0D, 0, win32con.KEYEVENTF_KEYUP, 0)

    def closeEvent(self, event):
        QApplication.closeAllWindows()
        
if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())