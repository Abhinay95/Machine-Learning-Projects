from datetime import datetime
from application_logging import logger
from Training_Raw_data_Validation.rawValidation import Raw_Data_Validation
from DataTypeValidation_Insertion_Training.DataTypeValidation import dBOperation

class train_validation:
    def __init__(self, path):
        self.file_object = open('Training_Logs/Training_Main_Log.txt', 'a+')
        self.log_writer = logger.App_Logger()
        self.raw_data = Raw_Data_Validation(path)
        self.dBOperation = dBOperation()

    def train_validation(self):
        try:
            self.log_writer.log(self.file_object, "Start of Validation on files for training!!")
            LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, noofcolumns = self.raw_data.valuesFromSchema()

            regex = self.raw_data.manualRegexCreation()

            self.raw_data.validationFileNameRaw(regex, LengthOfDateStampInFile, LengthOfTimeStampInFile)

            self.raw_data.validateColumnLength(noofcolumns)

            self.raw_data.validateMissingValuesInWholeColumns()
            self.log_writer.log(self.file_object, "Raw Data Validation Completed!!!")

            self.log_writer.log(self.file_object, "Creating Training_Database and tables on the basis of given schema!!!")
            self.dBOperation.createTableDb('Training', column_names)
            self.log_writer.log(self.file_object, "Table Creation Completed!!")

            self.log_writer.log(self.file_object, "Insertion of data into table started!!")
            self.dBOperation.insertIntoTableGoodData('Training')
            self.log_writer.log(self.file_object, "Data Inserted Successfully!!")

            self.log_writer.log(self.file_object, "Deleting Good Data Folder!!")
            self.raw_data.deleteExistingGoodDataTrainingFolder()
            self.log_writer.log(self.file_object, "Good data folder deleted!!")

            self.log_writer.log(self.file_object, "Moving bad files to Archive and deleting Bad_Data folder!!!")
            self.raw_data.moveBadFilesToArchiveBad()
            self.log_writer.log(self.file_object, "Bad files moved to archive!! Bad folder deleted!!")
            self.log_writer.log(self.file_object, "Validation operation completed!!")

            self.log_writer.log(self.file_object, "Extraction of csv file!!")
            self.dBOperation.selectingDatafromtableintocsv('Training')
            self.log_writer.log(self.file_object, "File extracted successfully!!")
            self.file_object.close()
        except Exception as e:
            raise e