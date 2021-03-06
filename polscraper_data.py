# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'polscraper_data.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import os, glob, sys, re, functools
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

from polscraper import language_analyzer


import pyqtgraph as pg



class Ui_DataWindow(object):

    def reverse_dict(self, data):        
        # sort data in reverse order
        data = {k: v for k, v in sorted(data.items(), key=lambda item: item[1])}

        # sort data in descending numerical order
        reversed_data = {}
        for key, value in reversed(data.items()):
            reversed_data[key] = value
        return reversed_data

    def get_countries(self, timeframe):
        current_time = datetime.now()

        countries = []

        if timeframe != "Today" and timeframe != "Select a timeframe":
            timeframe = re.findall('\d+', timeframe)
            timeframe = int(timeframe[0])

        elif timeframe == "Select a timeframe":
            print("user must select a timeframe")
            self.label.setText("Select a timeframe to enable this function")

        else:
            timeframe = 1

        max_time_diff = current_time - timedelta(days=timeframe)

        for report in glob.glob(f"polscraper\\reports\\*_pol_sentiment.json"):
            
            report_date = datetime.strptime(report[19:35], "%Y-%m-%d-%H-%M")
            if max_time_diff < report_date < current_time:

                with open(f"{report}", encoding="utf-8") as file:
                    datafile = json.load(file)

                    for thread in datafile:
                        op_flag = thread['Flag']

                        if op_flag not in countries:
                            countries.append(op_flag)

                        for reply in thread['Replies']:
                            reply_flag = reply['Flag']

                            if reply_flag not in countries:
                                countries.append(reply_flag)
                                
        print(countries)
        return countries

    def fill_country_list(self):
        timeframe = self.a_mainTimeframeList.currentText()
        countries = self.get_countries(timeframe)

        self.c_countryOptionsList.addItem("All Countries")
        for country in countries:
            self.c_countryOptionsList.addItem(str(country))



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
            

        # # sort data in reverse order
        # data = {k: v for k, v in sorted(data[0].items(), key=lambda item: item[1])}

        # # sort data in descending numerical order
        # reversed_data = {}
        # for key, value in reversed(data.items()):
        #     reversed_data[key] = value

        reversed_data = self.reverse_dict(data[0])

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
        print("pop graph single report")
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
        self.dataGraph.clear()
        self.dataGraph.addItem(bg1)

        # self.graphTitle.setText(f"Top 3 topics: {categories[0]}, {categories[1]}, {categories[2]}") disabled for sensitivity
        self.graphTitle.setText(f"Topic frequency visualisation")
        print("graph on display")


    def populate_table_basic_timeframe(self, *args):
        print(args)
        print("===============")
        self.dataTable.clear()
        self.tableTitle.setText("Topic Data: " + self.a_mainTimeframeList.currentText())
        print("pop table timeframe")
        current_time = datetime.now()
        timeframe = self.a_mainTimeframeList.currentText()

        if timeframe != "Today" and timeframe != "Select a timeframe":
            timeframe = re.findall('\d+', timeframe)
            timeframe = int(timeframe[0])
        elif timeframe == "Select a timeframe":
            print("user must select a timeframe")
            self.label.setText("Select a timeframe to enable this function")
        else:
            timeframe = 1

        max_time_diff = current_time - timedelta(days=timeframe)

        # this dict will hold all the reports as nested dicts
        data = {}

        # this is a list of the reports to be used for table vertical labels (not sure if needed now)
        reports = []


        # get reports that are within the specified timeframe
        for report in glob.glob(f"polscraper\\reports\\*_pol_sentiment_analysis.json"):
            report_date = datetime.strptime(report[19:35], "%Y-%m-%d-%H-%M")
            if max_time_diff < report_date < current_time:
                # print(report)
                # print("is within " + str(timeframe) + " days")

                # open the report file and extract the dictionary from the json (which puts it inside a list)
                with open(f"{report}") as report_json_file:
                    reportdata = json.load(report_json_file)
                    # print(reportdata)
                    reportdata = reportdata[0]

                    # the key of each sub-dictionary (representing an individual report) to be the datetime portion of the report filename:
                    report = report[19:35]
                    # which we then add to the list of reports in this timeframe (now sure if needed now)
                    reports.append(report)

                    # then for each report we add it as a nested dictionary to the dictionary "data"
                    data[report] = {}
                    for key, value in reportdata.items():
                        if key == "Date" or key == "Time":
                            pass
                        elif "polscraper" in key:
                            key = key[19:35]
                        else:
                            data[report][key] = value
        
        # this is a list of the reply count per report
        reply_count = []

        # this is a dict of the numposts per country
        country_posts = {}

        # get number of replies in each report and number of posts per country
        for report in glob.glob(f"polscraper\\reports\\*_pol_sentiment.json"):
            
            report_date = datetime.strptime(report[19:35], "%Y-%m-%d-%H-%M")
            if max_time_diff < report_date < current_time:
                with open(f"{report}", encoding="utf-8") as file:
                    datafile = json.load(file)

                    # print(report)

                    replies = 0
                    for thread in datafile:
                        # print(thread)
                        op_flag = thread['Flag']
                        # print("OP:")
                        # print(op_flag)
                        if op_flag not in country_posts:
                            country_posts[op_flag] = 1
                            # print("new country detected, value:")
                            # print(country_posts[op_flag])

                        else:
                            country_posts[op_flag] += 1
                            # print(country_posts[op_flag])


                        # print("=+=+=+")
                        replies += (len(thread['Replies']) + 1)

                        for reply in thread['Replies']:
                            reply_flag = reply['Flag']
                            # print(reply_flag)
                            if reply_flag not in country_posts:
                                country_posts[reply_flag] = 1
                                # print("new country detected, value:")
                                # print(country_posts[reply_flag])

                            else:
                                country_posts[reply_flag] += 1
                                # print(country_posts[reply_flag])

                                
                            # print(country_posts[reply['Flag']])


                reply_count.append(replies)




        # get all categories - from longest dict in data, as it will have more categories (ie if we add more categories later)
        length = 0
        longest = {'items':1}
        for d in data.values():
            if len(d) > len(longest):
                longest = d
            else:
                print("ignore")



        # make a list out of all the categories/topics of the longest sub dict to display as table header labels
        categories = list(longest.keys())
        categories.insert(0, "Report")
        
        self.dataTable.setRowCount(0)
        self.dataTable.setColumnCount(len(categories))
        self.dataTable.setHorizontalHeaderLabels(categories)

        # populate vertical headers (col 1) with report titles
        for r in data:
            row = self.dataTable.rowCount()
            self.dataTable.setRowCount(row+1)
            col = 0
            # print(r)
            cell = QtWidgets.QTableWidgetItem(str(r))
            self.dataTable.setItem(row, col, cell)

        # Populating the data

        # set the 'cursor', if you can call it that, to the top row
        row = 0

        # iterate over the dict of nested dicts ('data')
        for report_title, report_content in data.items():

            # set the cursor to the second column (first is the report titles)
            col = 1

            # iterate over each nested dict in turn
            for topic, freq in report_content.items():

                # populate each cell with the frequency (value) of each topic/category
                cell = QtWidgets.QTableWidgetItem(str(freq))
                self.dataTable.setItem(row, col, cell)

                # move the cursor to next column and row
                col += 1

            row += 1

        
        # if you click the "posts" button, plot post count over timeframe on graph
        if  args[0] == "showreplies":
            self.populate_graph_posts(reply_count)

        # if you enter countries in graph options show numposts from diff countries within timeframe
        elif args[0] == "countries":
            
            # detect what type of graph user wants to plot, if relevant
            graph_type = self.c_graphTimeframeList.currentText()

            if graph_type == "Bar Chart":
                print("PLOT THE COUNTRY POSTERS")
                self.populate_data_countries(country_posts, "barchart", reports, categories)

            else:
                print("PLOT THE COUNTRY POSTERS")
                self.populate_data_countries(country_posts, "lineplot", reports)        

        # if you click the "topics" button, plot topics count on graph
        else:           
            self.populate_graph_basic_timeframe(data) 


