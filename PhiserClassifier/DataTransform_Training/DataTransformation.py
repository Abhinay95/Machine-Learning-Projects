from datetime import datetime
from os import listdir
from application_logging.logger import AppLogger
import pandas as pd

class dataTransform:
    def __init__(self):
        self.goodPath = "Training_Raw_files_validated/Good_Raw"
        self.logger = AppLogger()

    def addQuotesToStringValuesInColumn(self):
        log_file = open("Training_Logs/addQuotesToStringValuesInColumn.txt", 'a+')
        try:
            onlyfiles = [f for f in listdir(self.goodPath)]

            for file in onlyfiles:
                data = pd.read_csv(self.goodPath + "/" + file)
                for column in data.columns:
                    count = data[column][data[column] == '?'].count()
                    if count != 0:
                        data[column] = data[column].replace('?', "'?'")
                data.to_csv(self.goodPath + "/" + file, index=None, header=True)
                self.logger.log(log_file," %s: Quotes added successfully!!" % file)
        except Exception as e:
            self.logger.log(log_file, "Data Transformation failed because:: %s" % e)
            log_file.close()
        log_file.close()