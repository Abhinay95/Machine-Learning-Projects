from datetime import datetime
from application_logging import logger
from Training_Raw_data_validation.rawValidation import Raw_Data_Validation
from DataTransform_Training.DataTransformation import dataTransform
from DataTypeValidation_Insertion_Training.DataTypeValidation import dBOperation

class train_validation:
    def __init__(self, path):
        self.file_object = open("Training_Logs/Training_Main_Log.txt", 'a+')
        self.log_writer =logger.AppLogger()
        self.raw_data = Raw_Data_Validation(path)
        self.data_transform = dataTransform()
        self.dBOperation = dBOperation()

    def train_Validation(self):
        try:
            self.log_writer.log(self.file_object, 'Start of Validation on files for prediction!!')
            LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, noofcolumns = self.raw_data.valueFromSchema()

            regex = self.raw_data.manualRegexCreation()

            self.raw_data.validationFileNameRaw(regex, LengthOfDateStampInFile, LengthOfTimeStampInFile)

            self.raw_data.validateColumnLength(noofcolumns)

            self.raw_data.validateMissingValuesInWholeColumn()
            self.log_writer.log(self.file_object, "Raw Data Validation Complete!!")

            self.log_writer.log(self.file_object, "Starting Data Transforamtion!!")
            self.data_transform.addQuotesToStringValuesInColumn()
            self.log_writer.log(self.file_object, "Ending Data Transformation!!")

            self.log_writer.log(self.file_object, "Creating Training_Database and tables on the basis of given schema!!!")
            self.dBOperation.createTableDb('Training', column_names)
            self.log_writer.log(self.file_object, "Table creation Completed!!")

            self.log_writer.log(self.file_object, "Insertion of Data into Table started!!!!")
            self.dBOperation.insertIntoTableGoodData('Training')
            self.log_writer.log(self.file_object, "Insertion in Table completed!!!")

            self.log_writer.log(self.file_object, "Deleting Good Data Folder!!")
            self.raw_data.deleteExistingGoodDataTrainingFolder()
            self.log_writer.log(self.file_object, "Good_Data folder deleted!!!")

            self.log_writer.log(self.file_object, "Moving bad files to Archive and deleting Bad_Data folder!!!")
            self.raw_data.moveBadFilesToArchiveBad()
            self.log_writer.log(self.file_object, "Bad files moved to archive!! Bad folder Deleted!!")

            self.log_writer.log(self.file_object, "Validation Operation completed!!")

            self.log_writer.log(self.file_object, "Extracting csv file from table")
            self.dBOperation.selectingDatafromtableintocsv('Training')
            self.log_writer.log(self.file_object, "File extracted successfully from table!!")
            self.file_object.close()

        except Exception as e:
            raise e

