import sys
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QLineEdit, QAction, QShortcut, QProgressBar, QTabWidget, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView

class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.remove_tab)

    def add_tab(self, url):
        web_view = QWebEngineView()
        web_view.load(QUrl(url))
        index = self.addTab(web_view, "New Tab")
        self.setCurrentIndex(index)

    def remove_tab(self, index):
        widget = self.widget(index)
        widget.deleteLater()
        self.removeTab(index)

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tabs = TabWidget()
        self.setCentralWidget(self.tabs)

        toolbar = QToolBar()
        self.addToolBar(toolbar)
        new_tab_action = QAction("New Tab", self)
        new_tab_action.triggered.connect(self.new_tab)
        toolbar.addAction(new_tab_action)

        back_action = QAction("Back", self)
        back_action.triggered.connect(self.go_back)
        toolbar.addAction(back_action)

        forward_action = QAction("Forward", self)
        forward_action.triggered.connect(self.go_forward)
        toolbar.addAction(forward_action)

        reload_action = QAction("Reload", self)
        reload_action.triggered.connect(self.reload_page)
        toolbar.addAction(reload_action)

        self.address_bar = QLineEdit()
        self.address_bar.returnPressed.connect(self.load_page)
        toolbar.addWidget(self.address_bar)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumWidth(120)
        toolbar.addWidget(self.progress_bar)

        back_shortcut = QShortcut(QKeySequence(Qt.Key_Backspace), self)
        back_shortcut.activated.connect(self.go_back)

        reload_shortcut = QShortcut(QKeySequence(Qt.Key_F5), self)
        reload_shortcut.activated.connect(self.reload_page)

        self.new_tab()

    def new_tab(self):
        self.tabs.add_tab("https://www.google.com")

    def load_page(self):
        url = QUrl(self.address_bar.text())
        index = self.tabs.currentIndex()
        web_view = self.tabs.widget(index)
        web_view.load(url)

    def go_back(self):
        web_view = self.tabs.currentWidget()
        web_view.back()

    def go_forward(self):
        web_view = self.tabs.currentWidget()
        web_view.forward()

    def reload_page(self):
        web_view = self.tabs.currentWidget()
        web_view.reload()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BrowserWindow()
    window.show()
    sys.exit(app.exec_())
