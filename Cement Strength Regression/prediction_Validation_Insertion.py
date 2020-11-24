from application_logging import logger
from Prediction_Raw_Data_Validation.predictionDataValidation import Prediction_Data_Validation
from DataTypeValidation_Insertion_Prediction.DataTypeValidationPrediction import dBOperation

class pred_validation:
    def __init__(self, path):
        self.file_object = open("Prediction_Logs/Prediction_Log.txt", 'a+')
        self.log_writer = logger.App_Logger()
        self.raw_data = Prediction_Data_Validation(path)
        self.dBOperation = dBOperation()

    def prediction_validation(self):
        try:
            self.log_writer.log(self.file_object, 'Start of Validation on files for prediction!!')
            LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, noofcolumns = self.raw_data.valuesFromSchema()

            regex = self.raw_data.manualRegexCreation()

            self.raw_data.validationFileNameRaw(regex, LengthOfDateStampInFile, LengthOfTimeStampInFile)

            self.raw_data.validateColumnLength(noofcolumns)

            self.raw_data.validateMissingValuesInWholeColumn()
            self.log_writer.log(self.file_object, "Raw Data validation completed!!")

            self.log_writer.log(self.file_object, "Creating Prediction_Database and tables on the basis of given schema!!!")
            self.dBOperation.createTableDb('Prediction', column_names)
            self.log_writer.log(self.file_object, "Table creation completed!!")

            self.log_writer.log(self.file_object, 'Insertion of data into table started!!')
            self.dBOperation.insertIntoTableGoodData('Prediction')
            self.log_writer.log(self.file_object, "Insertion of data into table completed!!")

            self.log_writer.log(self.file_object, "Deleting Good Data folder!!")
            self.raw_data.deleteExistingGoodDataPredictionFolder()
            self.log_writer.log(self.file_object, "Good Data folder deleted!!")

            self.log_writer.log(self.file_object, "Moving bad files to Archive and deleting Bad_Data folder!!!")
            self.raw_data.moveBadFilesToArchiveBad()
            self.log_writer.log(self.file_object, "Bad files moved to archive!! Bad folder Deleted!!")
            self.log_writer.log(self.file_object, "Validation Operation completed!!")

            self.log_writer.log(self.file_object, "Extracting csv file from table")
            self.dBOperation.selectingDatafromtableintocsv('Prediction')
            self.log_writer.log(self.file_object, "File exported Successfully!!")
            self.file_object.close()
        except Exception as e:
            raise e