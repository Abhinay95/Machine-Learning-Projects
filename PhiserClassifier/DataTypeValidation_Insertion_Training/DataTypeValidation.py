import sqlite3
import os
from os import listdir
import pandas as pd
from application_logging.logger import AppLogger
import csv
import shutil
from datetime import datetime

class dBOperation:
    def __init__(self):
        self.path = 'Training_Database/'
        self.badFilePath = "Training_Raw_files_validated/Bad_Raw"
        self.goodFilePath = "Training_Raw_files_validated/Good_Raw"
        self.logger = AppLogger()

    def databaseConnection(self, DatabaseName):
        try:
            conn = sqlite3.connect(self.path + DatabaseName + '.db')

            file = open("Training_Logs/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, "Opened %s database successfully" % DatabaseName)
            file.close()
        except ConnectionError:
            file = open("Training_Logs/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, "Error while connecting to database: %s" %ConnectionError)
            file.close()
            raise ConnectionError
        return conn

    def createTableDb(self, DatabaseName, column_names):
        try:
            conn = self.databaseConnection(DatabaseName)
            c = conn.cursor()
            c.execute("SELECT COUNT(name) FROM sqlite_master WHERE type = 'table' AND name = 'GOOD_RAW_DATA'")
            if c.fetchone()[0]==1:
                conn.close()
                file = open("Training_Logs/DbTableCreateLog.txt", 'a+')
                self.logger.log(file, "Tables created successfully!!")
                file.close()

                file = open("Training_Logs/DataBaseConnectionLog.txt", 'a+')
                self.logger.log(file, "Closed %s database successfully" % DatabaseName)
                file.close()
            else:
                for key in column_names.keys():
                    type = column_names[key]

                    try:
                        conn.execute('ALTER TABLE GOOD_RAW_DATA ADD COLUMN "{column_name}" {datatype}'.format(column_name=key, datatype=type))
                    except:
                        conn.execute('CREATE TABLE GOOD_RAW_DATA ({column_name} {datatype})'.format(column_name=key, datatype=type))

                conn.close()

                file = open("Training_Logs/DbTableCreateLog.txt", 'a+')
                self.logger.log(file, "Table created successfully!!")
                file.close()

                file = open("Training_Logs/DataBaseConnectionLog.txt", 'a+')
                self.logger.log(file, "Closed %s database successfully" % DatabaseName)
                file.close()

        except Exception as e:
            file = open("Training_Logs/DbTableCreateLog.txt", 'a+')
            self.logger.log(file, "Error while creating table: %s " % e)
            file.close()
            conn.close()

            file = open("Training_Logs/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, "Closed %s database successfully" % DatabaseName)
            file.close()
            raise e

    def insertIntoTableGoodData(self, Database):
        conn = self.databaseConnection(Database)
        goodFilePath = self.goodFilePath
        badFilePath = self.badFilePath
        onlyfiles = [f for f in listdir(goodFilePath)]
        log_file = open("Training_Logs/DbInsertLog.txt", 'a+')

        for file in onlyfiles:
            try:
                with open(self.goodFilePath + '/' + file, 'r') as f:
                    next(f)
                    reader = csv.reader(f, delimiter="\n")
                    for line in enumerate(reader):
                        for list_ in (line[1]):
                            try:
                                conn.execute('INSERT INTO GOOD_RAW_DATA values({values})'.format(values=list_))
                                self.logger.log(log_file," %s: File loaded successfully!!" % file)
                                conn.commit()
                            except Exception as e:
                                raise e
            except Exception as e:
                conn.rollback()
                self.logger.log(log_file, "Error while creating table: %s " % e)
                shutil.move(goodFilePath + '/' + file, badFilePath)
                self.logger.log(log_file, "File Moved Successfully %s" % file)
                log_file.close()
                conn.close()
        conn.close()
        log_file.close()

    def selectingDatafromtableintocsv(self, Database):
        self.fileFromDb = 'Training_FileFromDB/'
        self.filename = 'InputFile.csv'
        log_file = open("Training_Logs/ExportToCsv.txt", 'a+')
        try:
            conn = self.databaseConnection(Database)
            sqlSelect = 'SELECT * FROM GOOD_RAW_DATA'
            cursor = conn.cursor()

            cursor.execute(sqlSelect)

            results = cursor.fetchall()
            headers = [i[0] for i in cursor.description]

            if not os.path.isdir(self.fileFromDb):
                os.makedirs(self.fileFromDb)

            csvFile = csv .writer(open(self.fileFromDb + self.filename, 'w', newline=''), delimiter=',', lineterminator='\r\n',quoting=csv.QUOTE_ALL, escapechar='\\')

            csvFile.writerow(headers)
            csvFile.writerows(results)

            self.logger.log(log_file, "File exported successfully!!!")
            log_file.close()
        except Exception as e:
            self.logger.log(log_file,"File exporting failed. Error : %s" %e)
            log_file.close()
