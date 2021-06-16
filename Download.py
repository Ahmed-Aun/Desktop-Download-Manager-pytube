from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
#from PyQt5.uic import loadUiType
import sys
import os
from os import path
import urllib.request

from pytube import YouTube
from pytube import Playlist
from main import Ui_MainWindow

#uiFile, _ = loadUiType('main.ui')

class MainApp(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setup_userInterface()

    def setup_userInterface(self):
        self.setWindowTitle('Joud Download Manager')
        self.setFixedSize(614, 314)
        self.setup_buttons()
        self.tabWidget.tabBar().setVisible(False)

##################################
######## UI CHanges Methods ######

    def Open_Home(self):
        self.tabWidget.setCurrentIndex(0)

    def Open_Download(self):
        self.tabWidget.setCurrentIndex(1)

    def Open_Youtube_video(self):
        self.tabWidget.setCurrentIndex(2)

    def Open_Youtube_list(self):
        self.tabWidget.setCurrentIndex(3)

    def Open_History(self):
        self.tabWidget.setCurrentIndex(4)


    ###################All Buttons ######################
    def setup_buttons(self):
        self.pushButton.clicked.connect(self.download_file)
        self.pushButton_3.clicked.connect(self.Open_Home)
        self.pushButton_4.clicked.connect(self.Open_Download)
        self.pushButton_5.clicked.connect(self.Open_Youtube_video)
        self.pushButton_14.clicked.connect(self.Open_Youtube_list)
        self.pushButton_2.clicked.connect(self.setup_browse_file)
        self.pushButton_6.clicked.connect(self.download_yt_video)
        self.pushButton_12.clicked.connect(self.download_yt_playlist)
        self.pushButton_7.clicked.connect(self.setup_browse_forVideo)
        self.pushButton_13.clicked.connect(self.setup_browse_forList)
        self.pushButton_8.clicked.connect(self.get_video_data)
        self.pushButton_9.clicked.connect(self.get_plist_data)
        self.pushButton_10.clicked.connect(self.Open_History)

    ########## Downloading a video from youtube:#########
    def download_file(self):
        url = self.lineEdit.text()
        location = self.lineEdit_2.text()
        if url == '' or location == '':
            QMessageBox.warning(self, 'Error', 'Enter a valid URL and Location ...!!')
        else:
            try:
                urllib.request.urlretrieve(url, location, self.setup_progress_bar)
            except Exception:
                QMessageBox.warning(self, 'Download Error', 'The Download Failed')
                return
            QMessageBox.information(self, 'Download Completed', 'The Download Completed Successfully')
            self.lineEdit.setText('')
            self.lineEdit_2.setText('')
            self.progressBar.setValue(0)

    def setup_browse_file(self):
        location = QFileDialog.getExistingDirectory(self, 'Choose location')
        self.lineEdit_2.setText(location)

    def setup_progress_bar(self, blocknum, blocksize, totalsize):
        red = blocknum * blocksize
        if totalsize > 0:
            percent = red * 100 / totalsize
            self.progressBar.setValue(percent)
            QApplication.processEvents()

    ########## Downloading a video from youtube:#########
    def get_video_data(self):
        url = self.lineEdit_4.text()
        if url == '':
            QMessageBox.warning(self, 'Error', 'Enter a valid URL ... !!')
        else:
            vid = YouTube(url)
            data = vid.title
            self.textEdit_2.setPlainText(data)

    def download_yt_video(self):
        url = self.lineEdit_4.text()
        location = self.lineEdit_3.text()
        if url == '' or location == '':
            QMessageBox.warning(self, 'Error', 'Enter a valid URL and Location ... !!')
        else:
            vid = YouTube(url)

            try:
                vid.streams.get_highest_resolution().download(output_path=location)
            except Exception:
                QMessageBox.warning(self, 'Download Error', 'The Download Failed')
                return
            QMessageBox.information(self, 'Download Completed', 'The Download Completed Successfully')

            self.lineEdit_4.setText('')
            self.lineEdit_3.setText('')
            self.textEdit_2.setPlainText('')
            self.progressBar.setValue(0)

    def setup_browse_forVideo(self):
        location = QFileDialog.getExistingDirectory(self, 'Choose location')
        self.lineEdit_3.setText(location)

    ########## Downloading a video from youtube:#########
    def get_plist_data(self):
        url = self.lineEdit_10.text()
        if url == '':
            QMessageBox.warning(self, 'Error', 'Enter a valid URL ... !!')
        else:
            plist = Playlist(url)
            data = plist.title
            self.textEdit.setPlainText(data)

    def download_yt_playlist(self):
        url = self.lineEdit_10.text()
        location = self.lineEdit_9.text()
        if url == '' or location == '':
            QMessageBox.warning(self, 'Error', 'Enter a valid URL and Location ... !!')
        else:
            plist = Playlist(url)
            try:
                for video in plist.videos:
                    video.streams.get_highest_resolution().download(output_path=location)
            except Exception:
                QMessageBox.warning(self, 'Download Error', 'The Download Failed')
                return
            QMessageBox.information(self, 'Download Completed', 'The Play-List Videos completely Downloaded')
            self.lineEdit_10.setText('')
            self.lineEdit_9.setText('')
            self.textEdit.setPlainText('')
            self.progressBar.setValue(0)

    def setup_browse_forList(self):
        location = QFileDialog.getExistingDirectory(self, 'Choose Location ')
        self.lineEdit_9.setText(location)


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
