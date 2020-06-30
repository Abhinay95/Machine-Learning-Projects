import pandas as pd
import numpy as np
import os
from os import listdir
from application_logging.logger import AppLogger
from datetime import datetime

class dataTransformPredict:
    def __init__(self):
        self.logger = AppLogger()
        self.goodDataPath = "Prediction_Raw_Files_Validated/Good_Raw"

    def addQuotesToStringValuesInColumn(self):
        try:
            log_file = open("Prediction_Logs/dataTransformLog.txt", 'a+')
            onlyfiles = [f for f in listdir(self.goodDataPath)]
            for file in onlyfiles:
                data = pd.read_csv(self.goodDataPath + '/' + file)
                for column in data.columns:
                    count = data[column][data[column] == '?'].count()
                    if count != 0:
                        data[column] = data[column].replace('?', "'?'")
                data.to_csv(self.goodDataPath + "/" + file, index=None, header=True)
                self.logger.log(log_file, " %s: Quotes added successfully!!" % file)
        except Exception as e:
            log_file = open("Prediction_Logs/dataTransformLog.txt", 'a+')
            self.logger.log(log_file, "Data Transformation failed because:: %s" % e)
            log_file.close()
            return e
        log_file.close()
