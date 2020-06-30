import sqlite3
import csv
from application_logging.logger import AppLogger
from datetime import datetime
import os
from os import listdir
import shutil

class dBOperation:
    def __init__(self):
        self.path = 'Prediction_Database/'
        self.goodFilePath = "Prediction_Raw_Files_Validated/Good_Raw"
        self.badFilePath = "Prediction_Raw_Files_Validated/Bad_Raw"
        self.logger = AppLogger()

    def databaseConnection(self, DatabaseName):
        try:
            conn = sqlite3.connect(self.path+DatabaseName+'.db')
            file = open("Prediction_Logs/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, "Opened %s database successfully" % DatabaseName)
            file.close()
        except ConnectionError:
            file = open("Prediction_Logs/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, "Error while connecting to database: %s" %ConnectionError)
            file.close()
            raise ConnectionError
        return conn

    def createTableDb(self, DatabaseName, column_names):
        try:
            conn = self.databaseConnection(DatabaseName)
            conn.execute('DROP TABLE IF EXISTS GOOD_RAW_DATA')

            for key in column_names.keys():
                type = column_names[key]

                try:
                    conn.execute('ALTER TABLE GOOD_RAW_DATA ADD COLUMN "{column_name}" {datatype}'.format(column_name=key, datatype=type))
                except:
                    conn.execute('CREATE TABLE GOOD_RAW_DATA ({column_name} {datatype})'.format(column_name=key, datatype=type))
            conn.close()
            file = open("Prediction_Logs/DbTableCreateLog.txt", 'a+')
            self.logger.log(file, "Tables created successfully!!")
            file.close()

            file = open("Prediction_Logs/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, "Closed %s database successfully" % DatabaseName)
            file.close()
        except Exception as e:
            file = open("Prediction_Logs/DbTableCreateLog.txt", 'a+')
            self.logger.log(file, "Error while creating table: %s " % e)
            file.close()
            conn.close()
            file = open("Prediction_Logs/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, "Closed %s database successfully" % DatabaseName)
            file.close()
            raise e

    def insertIntoTableGoodData(self, Database):

        """
                                       Method Name: insertIntoTableGoodData
                                       Description: This method inserts the Good data files from the Good_Raw folder into the
                                                    above created table.
                                       Output: None
                                       On Failure: Raise Exception

                                        Written By: iNeuron Intelligence
                                       Version: 1.0
                                       Revisions: None

                """

        conn = self.databaseConnection(Database)
        goodFilePath = self.goodFilePath
        badFilePath = self.badFilePath
        onlyfiles = [f for f in listdir(goodFilePath)]
        log_file = open("Prediction_Logs/DbInsertLog.txt", 'a+')

        for file in onlyfiles:
            try:
                with open(goodFilePath + '/' + file, 'r') as f:
                    next(f)
                    reader = csv.reader(f, delimiter="\n")
                    for line in enumerate(reader):
                        for list_ in (line[1]):
                            try:
                                conn.execute('INSERT INTO Good_Raw_Data values ({values})'.format(values=(list_)))
                                self.logger.log(log_file, " %s: File loaded successfully!!" % file)
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
                raise e

        conn.close()
        log_file.close()

    def selectingDatafromtableintocsv(self, Database):
        self.fileFromDb = 'Prediction_FileFromDB/'
        self.filename = 'InputFile.csv'
        log_file = open("Prediction_Logs/ExportToCsv.txt", 'a+')
        try:
            conn =self.databaseConnection(Database)
            sqlSelect = "SELECT * FROM GOOD_RAW_DATA"
            cursor = conn.cursor()

            cursor.execute(sqlSelect)

            results = cursor.fetchall()
            headers = [i[0] for i in cursor.description]

            if not os.path.isdir(self.fileFromDb):
                os.makedirs(self.fileFromDb)

            csv_file = csv.writer(open(self.fileFromDb + self.filename, 'w', newline=''),delimiter=',', lineterminator='\r\n',quoting=csv.QUOTE_ALL, escapechar='\\')

            csv_file.writerow(headers)
            csv_file.writerows(results)

            self.logger.log(log_file, "File exported successfully!!!")
        except Exception as e:
            self.logger.log(log_file, "File exporting failed. Error : %s" %e)
            log_file.close()
            raise e