# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'property_avprice_table.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from scripts import storage


class Ui_MainWindow(object):

    def toMainMenu(self):
        print("to main menu")
        self.main_menu=QtWidgets.QMainWindow()
        self.ui = main.Ui_MainWindow()
        self.ui.setupUi(self.main_menu)
        MainWindow.destroy()
        self.main_menu.show()

    def populate_table(self):        
        self.data_table.setRowCount(0)
        # self.scan_progress_bar.setProperty("value", 0)
        city = self.citylist.currentText()
        # step = 10
        print(f"Fetching {city} from DB")
        # properties = storage.view_properties(city)
        data = storage.view_property_data(city)
        print(data)
        if data == 'not found':
            step=100
            self.title.setText(f"{city.upper()} not found in database")
        else:
            self.title.setText(f"Property Trend Data: {city.upper()}")
            row = self.data_table.rowCount()
            self.data_table.setRowCount(row+1)
            col = 0
            for tuple_object in data:
                self.addTableRow(self.data_table, tuple_object)

    def addTableRow(self, table, row_data):
        row = table.rowCount()
        table.setRowCount(row+1)
        col = 0
        for item in row_data[1:]: # exclude ID, no need to display
            cell = QtWidgets.QTableWidgetItem(str(item))
            table.setItem(row, col, cell)
            col += 1
    
    def get_cities(self):
        return storage.get_all_cities()




    def setupUi(self, MainWindow):

        MainWindow.setObjectName("Mean Data Tables")
        MainWindow.resize(826, 554)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        cities = self.get_cities()
        self.citylist = QtWidgets.QComboBox(self.centralwidget)
        self.citylist.setGeometry(QtCore.QRect(560, 60, 181, 31))
        self.citylist.setObjectName("citylist")
        for city in cities:
            self.citylist.addItem(city)
        self.citylist.activated.connect(self.populate_table)

        self.city_select = QtWidgets.QLabel(self.centralwidget)
        self.city_select.setGeometry(QtCore.QRect(560, 30, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.city_select.setFont(font)
        self.city_select.setAlignment(QtCore.Qt.AlignCenter)
        self.city_select.setObjectName("city_select")

        self.graph_button = QtWidgets.QPushButton(self.centralwidget)
        self.graph_button.setGeometry(QtCore.QRect(600, 120, 101, 31))
        self.graph_button.setObjectName("graph_button")

        self.title = QtWidgets.QLabel(self.centralwidget)
        self.title.setGeometry(QtCore.QRect(50, 10, 360, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setObjectName("title")

        self.data_table = QtWidgets.QTableWidget(self.centralwidget)
        self.data_table.setGeometry(QtCore.QRect(0, 40, 461, 470))
        self.data_table.setObjectName("data_table")
        self.data_table.setColumnCount(4)
        self.data_table.setRowCount(0)
        self.data_table.setShowGrid(True)
        self.data_table.setHorizontalHeaderLabels(["Date Collected","Average Price","Average Bedrooms","Listings scanned"])

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 826, 21))
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        self.menuPrograms = QtWidgets.QMenu(self.menubar)
        self.menuPrograms.setObjectName("menuPrograms")
        self.menuProperty_Data = QtWidgets.QMenu(self.menuPrograms)
        self.menuProperty_Data.setObjectName("menuProperty_Data")
        self.menuAPI = QtWidgets.QMenu(self.menubar)
        self.menuAPI.setObjectName("menuAPI")
        self.menuComputer = QtWidgets.QMenu(self.menubar)
        self.menuComputer.setObjectName("menuComputer")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionNews_Scraper = QtWidgets.QAction(MainWindow)
        self.actionNews_Scraper.setObjectName("actionNews_Scraper")
        self.actionPolscraper = QtWidgets.QAction(MainWindow)
        self.actionPolscraper.setObjectName("actionPolscraper")
        self.actionDarkSky_Weather = QtWidgets.QAction(MainWindow)
        self.actionDarkSky_Weather.setObjectName("actionDarkSky_Weather")
        self.actionLocal_Information = QtWidgets.QAction(MainWindow)
        self.actionLocal_Information.setObjectName("actionLocal_Information")
        self.actionLock = QtWidgets.QAction(MainWindow)
        self.actionLock.setObjectName("actionLock")
        self.actionPrice_Display = QtWidgets.QAction(MainWindow)
        self.actionPrice_Display.setObjectName("actionPrice_Display")
        self.actionPrice_Data = QtWidgets.QAction(MainWindow)
        self.actionPrice_Data.setObjectName("actionPrice_Data")
        self.menuMenu.addAction(self.actionExit)
        self.menuPrograms.addAction(self.menuProperty_Data.menuAction())
        self.menuProperty_Data.addAction(self.actionPrice_Display)
        self.menuProperty_Data.addAction(self.actionPrice_Data)
        self.menuPrograms.addAction(self.actionNews_Scraper)
        self.menuPrograms.addAction(self.actionPolscraper)
        self.menuAPI.addAction(self.actionDarkSky_Weather)
        self.menuAPI.addAction(self.actionLocal_Information)
        self.menuComputer.addAction(self.actionLock)
        self.menubar.addAction(self.menuMenu.menuAction())
        self.menubar.addAction(self.menuPrograms.menuAction())
        self.menubar.addAction(self.menuAPI.menuAction())
        self.menubar.addAction(self.menuComputer.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Mean Data Tables"))
        self.city_select.setText(_translate("MainWindow", "Select City"))
        self.graph_button.setText(_translate("MainWindow", "View Graph"))
        self.title.setText(_translate("MainWindow", "Property Trend Data - No City"))
        self.menuMenu.setTitle(_translate("MainWindow", "Menu"))
        self.menuPrograms.setTitle(_translate("MainWindow", "Programs"))
        self.menuProperty_Data.setTitle(_translate("MainWindow", "Property Data"))
        self.menuAPI.setTitle(_translate("MainWindow", "API"))
        self.menuComputer.setTitle(_translate("MainWindow", "Computer"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionNews_Scraper.setText(_translate("MainWindow", "News Scraper"))
        self.actionPolscraper.setText(_translate("MainWindow", "Polscraper"))
        self.actionDarkSky_Weather.setText(_translate("MainWindow", "DarkSky Weather"))
        self.actionLocal_Information.setText(_translate("MainWindow", "Local Information"))
        self.actionLock.setText(_translate("MainWindow", "Lock"))
        self.actionPrice_Display.setText(_translate("MainWindow", "Price Display"))
        self.actionPrice_Data.setText(_translate("MainWindow", "Price Data"))


if __name__ == "__main__":
    print("we're in")
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())