# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'properties.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.



from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal
from datetime import datetime
from scripts import zoopla_scraper, otm_scraper
from scripts import storage

from plyer import notification

# from main import Ui_MainWindow
import main, prop_av_table, prop_av_graph
import sys
import time
import webbrowser
from datetime import datetime

scanning_active = False


class ScraperThread(QThread):
    scraper_signal = pyqtSignal("PyQt_PyObject", "PyQt_PyObject", "PyQt_PyObject", "PyQt_PyObject", "PyQt_PyObject", "PyQt_PyObject", "PyQt_PyObject", "PyQt_PyObject", "PyQt_PyObject", )

    def __init__(self, city, radius):
        QThread.__init__(self)
        self.city = city
        self.radius = radius

    def run(self):       
        zoo_props_saved, zoo_props_exist, zoo_avprice, zoo_avbeds = zoopla_scraper.scanner(self.city, self.radius)
        otm_props_saved, otm_props_exist, otm_avprice, otm_avbeds = otm_scraper.scanner(self.city, self.radius)
        
        # try:
        #     zoo_props_saved, zoo_props_exist, zoo_avprice, zoo_avbeds = zoopla_scraper.scanner(self.city, self.radius)
        #     print("zoopla scraper run")
        # except:
        #     zoo_props_saved, zoo_props_exist, zoo_avprice, zoo_avbeds = 0, 0, 0, 0
        #     print("zoopla scraper NOT RUN")
        
        # try:
        #     otm_props_saved, otm_props_exist, otm_avprice, otm_avbeds = otm_scraper.scanner(self.city, self.radius)
        #     print("OTM scraper run")
        # except:
        #     otm_props_saved, otm_props_exist, otm_avprice, otm_avbeds = 0, 0, 0, 0
        #     print("omt SCRAPER not run")
            
        self.scraper_signal.emit(self.city, zoo_props_saved, zoo_props_exist, zoo_avprice, zoo_avbeds, otm_props_saved, otm_props_exist, otm_avprice, otm_avbeds)
        



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

    def interval_scan(self, intervals, cities_to_scan):
        global scanning_active
        scanning_active = False
        """
        This function is only an example for now. Will be implemented later for regular periodic scanning.
        Must make sure to use this function as a separate thread...
        """

        # THE ARGUMENTS RECEIVED MUST BE LIKE THIS:
        # intervals = {
        #     '3_per_day':['08:00:00', '16:00:00', '23:59:00'],
        #     '2_per_day':['09:00:00','21:00:00'],
        #     '1_per_day':['12:00:00']
        # }

        # cities_to_scan = []

        while scanning_active == True:
            current_time = datetime.now().strftime("%H:%M:%S")
            if str(current_time) in  intervals['3_per_day']:
                print("it is now THAT time!!!" + str(current_time))
                time.sleep(1)



    def scan(self):
        global scanning_active
        self.scan_progress_bar.setProperty("value", 0)
        step_increment = 100 / int(zoopla_scraper.numpages)
        step = 0
        accepted_radii = [1, 3, 5, 10, 15, 20, 30, 40]

        self.scan_results_label.setText("Scanning...")
        city = self.city_town_scan_input.text()
        radius = self.search_radius_slider.value()

        print("Scanning for new properties")
        print(str(city))
        print(str(radius))

        self.scan_progress_bar.setProperty("value", step)
        step = step + step_increment
        self.scan_progress_bar.setProperty("value", step)

        if radius in accepted_radii:

            try:
                self.scan_thread = ScraperThread(city, radius)
                self.scan_thread.scraper_signal.connect(self.scan_complete)
                self.scan_thread.start()
                self.scan_new_properties_button.setEnabled(False)
                scanning_active = True

            except Exception as error:
                result = error
                self.scan_results_label.setText(str(result))
                notification.notify(title= "Python Control Panel", message= f"Property Scanner Error: {str(result)}")

        else:
            self.scan_results_label.setText("Please enter a radius of 1, 3, 5, 10, 15, 20, 30 or 40")

    def scan_complete(self, city, zoo_props_saved, zoo_props_exist, zoo_avprice, zoo_avbeds, otm_props_saved, otm_props_exist, otm_avprice, otm_avbeds):
        global scanning_active
        scanning_active = False
        tot_props_saved = zoo_props_saved + otm_props_saved
        tot_props_exist = zoo_props_exist + otm_props_exist
        av_avprice = (zoo_avprice + otm_avprice) / 2            
        av_avbeds = (zoo_avbeds + otm_avbeds) / 2

        # if otm_avprice > 0 and zoo_avprice > 0:
        #     tot_props_saved = zoo_props_saved + otm_props_saved
        #     tot_props_exist = zoo_props_exist + otm_props_exist
        #     av_avprice = (zoo_avprice + otm_avprice) / 2            
        #     av_avbeds = (zoo_avbeds + otm_avbeds) / 2
        #     print("got both")
            
        # elif otm_avprice == 0 and zoo_avprice > 0:
        #     tot_props_saved = zoo_props_saved
        #     tot_props_exist = zoo_props_exist
        #     av_avprice = zoo_avprice            
        #     av_avbeds = zoo_avbeds
        #     print("only zoopla data")
            
        # elif otm_avprice > 0 and zoo_avprice == 0:
        #     tot_props_saved = otm_props_saved
        #     tot_props_exist = otm_props_exist
        #     av_avprice = otm_avprice            
        #     av_avbeds = otm_avbeds
        #     print("only otm data")
            
        # else:
        #     print("FATAL PROPERTY SCRAPER ERROR - AVERAGES NOT SAVED\n"*50)

        print(zoo_avprice)
        print(otm_avprice)

        print("Now storing to averages database...")
        self.scan_results_label.setText("Saving to database...")
        
        datecollected = datetime.now().strftime("%Y-%m-%d_%H:%M")
        storage.store_property_data(city, datecollected, av_avprice, round(av_avbeds, 1), (tot_props_exist + tot_props_saved))
        print("avbeds: " + str(zoo_avbeds) + " otm: " + str(otm_avbeds))
        results = f"{city.upper()}: {tot_props_saved} new properties saved. {tot_props_exist} already in database. Average price: {av_avprice}"

        self.scan_results_label.setText(str(results))
        time.sleep(1)
        self.scan_progress_bar.setProperty("value", 0)

        self.scan_new_properties_button.setEnabled(True)

        # if not interval scan?
        notification.notify(title="Python Control Panel", message=f"{city[0].upper()}{city[1:].lower()} scan completed. {tot_props_saved} new properties added to database")

        

    def search(self):
        # wondering why event loop error? because it asks for user input i think
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
                # print(p)
                # print(f"adding {p[3]} to table")
                self.addTableRow(self.property_table, p)
                step = step + step_increment
                self.scan_progress_bar.setProperty("value", step)
        time.sleep(1)
        self.scan_progress_bar.setProperty("value", 0)

    def addTableRow(self, table, row_data):
        row = table.rowCount()
        table.setRowCount(row+1)
        col = 0
        # print("row data")
        # print(row_data)
        for item in row_data[1:]: # exclude ID, no need to display
            # print("item")
            # print(item)
            cell = QtWidgets.QTableWidgetItem(str(item))
            table.setItem(row, col, cell)
            col += 1
            
    def goto_property(self, property_link):
        print("goto property " + str(property_link))
        webbrowser.open(property_link)
        


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
        self.property_table.setColumnCount(11)
        self.property_table.setObjectName("property_table")
        self.property_table.setHorizontalHeaderLabels(["Date listed", "Price", "Address", "Bedrooms", "Bathrooms","Reception rooms","Agent name","Agent Tel","Website","Fetched at", "Link"])
        self.property_table.setSortingEnabled(True)
        self.property_table.itemDoubleClicked.connect(lambda: self.goto_property(self.property_table.item(self.property_table.currentRow(), 10).text()))
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
        self.menuProperty_Data = QtWidgets.QMenu(self.menuPrograms)
        self.menuProperty_Data.setObjectName("menuProperty_Data")

        # self.menuAPI = QtWidgets.QMenu(self.menubar)
        # self.menuAPI.setObjectName("menuAPI")
        # self.menuComputer = QtWidgets.QMenu(self.menubar)
        # self.menuComputer.setObjectName("menuComputer")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.actionMain = QtWidgets.QAction(MainWindow)
        self.actionMain.setObjectName("actionMain")
        self.actionMain.triggered.connect(self.toMainMenu)

        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionExit.triggered.connect(self.exit_program)

        # self.actionNews_Scraper = QtWidgets.QAction(MainWindow)
        # self.actionNews_Scraper.setObjectName("actionNews_Scraper")
        # self.actionPolscraper = QtWidgets.QAction(MainWindow)
        # self.actionPolscraper.setObjectName("actionPolscraper")
        # self.actionDarkSky_Weather = QtWidgets.QAction(MainWindow)
        # self.actionDarkSky_Weather.setObjectName("actionDarkSky_Weather")
        # self.actionLocal_Information = QtWidgets.QAction(MainWindow)
        # self.actionLocal_Information.setObjectName("actionLocal_Information")
        # self.actionLock = QtWidgets.QAction(MainWindow)
        # self.actionLock.setObjectName("actionLock")

        # self.actionProperty_Data = QtWidgets.QAction(MainWindow)
        # self.actionProperty_Data.setObjectName("actionProperty_Data")
        self.actionPrice_Display = QtWidgets.QAction(MainWindow)
        self.actionPrice_Display.setObjectName("actionPrice_Display")
        self.actionPrice_Display.triggered.connect(self.toPriceDisplay)

        self.actionPrice_Data = QtWidgets.QAction(MainWindow)
        self.actionPrice_Data.setObjectName("actionPrice_Data")
        self.actionPrice_Data.triggered.connect(self.toPriceData)


        self.menuMenu.addAction(self.actionMain)
        self.menuMenu.addAction(self.actionExit)

        # self.menuPrograms.addAction(self.actionNews_Scraper)

        # self.menuPrograms.addAction(self.menuProperty_Data.menuAction())
        # self.menuProperty_Data.addAction(self.actionProperty_Data)
        self.menuPrograms.addAction(self.actionPrice_Display)
        self.menuPrograms.addAction(self.actionPrice_Data)
        # self.menuPrograms.addAction(self.actionPolscraper)
        # self.menuAPI.addAction(self.actionDarkSky_Weather)
        # self.menuAPI.addAction(self.actionLocal_Information)
        # self.menuComputer.addAction(self.actionLock)
        self.menubar.addAction(self.menuMenu.menuAction())
        self.menubar.addAction(self.menuPrograms.menuAction())
        # self.menubar.addAction(self.menuAPI.menuAction())
        # self.menubar.addAction(self.menuComputer.menuAction())

        

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Property Dashboard"))
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
        self.menuPrograms.setTitle(_translate("MainWindow", "Property"))

        # self.menuAPI.setTitle(_translate("MainWindow", "API"))
        # self.menuComputer.setTitle(_translate("MainWindow", "Computer"))

        self.actionMain.setText(_translate("MainWindow", "Main Menu"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))

        # self.actionNews_Scraper.setText(_translate("MainWindow", "News Scraper"))

        self.menuProperty_Data.setTitle(_translate("MainWindow", "Property Data"))

        # self.actionPolscraper.setText(_translate("MainWindow", "Polscraper"))
        # self.actionDarkSky_Weather.setText(_translate("MainWindow", "DarkSky Weather"))
        # self.actionLocal_Information.setText(_translate("MainWindow", "Local Information"))
        # self.actionLock.setText(_translate("MainWindow", "Lock"))

        # self.actionProperty_Data.setText(_translate("MainWindow", "Property Main"))
        self.actionPrice_Display.setText(_translate("MainWindow", "Price Display"))
        self.actionPrice_Data.setText(_translate("MainWindow", "Price Data"))


    def toMainMenu(self):
        print("to main menu")
        self.main_menu=QtWidgets.QMainWindow()
        self.ui = main.Ui_MainWindow()
        self.ui.setupUi(self.main_menu)
        MainWindow.destroy()
        self.main_menu.show()
    def toPriceData(self):
        print("to price data")
        self.price_data=QtWidgets.QMainWindow()
        self.ui = prop_av_table.Ui_TableWindow()
        self.ui.setupUi(self.price_data)
        MainWindow.destroy()
        self.price_data.show()
    def toPriceDisplay(self):
        print("to price data")
        self.price_display=QtWidgets.QMainWindow()
        self.ui = prop_av_graph.Ui_GraphWindow()
        self.ui.setupUi(self.price_display)
        MainWindow.destroy()
        self.price_display.show()
    def exit_program(self):
        cfm = QMessageBox()
        cfm.setWindowTitle("Close PCP?")
        cfm.setText("Confirm if you want to close the Python Control Panel")
        cfm.setIcon(QMessageBox.Information)
        cfm.setStandardButtons(QMessageBox.Close | QMessageBox.Cancel)
        cfm.setDefaultButton(QMessageBox.Cancel)

        cfm.buttonClicked.connect(self.closeprogram)
        x = cfm.exec_()

    def closeprogram(self, i):
        order = i.text()
        if order == 'Close':
            exit()
        else:
            print(i.text())

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