# This gets the TOTALS over the timeframe
# for key, value in reportdata.items():
#     if key == "Date" or key == "Time":
#         print(str(key) + " - ignoring")
#     else:
#         print("checking " + str(key))
#         if key not in data:
#             data[key] = value
#             print("new category added - " + str(key) + " with score of: " + str(value))
#         else:
#             print("update category - " + str(key) + " current score: " + str(value))
#             data[key] += value
#             print("score now: " + str(data[key]))

    
    def addTableRow_basic_timeframe(self, table, row_data):
        row = table.rowCount()
        table.setRowCount(row+1)
        col = 0
        for item in row_data: 
            cell = QtWidgets.QTableWidgetItem(str(item))
            table.setItem(row, col, cell)
            col += 1


    def populate_graph_basic_timeframe(self, data):
        self.dataGraph.clear()
        self.graphTitle.setText("Activity timeframe: " + self.a_mainTimeframeList.currentText())
        print("pop graph timeframe")

        length = 0
        longest = {'items':1}
        for d in data.values():
            if len(d) > len(longest):
                longest = d
            else:
                print("ignore")
        x_axis = list(longest.keys())
        x_axis.remove("Pages")


        # need to get more colours than the same 7 repeating!
        colours = ['w','b','r','g','c','m','y','w','b','r','g','c','m','y','w','b','r','g','c','m','y','w','b','r','g','c','m','y','w','b','r','g','c','m','y']
        # colours = ['RGB(240,248,255)','RGB(139,131,120)','RGB(0,255,255)','RGB(227,207,87)','RGB(0,0,255)','RGB(138,43,226)','RGB(156,102,31)','RGB(165,42,42)','RGB(255,97,3)','RGB(69,139,0)','RGB(220,20,60)','RGB(184,134,11)','RGB(85,107,47)','RGB(255,174,185)','RGB(255,160,122)','RGB(139,87,66)','RGB(119,136,153)','RGB(139,139,0)','RGB(179,238,58)','RGB(238,207,161)','RGB(238,213,210)','RGB(199,21,133)','RGB(60,179,113)','RGB(186,85,211)']
        # colours = ['240,248,255,1','139,131,120,1','0,255,255,1','227,207,87,1','0,0,255,1','138,43,226,1','156,102,31,1','165,42,42,1','255,97,3,1','69,139,0,1','220,20,60,1','184,134,11,1','85,107,47,1','255,174,185,1','255,160,122,1','139,87,66,1','119,136,153,1','139,139,0,1','179,238,58,1','238,207,161,1','238,213,210,1','199,21,133,1','60,179,113,1','186,85,211,1']
        # colours = [(240,248,255,1),(139,131,120,1),(0,255,255,1),(227,207,87,1),(0,0,255,1),(138,43,226,1),(156,102,31,1),(165,42,42,1),(255,97,3,1),(69,139,0,1),(220,20,60,1),(184,134,11,1),(85,107,47,1),(255,174,185,1),(255,160,122,1),(139,87,66,1),(119,136,153,1),(139,139,0,1),(179,238,58,1),(238,207,161,1),(238,213,210,1),(199,21,133,1),(60,179,113,1),(186,85,211,1)]
        col_select = 0



        for category in x_axis:
            topicfreqs = []
            for report_title, report_content in data.items():
                for topic, freq in report_content.items():
                    if topic == category:
                        topicfreqs.append(freq)
            pen=pg.mkPen(color=colours[col_select])
            # self.dataGraph.plot(x_axis, freqs) need to convert x axis to string for pyqtgraph
            self.dataGraph.plot(range(1, len(topicfreqs)+1), topicfreqs, pen=pen, name=str(category))
            col_select += 1
        self.label.setText("Displaying topic frequencies")
        # self.dataGraph.addLegend() 

        # SEE IF IT'S POSSIBLE TO ADD A TICKBOX TO SHOW/HIDE EACH TOPIC LINE
        # SO YOU CAN CLUTTER/DECLUTTER AS REQUIRED

        # ....don't know what the graph will look like yet
        # maybe the DIFFERENCE between the top topic and the next on the list
        # displayed as a bar chart? or line plot?
        # or total number of posts displayed as a line plot?
        # hmmm...

    # show line plot of total replies over time period
    def populate_graph_posts(self,replies):
        print("pop graph posts")
        self.dataGraph.clear()
        total_replies = 0

        for reply in replies:
            total_replies += reply

        self.graphTitle.setText(f"Activity plot - {total_replies} stored posts")
        self.dataGraph.showGrid(x=True, y=True)
        self.dataGraph.plot(range(1, len(replies)+1), replies)
        self.label.setText("Topic data table with post count plot")


    # show data based on country of origin (poster's location)
    def populate_data_countries(self, poster_data, *args):
        self.dataGraph.clear()
        self.dataTable.clear()
        self.dataTable.setColumnCount(2)
        self.dataTable.setRowCount(0)

        timeframe = self.a_mainTimeframeList.currentText()

        print("pop table countries")
        print(args)

        poster_data = self.reverse_dict(poster_data)

        options = self.c_countryOptionsList.currentText()


        row = 0
        col = 0
        for country, numposts in poster_data.items():
            self.dataTable.setRowCount(row+1)
            col = 0

            cell = QtWidgets.QTableWidgetItem(str(country))
            self.dataTable.setItem(row, col, cell)
            col += 1
            # print(country)

            cell = QtWidgets.QTableWidgetItem(str(numposts))
            self.dataTable.setItem(row, col, cell)
            # print(numposts)
            row += 1


        # display total number of posts per country
        if args[0] == "barchart" and options == "All Countries":
            countries = []
            posts = []

            for key, value in poster_data.items():
                countries.append(key)
                posts.append(int(value))


            maxY = nlargest(1, posts)
            print(maxY)

            y1 = range(0, maxY[0])

            x = range(1, len(countries))

            bg1= pg.BarGraphItem(x=x, height=posts, width=0.8, brush="b")
            self.dataGraph.clear()
            self.dataGraph.addItem(bg1)

            self.graphTitle.setText(f"Activity by country")
            print("graph on display")

        # display individual countries' topic counts
        elif args[0] == "barchart" and options != "All Countries":
            print("display topic usage by selected country")

            t = 0
            for country, post_count in poster_data.items():
                if country == options:
                    t = post_count
            
            print(t)

            # manipulate the data
            reports = args[1]
            print(reports)

            print(f"Scanning reports for {options}")
            topics_by_country = language_analyzer.country_analyzer(reports, options)

            print(f"{options} topic counts:")

            topics_by_country = self.reverse_dict(topics_by_country)
            print(topics_by_country)

            most_discussed = nlargest(1, topics_by_country, key=topics_by_country.get)

            topics = list(topics_by_country.keys())
            topic_counts = list(topics_by_country.values())

            # fill the table
            self.dataTable.clear()
            self.dataTable.setRowCount(0)
            self.dataTable.setColumnCount(2)

            row = 0
            col = 0
            for category, category_count in topics_by_country.items():
                self.dataTable.setRowCount(row+1)
                col = 0

                cell = QtWidgets.QTableWidgetItem(str(category))
                self.dataTable.setItem(row, col, cell)
                col += 1

                cell = QtWidgets.QTableWidgetItem(str(category_count))
                self.dataTable.setItem(row, col, cell)
                row += 1


            # create the bar chart
            maxY = nlargest(1, topic_counts)
            print(maxY)

            y1 = range(0, maxY[0])

            x = range(1, len(topics))

            bg1= pg.BarGraphItem(x=x, height=topic_counts, width=0.8, brush="b")
            self.dataGraph.clear()
            self.dataGraph.showGrid(x=True, y=True)
            self.dataGraph.addItem(bg1)

            self.tableTitle.setText(f"{options}: most frequent subjects - {timeframe}")
            self.graphTitle.setText(f"{t} posts stored")
            self.label.setText(f"{timeframe}: The most common topic for posters from {options} was {most_discussed[0]}")

        # display activity per individual country over a time period
        elif args[0] == "lineplot" and options != "All Countries":
            print("lineplot!!!")
            print("displaying country activity by time/report")

            # set up the data receiving structures
            reports = args[1]
            posts_by_country_per_report = []
            total_country_posts = 0

            
            self.dataTable.clear()
            self.dataTable.setRowCount(0)
            self.dataTable.setColumnCount(2)

            # extract the data
            for reportfile in glob.glob(f"polscraper\\reports\\*_pol_sentiment.json"):
                if reportfile[19:35] in reports:
                    country_posts_in_this_report = 0
                    with open(f"{reportfile}", encoding="utf-8") as file:
                        datafile = json.load(file)

                        for thread in datafile:
                            if thread['Flag'] == options:
                                country_posts_in_this_report += 1
                            
                            for reply in thread['Replies']:
                                if reply['Flag'] == options:
                                    country_posts_in_this_report += 1

                    posts_by_country_per_report.append(country_posts_in_this_report)
                    total_country_posts += country_posts_in_this_report

            # fill the table
            row = 0
            row = self.dataTable.rowCount()
            for report in reports:
                self.dataTable.setRowCount(row+1)
                col = 0

                cell = QtWidgets.QTableWidgetItem(str(report))
                self.dataTable.setItem(row, col, cell)
                row += 1

            row = 0
            col = 1
            for quantity in posts_by_country_per_report:
                cell = QtWidgets.QTableWidgetItem(str(quantity))
                self.dataTable.setItem(row, col, cell)
                row += 1



            # plot the line graph
            self.dataGraph.plot(range(1, len(reports)+1), posts_by_country_per_report)
            self.dataGraph.showGrid(x=True, y=True)
            self.graphTitle.setText(f"Activity: {options}")
            self.tableTitle.setText(f"{options}: {total_country_posts} posts - {timeframe}")

        else:
            print("nothin")







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

        self.a_mainTimeframeList.addItem("Select a timeframe")
        self.a_mainTimeframeList.addItem("Today")
        self.a_mainTimeframeList.addItem("Last 2 days")
        self.a_mainTimeframeList.addItem("Last 7 days")
        self.a_mainTimeframeList.addItem("Last 14 days")
        self.a_mainTimeframeList.addItem("Last 30 days")
        self.a_mainTimeframeList.addItem("Last 60 days")
        self.a_mainTimeframeList.addItem("Last 180 days")
        self.a_mainTimeframeList.addItem("Last 365 days")

        self.a_mainTimeframeList.activated.connect(self.fill_country_list)
        self.a_mainTimeframeList.activated.connect(lambda: self.label.setText(self.a_mainTimeframeList.currentText() + " selected"))

        self.a_showTopicsButton = QtWidgets.QPushButton(self.centralwidget)
        self.a_showTopicsButton.setGeometry(QtCore.QRect(490, 230, 71, 23))
        self.a_showTopicsButton.setObjectName("a_showTopicsButton")

        self.a_showTopicsButton.clicked.connect(self.populate_table_basic_timeframe)

        self.a_showRepliesButton = QtWidgets.QPushButton(self.centralwidget)
        self.a_showRepliesButton.setGeometry(QtCore.QRect(560, 230, 71, 23))
        self.a_showRepliesButton.setObjectName("a_showRepliesButton")

        self.a_showRepliesButton.clicked.connect(functools.partial(self.populate_table_basic_timeframe, "showreplies"))

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

        self.c_countryOptionsTitle = QtWidgets.QLabel(self.centralwidget)
        self.c_countryOptionsTitle.setGeometry(QtCore.QRect(570, 280, 91, 16))
        self.c_countryOptionsTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.c_countryOptionsTitle.setObjectName("c_countryOptionsTitle")

        self.c_countryOptionsList = QtWidgets.QComboBox(self.centralwidget)
        self.c_countryOptionsList.setGeometry(QtCore.QRect(570, 310, 91, 22))
        self.c_countryOptionsList.setObjectName("c_countryOptionsList")

        self.c_graphTimeframeList = QtWidgets.QComboBox(self.centralwidget)
        self.c_graphTimeframeList.setGeometry(QtCore.QRect(570, 360, 91, 22))
        self.c_graphTimeframeList.setObjectName("c_graphTimeframeList")
        self.c_graphTimeframeList.addItem("Bar Chart")
        self.c_graphTimeframeList.addItem("Line Plot")

        self.c_showGraphDataButton = QtWidgets.QPushButton(self.centralwidget)
        self.c_showGraphDataButton.setGeometry(QtCore.QRect(570, 400, 91, 23))
        self.c_showGraphDataButton.setObjectName("c_showGraphDataButton")
        self.c_showGraphDataButton.clicked.connect(functools.partial(self.populate_table_basic_timeframe, "countries"))

        #############################################################################

        self.clearDataButton = QtWidgets.QPushButton(self.centralwidget)
        self.clearDataButton.setGeometry(QtCore.QRect(510, 450, 101, 23))
        self.clearDataButton.setObjectName("clearDataButton")
        self.clearDataButton.clicked.connect(lambda: self.dataGraph.clear())
        self.clearDataButton.clicked.connect(lambda: self.dataTable.clear())
        self.clearDataButton.clicked.connect(lambda: self.label.setText("Displays Cleared"))

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(460, 480, 201, 111))
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
        self.a_showTopicsButton.setText(_translate("DataWindow", "Topics"))
        self.a_showRepliesButton.setText(_translate("DataWindow", "Posts"))
        self.c_countryOptionsTitle.setText(_translate("DataWindow", "Country Data"))
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