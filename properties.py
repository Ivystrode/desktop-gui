# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'properties.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

# ADD NEW TABLE WINDOW TO SHOW AVERAGE PRICE PER AREA OVER EACH DAY
# EACH COLUMN IS A DATE
# EACH ROW IS A CITY/AREA
# AVERAGE PRICES IN THE COLUMNS
# WILL NEED TO MAKE NEW TABLE IN DB FOR AVERAGE PRICES


from PyQt5 import QtCore, QtGui, QtWidgets
from datetime import datetime
from scripts import zoopla_scraper, otm_scraper
from scripts import storage

# from main import Ui_MainWindow
import main
import sys



class Ui_PropertyWindow(object):

    # def __init__(self):
    #     app = QtWidgets.QApplication(sys.argv)
    #     MainWindow = QtWidgets.QMainWindow()
    #     ui = Ui_PropertyWindow()
    #     # ui.setupUi(MainWindow)
    #     # MainWindow.show()
    #     # sys.exit(app.exec_())


    def populate_table(self, city):
        print("put the city in the table widget")

    def slider_value(self):
        value = self.search_radius_slider.value()
        self.search_radius_label.setText("Search Radius: " + str(value))

    def scan(self):
        # ADD OTM SCRAPER N
        self.scan_progress_bar.setProperty("value", 0)
        step_increment = 100 / int(zoopla_scraper.numpages)
        step = 0

        self.scan_results_label.setText("Scanning...")
        city = self.city_town_scan_input.text()
        radius = self.search_radius_slider.value()

        print("Scanning for new properties")
        print(str(city))
        print(str(radius))

        self.scan_progress_bar.setProperty("value", step)
        step = step + step_increment
        self.scan_progress_bar.setProperty("value", step)
        zoo_props_saved, zoo_props_exist, zoo_avprice = zoopla_scraper.scanner(city, radius)
        otm_props_saved, otm_props_exist, otm_avprice = otm_scraper.scanner(city, radius)
        print("scan complete")

        tot_props_saved = zoo_props_saved + otm_props_saved
        tot_props_exist = zoo_props_exist + otm_props_exist
        av_avprice = (zoo_avprice + otm_avprice) / 2

        print(zoo_avprice)
        print(otm_avprice)

        print("Now storing to averages database...")
        datecollected = datetime.now().strftime("%Y-%m-%d_%H:%M")
        storage.store_property_data(city, av_avprice, datecollected)

        results = f"{city.upper()}: {tot_props_saved} new properties saved. {tot_props_exist} already in database. Average price: {av_avprice}"

        self.scan_results_label.setText(str(results))

    def search(self):
        self.property_table.setRowCount(0)
        self.scan_progress_bar.setProperty("value", 0)
        city = self.db_search_input.text()
        step = 10
        print(f"Fetching {city} from DB")
        properties = storage.view_properties(city)
        if properties == 'not found':
            step=100
            self.scan_results_label.setText(f"{city.upper()} not found in database")
        else:
            step_increment = (100 / len(properties))
            step = step + step_increment
            self.scan_results_label.setText(f"{city.upper()}: {len(properties)} properties found in database")
            self.property_title_2.setText(f"CITY: {city.upper()} - {len(properties)} PROPERTIES")
            for p in properties:
                print(p)
                print(f"adding {p[3]} to table")
                self.addTableRow(self.property_table, p)
                step = step + step_increment
                self.scan_progress_bar.setProperty("value", step)

    def addTableRow(self, table, row_data):
        row = table.rowCount()
        table.setRowCount(row+1)
        col = 0
        for item in row_data[1:]: # exclude ID, no need to display
            cell = QtWidgets.QTableWidgetItem(str(item))
            table.setItem(row, col, cell)
            col += 1





    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Property Data Collector")
        MainWindow.resize(826, 554)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.property_title = QtWidgets.QLabel(self.centralwidget)
        self.property_title.setGeometry(QtCore.QRect(690, 0, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)

        self.property_title.setFont(font)
        self.property_title.setAlignment(QtCore.Qt.AlignCenter)
        self.property_title.setObjectName("property_title")

        self.db_search_button = QtWidgets.QPushButton(self.centralwidget)
        self.db_search_button.setGeometry(QtCore.QRect(710, 120, 75, 23))
        self.db_search_button.setObjectName("db_search_button")
        self.db_search_button.clicked.connect(self.search)

        self.property_table = QtWidgets.QTableWidget(self.centralwidget)
        self.property_table.setGeometry(QtCore.QRect(0, 50, 661, 401))
        self.property_table.setToolTipDuration(0)
        self.property_table.setShowGrid(True)
        self.property_table.setRowCount(0)
        self.property_table.setColumnCount(10)
        self.property_table.setObjectName("property_table")
        self.property_table.setHorizontalHeaderLabels(["Date listed", "Price", "Address", "Bedrooms", "Bathrooms","Reception rooms","Agent name","Agent Tel","Website","Fetched at"])
        # self.property_table.resizeColumnsToContents()


        self.db_search_input = QtWidgets.QLineEdit(self.centralwidget)
        self.db_search_input.setGeometry(QtCore.QRect(670, 80, 151, 31))
        self.db_search_input.setObjectName("db_search_input")

        self.db_search_label = QtWidgets.QLabel(self.centralwidget)
        self.db_search_label.setGeometry(QtCore.QRect(670, 49, 151, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.db_search_label.setFont(font)
        self.db_search_label.setAlignment(QtCore.Qt.AlignCenter)
        self.db_search_label.setObjectName("db_search_label")

        self.scan_properties_label = QtWidgets.QLabel(self.centralwidget)
        self.scan_properties_label.setGeometry(QtCore.QRect(670, 170, 151, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.scan_properties_label.setFont(font)
        self.scan_properties_label.setAlignment(QtCore.Qt.AlignCenter)
        self.scan_properties_label.setObjectName("scan_properties_label")

        self.city_town_scan_input = QtWidgets.QLineEdit(self.centralwidget)
        self.city_town_scan_input.setGeometry(QtCore.QRect(670, 230, 151, 31))
        self.city_town_scan_input.setObjectName("city_town_scan_input")

        self.city_town_label = QtWidgets.QLabel(self.centralwidget)
        self.city_town_label.setGeometry(QtCore.QRect(670, 200, 151, 31))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.city_town_label.setFont(font)
        self.city_town_label.setAlignment(QtCore.Qt.AlignCenter)
        self.city_town_label.setObjectName("city_town_label")

        self.search_radius_label = QtWidgets.QLabel(self.centralwidget)
        self.search_radius_label.setGeometry(QtCore.QRect(670, 260, 151, 41))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.search_radius_label.setFont(font)
        self.search_radius_label.setAlignment(QtCore.Qt.AlignCenter)
        self.search_radius_label.setObjectName("search_radius_label")

        self.scan_new_properties_button = QtWidgets.QPushButton(self.centralwidget)
        self.scan_new_properties_button.setGeometry(QtCore.QRect(710, 320, 75, 23))
        self.scan_new_properties_button.setObjectName("scan_new_properties_button")
        self.scan_new_properties_button.clicked.connect(self.scan)

        self.search_radius_slider = QtWidgets.QSlider(self.centralwidget)
        self.search_radius_slider.setGeometry(QtCore.QRect(670, 290, 141, 22))
        self.search_radius_slider.setOrientation(QtCore.Qt.Horizontal)
        self.search_radius_slider.setObjectName("search_radius_slider")
        self.search_radius_slider.setMinimum(1)
        self.search_radius_slider.setMaximum(40)
        self.search_radius_slider.setValue(1)
        self.search_radius_slider.setSingleStep(5)
        self.search_radius_slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.search_radius_slider.setTickInterval(5)
        self.search_radius_slider.valueChanged.connect(self.slider_value)

        self.scan_progress_bar = QtWidgets.QProgressBar(self.centralwidget)
        self.scan_progress_bar.setEnabled(True)
        self.scan_progress_bar.setGeometry(QtCore.QRect(670, 360, 151, 23))
        self.scan_progress_bar.setProperty("value", 0)
        self.scan_progress_bar.setTextVisible(False)
        self.scan_progress_bar.setOrientation(QtCore.Qt.Horizontal)
        self.scan_progress_bar.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.scan_progress_bar.setObjectName("scan_progress_bar")

        self.property_title_2 = QtWidgets.QLabel(self.centralwidget)
        self.property_title_2.setGeometry(QtCore.QRect(0, 0, 251, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.property_title_2.setFont(font)
        self.property_title_2.setAlignment(QtCore.Qt.AlignCenter)
        self.property_title_2.setObjectName("property_title_2")

        self.scan_results_label = QtWidgets.QLabel(self.centralwidget)
        self.scan_results_label.setGeometry(QtCore.QRect(670, 390, 151, 61))
        self.scan_results_label.setText("")
        self.scan_results_label.setObjectName("scan_results_label")
        self.scan_results_label.setWordWrap(True)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 826, 21))
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        self.menuPrograms = QtWidgets.QMenu(self.menubar)
        self.menuPrograms.setObjectName("menuPrograms")
        self.menuAPI = QtWidgets.QMenu(self.menubar)
        self.menuAPI.setObjectName("menuAPI")
        self.menuComputer = QtWidgets.QMenu(self.menubar)
        self.menuComputer.setObjectName("menuComputer")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.actionMain = QtWidgets.QAction(MainWindow)
        self.actionMain.setObjectName("actionMain")
        self.actionMain.triggered.connect(self.toMainMenu)

        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")

        self.actionNews_Scraper = QtWidgets.QAction(MainWindow)
        self.actionNews_Scraper.setObjectName("actionNews_Scraper")
        self.actionProperty_Data = QtWidgets.QAction(MainWindow)
        self.actionProperty_Data.setObjectName("actionProperty_Data")
        self.actionPolscraper = QtWidgets.QAction(MainWindow)
        self.actionPolscraper.setObjectName("actionPolscraper")
        self.actionDarkSky_Weather = QtWidgets.QAction(MainWindow)
        self.actionDarkSky_Weather.setObjectName("actionDarkSky_Weather")
        self.actionLocal_Information = QtWidgets.QAction(MainWindow)
        self.actionLocal_Information.setObjectName("actionLocal_Information")
        self.actionLock = QtWidgets.QAction(MainWindow)
        self.actionLock.setObjectName("actionLock")
        self.menuMenu.addAction(self.actionMain)
        self.menuMenu.addAction(self.actionExit)
        self.menuPrograms.addAction(self.actionNews_Scraper)
        self.menuPrograms.addAction(self.actionProperty_Data)
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
        MainWindow.setWindowTitle(_translate("MainWindow", "Property Data Collector"))
        self.property_title.setText(_translate("MainWindow", "PROPERTY DATA"))
        self.db_search_button.setText(_translate("MainWindow", "Search"))
        self.db_search_label.setText(_translate("MainWindow", "Search the DB for a city"))
        self.scan_properties_label.setText(_translate("MainWindow", "Scan for new properties"))
        self.city_town_label.setText(_translate("MainWindow", "City/Town"))
        self.search_radius_label.setText(_translate("MainWindow", "Search Radius"))
        self.scan_new_properties_button.setText(_translate("MainWindow", "Scan"))
        self.scan_progress_bar.setFormat(_translate("MainWindow", "%p%"))
        self.property_title_2.setText(_translate("MainWindow", "CITY: "))
        self.menuMenu.setTitle(_translate("MainWindow", "Menu"))
        self.menuPrograms.setTitle(_translate("MainWindow", "Programs"))
        self.menuAPI.setTitle(_translate("MainWindow", "API"))
        self.menuComputer.setTitle(_translate("MainWindow", "Computer"))
        self.actionMain.setText(_translate("MainWindow", "Main Menu"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionNews_Scraper.setText(_translate("MainWindow", "News Scraper"))
        self.actionProperty_Data.setText(_translate("MainWindow", "Property Data"))
        self.actionPolscraper.setText(_translate("MainWindow", "Polscraper"))
        self.actionDarkSky_Weather.setText(_translate("MainWindow", "DarkSky Weather"))
        self.actionLocal_Information.setText(_translate("MainWindow", "Local Information"))
        self.actionLock.setText(_translate("MainWindow", "Lock"))

    def toMainMenu(self):
        print("to main menu")
        self.main_menu=QtWidgets.QMainWindow()
        self.ui = main.Ui_MainWindow()
        self.ui.setupUi(self.main_menu)
        MainWindow.destroy()
        self.main_menu.show()

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_PropertyWindow()
ui.setupUi(MainWindow)

# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     ui = Ui_PropertyWindow()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())
