#!/bin/python3

from feedparser import parse
from feedparse import loadURLs,addFeed,removeFeed
from PyQt5.QtWidgets import QMainWindow,QAction,qApp,QApplication,QInputDialog, QLabel, QComboBox, QWidget, QMessageBox
from PyQt5.QtGui import QIcon
import sys


class FeedGUI(QMainWindow):
    def __init__(self,):
        QMainWindow.__init__(self)
        self.feeds = {}
        self.urls = loadURLs()
        try:
            self.currentFeedName = list(self.urls.keys())[0]
            self.currentFeed = parse(self.urls[self.currentFeedName])
        except IndexError:
            self.currentFeedName = "BBC News"
            self.currentFeed = parse("http://feeds.bbci.co.uk/news/rss.xml")
        self.feeds[self.currentFeedName] = self.currentFeed
        self.initUI()

    ## Accessors
    def getCurrentFeed(self):
        return self.currentFeed

    def setCurrentFeed(self, feed):
        self.currentFeedName = feed
        try:
            self.currentFeed = self.feeds[feed]
        except KeyError:
            self.currentFeed = parse(self.urls[feed])
        self.updateLabels()


    def initUI(self):
        self.genLabels(10)
        self.updateLabels()

        combo = QComboBox(self)
        self.combo = combo
        for feedName in self.urls.keys():
            combo.addItem(feedName)
        combo.activated[str].connect(self.onActivated)
        combo.move(15,35)
        combo.adjustSize()

        newFeedAction = QAction(QIcon("exit.png"),"&New Feed", self)
        newFeedAction.triggered.connect(self.newFeed)
        remFeedAction = QAction(QIcon("exit.png"),"&Delete Feed", self)
        remFeedAction.triggered.connect(self.removeFeed)
        menubar = self.menuBar()
        editMenu = menubar.addMenu("&Edit")
        editMenu.addAction(newFeedAction)
        editMenu.addAction(remFeedAction)


        self.setGeometry(200,200,600,280)
        self.setWindowTitle("Nick's RSS Feed Aggregator")
        self.show()

    def onActivated(self,text):
        self.setCurrentFeed(text)

    def genLabels(self, number):
        self.labels = []
        lblx, lbly = 15, 70
        for entry in range(number):
            self.labels.append(QLabel("",self))
            self.labels[-1].move(lblx,lbly)
            self.labels[-1].adjustSize()
            lbly += 20

    def updateLabels(self):
        feed = self.getCurrentFeed()
        for i in range(len(self.labels)):
            try:
                entry = feed['entries'][i]
                link = entry['links'][0]['href']
                if link[-1] == "/":
                    link = link[:-1]
                text = entry['title'] + " (<a href=" + link + ">Link</a>)"
                self.labels[i].setText(text)
                self.labels[i].setOpenExternalLinks(True)
                self.labels[i].adjustSize()
            except IndexError:
                self.labels[i].setText("ERROR: COULD NOT FIND ARTICLE")
                self.labels[i].adjustSize()

    def removeFeed(self):
        feed = self.getCurrentFeed()
        confirm = QMessageBox.question(self, "Confirm", "Really delete {}?".format(self.currentFeedName))
        if confirm == QMessageBox.Yes:
           removeFeed(self.currentFeedName) 
        QMessageBox.information(self,"Deletion complete","Please note: feed will not be removed until the program is restarted.")

    def newFeed(self):
        url, ok = QInputDialog.getText(self,"Add New Feed","Enter an RSS URL")
        if not ok:
            return
        nick, ok = QInputDialog.getText(self,"Add New Feed",
                                             "Enter a nickname for this feed")

        if ok:
            addFeed(url,nick)
            feed = parse(url)
            self.feeds[nick] = feed
            self.combo.addItem(nick)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = FeedGUI()
    sys.exit(app.exec_())
