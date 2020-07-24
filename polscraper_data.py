# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'polscraper_data.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import os, glob, sys, re
import json
import numpy as np
import random
from datetime import datetime, timedelta
from heapq import nlargest

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtChart import QChart, QChartView, QValueAxis, QBarCategoryAxis, QBarSet, QBarSeries
from PyQt5.Qt import Qt
from PyQt5.QtGui import QPainter

import main, polscraper_main


import pyqtgraph as pg



class Ui_DataWindow(object):

    def populate_table_single_report(self):     
        self.dataTable.clear()

        self.dataTable.setRowCount(0)
        self.dataTable.setColumnCount(2)
        self.dataTable.setHorizontalHeaderLabels(["Category", "Frequency"])

        # try:
        reportname = self.a_mainReportList.currentText()
        reportfilename = glob.glob(f"polscraper\\reports\\*{reportname}_pol_sentiment_analysis.json")[0]
                 


        with open(f"{reportfilename}") as report_json_file:
            data = json.load(report_json_file)

        del data[0]['Date']
        del data[0]['Time']

        try:
            self.label.setText("Table displaying: " + str(reportname)  + " Pages scanned: " + str(data[0]['Pages']))
            del data[0]['Pages']
        except:
            self.label.setText("Table displaying: " + str(reportname)) 
            

        # sort data in reverse order
        data = {k: v for k, v in sorted(data[0].items(), key=lambda item: item[1])}

        # sort data in descending numerical order
        reversed_data = {}
        for key, value in reversed(data.items()):
            reversed_data[key] = value

        col = 0

        # turn scores into integers
        for key, value in reversed_data.items():
            value = int(value)

        for pair in reversed_data.items():
            self.addTableRow_singleReport(self.dataTable, pair)

        self.tableTitle.setText(f"{reportname} topic frequency")

        # show in graph
        self.populate_graph_single_report(reversed_data)

        # except Exception as e:
        #     self.label.setText(f"Error: {e}")

    def addTableRow_singleReport(self, table, row_data):
        row = table.rowCount()
        table.setRowCount(row+1)
        col = 0
        for item in row_data: 
            cell = QtWidgets.QTableWidgetItem(str(item))
            table.setItem(row, col, cell)
            col += 1

    def populate_graph_single_report(self, data):
        self.dataGraph.clear()
        print("graph function")
        print(data)

        categories = []
        scores = []

        for key, value in data.items():
            categories.append(key)
            scores.append(int(value))

        # add "Apply Weighting" tickbox and boolean to bottom of window
        # this divides b and j scores by 5 and 3 or 2 so they don't always dwarf
        # everything else

        maxY = nlargest(1, scores)
        print(maxY)

        y1 = range(0, maxY[0])

        x = range(1, len(categories))
        # x = range(1, len(scores))

        bg1= pg.BarGraphItem(x=x, height=scores, width=0.8, brush="b")
        # self.dataGraph = pg.plot(self.centralwidget)
        self.dataGraph.addItem(bg1)

        # self.graphTitle.setText(f"Top 3 topics: {categories[0]}, {categories[1]}, {categories[2]}") disabled for sensitivity
        self.graphTitle.setText(f"Topic frequency visualisation")
        print("graph on display")


    def populate_table_basic_timeframe(self):
        self.dataTable.clear()
        self.tableTitle.setText("Topic Data: " + self.a_mainTimeframeList.currentText())
        print("pop table timeframe")
        current_time = datetime.now()
        timeframe = self.a_mainTimeframeList.currentText()

        if timeframe != "Today":
            timeframe = re.findall('\d+', timeframe)
            timeframe = int(timeframe[0])
        else:
            timeframe = 1


        max_time_diff = current_time - timedelta(days=timeframe)

        # get reports that are within the specified timeframe
        for report in glob.glob(f"polscraper\\reports\\*_pol_sentiment_analysis.json"):
            report_date = datetime.strptime(report[19:35], "%Y-%m-%d-%H-%M")
            if max_time_diff < report_date < current_time:
                print(report)
                print("is within " + str(timeframe) + " days")

        # what needs to happen now is the x axis of table must list all categories
        # the y axis must list all the reports
        # ....don't know what the graph will look like yet
        # maybe the DIFFERENCE between the top topic and the next on the list
        # displayed as a bar chart? or line plot?
        # or total number of posts displayed as a line plot?
        # hmmm...

        self.populate_graph_basic_timeframe()


    def populate_graph_basic_timeframe(self):
        self.dataGraph.clear()
        self.dataGraph = pg.PlotWidget(self.centralwidget)
        self.graphTitle.setText("Activity timeframe: " + self.a_mainTimeframeList.currentText())
        print("pop graph timeframe")






    def setupUi(self, DataWindow):
        DataWindow.setObjectName("DataWindow")
        DataWindow.resize(1124, 635)
        self.centralwidget = QtWidgets.QWidget(DataWindow)
        self.centralwidget.setObjectName("centralwidget")

        
        ##############################################################################
        ##############################################################################

        self.dataTable = QtWidgets.QTableWidget(self.centralwidget)
        self.dataTable.setGeometry(QtCore.QRect(0, 60, 441, 511))
        self.dataTable.setObjectName("dataTable")
        self.dataTable.setRowCount(0)
        self.dataTable.setShowGrid(True)

        
        self.tableTitle = QtWidgets.QLabel(self.centralwidget)
        self.tableTitle.setGeometry(QtCore.QRect(0, 0, 441, 61))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.tableTitle.setFont(font)
        self.tableTitle.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.tableTitle.setObjectName("tableTitle")

        self.dataGraph = pg.PlotWidget(self.centralwidget)
        self.dataGraph.setGeometry(QtCore.QRect(680, 60, 441, 511))
        self.dataGraph.setObjectName("dataGraph")


        self.graphTitle = QtWidgets.QLabel(self.centralwidget)
        self.graphTitle.setGeometry(QtCore.QRect(680, 0, 441, 61))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.graphTitle.setFont(font)
        self.graphTitle.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.graphTitle.setObjectName("graphTitle")
        
        #AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

        self.a_dataOptionsTitle = QtWidgets.QLabel(self.centralwidget)
        self.a_dataOptionsTitle.setGeometry(QtCore.QRect(490, 60, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.a_dataOptionsTitle.setFont(font)
        self.a_dataOptionsTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.a_dataOptionsTitle.setObjectName("a_dataOptionsTitle")

        self.a_line = QtWidgets.QFrame(self.centralwidget)
        self.a_line.setGeometry(QtCore.QRect(460, 90, 201, 16))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.a_line.setFont(font)
        self.a_line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.a_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.a_line.setObjectName("a_line")

        self.a_mainReportList = QtWidgets.QComboBox(self.centralwidget)
        self.a_mainReportList.setGeometry(QtCore.QRect(490, 120, 141, 22))
        self.a_mainReportList.setObjectName("a_mainReportList")
        for report in glob.glob("polscraper/reports/*analysis.json"):
            self.a_mainReportList.addItem(report[19:35])
        self.a_mainReportList.activated.connect(lambda: self.label.setText(self.a_mainReportList.currentText() + " selected"))

        self.a_showReportButton = QtWidgets.QPushButton(self.centralwidget)
        self.a_showReportButton.setGeometry(QtCore.QRect(510, 150, 101, 23))
        self.a_showReportButton.setObjectName("a_showReportButton")
        self.a_showReportButton.clicked.connect(self.populate_table_single_report)

        self.a_mainTimeframeList = QtWidgets.QComboBox(self.centralwidget)
        self.a_mainTimeframeList.setGeometry(QtCore.QRect(490, 200, 141, 22))
        self.a_mainTimeframeList.setObjectName("a_mainTimeframeList")

        self.a_mainTimeframeList.addItem("Today")
        self.a_mainTimeframeList.addItem("Last 2 days")
        self.a_mainTimeframeList.addItem("Last 7 days")
        self.a_mainTimeframeList.addItem("Last 14 days")
        self.a_mainTimeframeList.addItem("Last 30 days")
        self.a_mainTimeframeList.addItem("Last 60 days")
        self.a_mainTimeframeList.addItem("Last 180 days")
        self.a_mainTimeframeList.addItem("Last 365 days")

        self.a_mainTimeframeList.activated.connect(lambda: self.label.setText(self.a_mainTimeframeList.currentText() + " selected"))

        self.a_showTimeframeButton = QtWidgets.QPushButton(self.centralwidget)
        self.a_showTimeframeButton.setGeometry(QtCore.QRect(510, 230, 101, 23))
        self.a_showTimeframeButton.setObjectName("a_showTimeframeButton")

        self.a_showTimeframeButton.clicked.connect(self.populate_table_basic_timeframe)

        #BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB

        self.b_line_2 = QtWidgets.QFrame(self.centralwidget)
        self.b_line_2.setGeometry(QtCore.QRect(460, 260, 201, 16))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.b_line_2.setFont(font)
        self.b_line_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.b_line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.b_line_2.setObjectName("b_line_2")

        self.b_graphOptionsTitle_2 = QtWidgets.QLabel(self.centralwidget)
        self.b_graphOptionsTitle_2.setGeometry(QtCore.QRect(460, 280, 91, 16))
        self.b_graphOptionsTitle_2.setAlignment(QtCore.Qt.AlignCenter)
        self.b_graphOptionsTitle_2.setObjectName("b_graphOptionsTitle_2")

        self.b_tableCategoriesList = QtWidgets.QComboBox(self.centralwidget)
        self.b_tableCategoriesList.setGeometry(QtCore.QRect(460, 310, 91, 22))
        self.b_tableCategoriesList.setObjectName("b_tableCategoriesList")

        self.b_tableTimeframeList = QtWidgets.QComboBox(self.centralwidget)
        self.b_tableTimeframeList.setGeometry(QtCore.QRect(460, 360, 91, 22))
        self.b_tableTimeframeList.setObjectName("b_tableTimeframeList")

        self.b_showTableDataButton = QtWidgets.QPushButton(self.centralwidget)
        self.b_showTableDataButton.setGeometry(QtCore.QRect(460, 400, 91, 23))
        self.b_showTableDataButton.setObjectName("b_showTableDataButton")
        self.b_showTableDataButton.clicked.connect(lambda: print("clicked table data"))

        #CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC

        self.c_line_3 = QtWidgets.QFrame(self.centralwidget)
        self.c_line_3.setGeometry(QtCore.QRect(550, 280, 20, 151))
        self.c_line_3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.c_line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.c_line_3.setObjectName("c_line_3")

        self.c_graphOptionsTitle = QtWidgets.QLabel(self.centralwidget)
        self.c_graphOptionsTitle.setGeometry(QtCore.QRect(570, 280, 91, 16))
        self.c_graphOptionsTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.c_graphOptionsTitle.setObjectName("c_graphOptionsTitle")

        self.c_graphCategoriesList = QtWidgets.QComboBox(self.centralwidget)
        self.c_graphCategoriesList.setGeometry(QtCore.QRect(570, 310, 91, 22))
        self.c_graphCategoriesList.setObjectName("c_graphCategoriesList")

        self.c_graphTimeframeList = QtWidgets.QComboBox(self.centralwidget)
        self.c_graphTimeframeList.setGeometry(QtCore.QRect(570, 360, 91, 22))
        self.c_graphTimeframeList.setObjectName("c_graphTimeframeList")

        self.c_showGraphDataButton = QtWidgets.QPushButton(self.centralwidget)
        self.c_showGraphDataButton.setGeometry(QtCore.QRect(570, 400, 91, 23))
        self.c_showGraphDataButton.setObjectName("c_showGraphDataButton")

        #############################################################################

        self.clearDataButton = QtWidgets.QPushButton(self.centralwidget)
        self.clearDataButton.setGeometry(QtCore.QRect(510, 450, 101, 23))
        self.clearDataButton.setObjectName("clearDataButton")
        self.clearDataButton.clicked.connect(lambda: print("clicked clear data"))

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(460, 450, 201, 121))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")

        ##############################################################################
        ##############################################################################

        DataWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(DataWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1124, 21))
        self.menubar.setObjectName("menubar")

        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")

        self.menuPolscraper = QtWidgets.QMenu(self.menubar)
        self.menuPolscraper.setObjectName("menuPolscraper")

        DataWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(DataWindow)
        self.statusbar.setObjectName("statusbar")

        DataWindow.setStatusBar(self.statusbar)
        self.actionMain_Menu = QtWidgets.QAction(DataWindow)
        self.actionMain_Menu.setObjectName("actionMain_Menu")
        self.actionMain_Menu.triggered.connect(self.toMainMenu)

        self.actionExit = QtWidgets.QAction(DataWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionExit.triggered.connect(self.exit_program)

        self.actionPolscraper_Main = QtWidgets.QAction(DataWindow)
        self.actionPolscraper_Main.setObjectName("actionPolscraper_Main")
        self.actionPolscraper_Main.triggered.connect(self.toPolscraperMain)

        self.actionScheduler = QtWidgets.QAction(DataWindow)
        self.actionScheduler.setObjectName("actionScheduler")

        self.actionSentiment = QtWidgets.QAction(DataWindow)
        self.actionSentiment.setObjectName("actionSentiment")

        self.menuMenu.addAction(self.actionMain_Menu)
        self.menuMenu.addAction(self.actionExit)

        self.menuPolscraper.addAction(self.actionPolscraper_Main)
        self.menuPolscraper.addAction(self.actionSentiment)
        self.menuPolscraper.addAction(self.actionScheduler)

        self.menubar.addAction(self.menuMenu.menuAction())
        self.menubar.addAction(self.menuPolscraper.menuAction())

        self.retranslateUi(DataWindow)
        QtCore.QMetaObject.connectSlotsByName(DataWindow)

    def retranslateUi(self, DataWindow):
        _translate = QtCore.QCoreApplication.translate
        DataWindow.setWindowTitle(_translate("DataWindow", "Polscraper Data Display"))
        self.tableTitle.setText(_translate("DataWindow", "Report title or description"))
        self.graphTitle.setText(_translate("DataWindow", "Graph title or description"))
        self.a_dataOptionsTitle.setText(_translate("DataWindow", "Display Options"))
        self.a_showReportButton.setText(_translate("DataWindow", "Show Report"))
        self.a_showTimeframeButton.setText(_translate("DataWindow", "Show Timeframe"))
        self.c_graphOptionsTitle.setText(_translate("DataWindow", "Graph Options"))
        self.b_graphOptionsTitle_2.setText(_translate("DataWindow", "Table Options"))
        self.c_showGraphDataButton.setText(_translate("DataWindow", "Show Data"))
        self.b_showTableDataButton.setText(_translate("DataWindow", "Show Data"))
        self.label.setText(_translate("DataWindow", "Select how to view data using the options above"))
        self.clearDataButton.setText(_translate("DataWindow", "Clear Data"))
        self.menuMenu.setTitle(_translate("DataWindow", "Menu"))
        self.menuPolscraper.setTitle(_translate("DataWindow", "Polscraper"))
        self.actionMain_Menu.setText(_translate("DataWindow", "Main Menu"))
        self.actionExit.setText(_translate("DataWindow", "Exit"))
        self.actionPolscraper_Main.setText(_translate("DataWindow", "Polscraper Main"))
        self.actionScheduler.setText(_translate("DataWindow", "Scheduler"))
        self.actionSentiment.setText(_translate("DataWindow", "Sentiment"))

        
    def toMainMenu(self):
        print("to main menu")
        self.main_menu=QtWidgets.QMainWindow()
        self.ui = main.Ui_MainWindow()
        self.ui.setupUi(self.main_menu)
        DataWindow.destroy()
        self.main_menu.show()
    def toPolscraperMain(self):
        print("to polscraper data")
        self.polscraper_main=QtWidgets.QMainWindow()
        self.ui = polscraper_main.Ui_PolscraperWindow()
        self.ui.setupUi(self.polscraper_main)
        DataWindow.destroy()
        self.polscraper_main.show()
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

# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     DataWindow = QtWidgets.QMainWindow()
#     ui = Ui_DataWindow()
#     ui.setupUi(DataWindow)
#     DataWindow.show()
#     sys.exit(app.exec_())

app = QtWidgets.QApplication(sys.argv)
DataWindow = QtWidgets.QMainWindow()
ui = Ui_DataWindow()
ui.setupUi(DataWindow)


####### POP OUT CHART #######
####### ADD LATER #######
        # set0 = QBarSet('Topics')

        # set0.append([x for x in scores])

        # series = QBarSeries()
        # series.append(set0)

        # chart = QChart()
        # chart.addSeries(series)
        # chart.setTitle('Category frequency chart')
        # chart.setAnimationOptions(QChart.SeriesAnimations)


        # axisX = QBarCategoryAxis()
        # axisX.append(categories)

        # axisY = QValueAxis()
        # maxY = nlargest(1, scores)
        # print(maxY)
        # axisY.setRange(0, maxY[0])

        # chart.addAxis(axisX, Qt.AlignBottom)
        # chart.addAxis(axisY, Qt.AlignLeft)

        # chart.legend().setVisible(True)
        # chart.legend().setAlignment(Qt.AlignBottom)

        # NEED NOT REPLACE DATAGRAPH
        # JUST DO QCHARTVIEW(CHART).SHOW() OR SOMETHING
        # self.dataGraph = QChartView(chart)
        # self.dataGraph.setGeometry(QtCore.QRect(680, 60, 441, 511))
        # self.dataGraph.setObjectName("dataGraph")

##############################