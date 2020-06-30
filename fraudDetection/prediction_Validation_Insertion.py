from datetime import datetime
from Prediction_Raw_Data_Validation.predictionDataValidation import Prediction_Data_validation
from DataTransformation_Prediction.DataTransformationPrediction import dataTransformPredict
from DataTypeValidation_Insertion_Prediction.DataTypeValidationPrediction import dBOperation
from application_logging import logger

class pred_validation:
    def __init__(self,path):
        self.raw_data = Prediction_Data_validation(path)
        self.dataTransform = dataTransformPredict()
        self.dBOperation = dBOperation()
        self.file_object = open("Prediction_Logs/Prediction_Log.txt", 'a+')
        self.log_writer = logger.App_Logger()
        
    def prediction_validation(self):
        try:
            self.log_writer.log(self.file_object, 'Start of Validation on files for prediction!!')
            LengthOfDateStampInFile,LengthOfTimeStampInFile,column_names,noofcolumns = self.raw_data.valuesFromSchema()

            regex = self.raw_data.manualRegexCreation()

            self.raw_data.validationFileNameRaw(regex,LengthOfDateStampInFile, LengthOfTimeStampInFile)

            self.raw_data.validateColumnLength(noofcolumns)

            self.raw_data.validateMissingValuesInWholeColumn()
            self.log_writer.log(self.file_object, "Raw Data validation complete!!")

            self.log_writer.log(self.file_object, "Starting Data transformation!!")
            self.dataTransform.replaceSingleQuotesToDouble()
            self.log_writer.log(self.file_object, "DataTransformation Completed!!!")

            self.log_writer.log(self.file_object,
                                "Creating Prediction_Database and tables on the basis of given schema!!!")
            self.dBOperation.createTableDb('Prediction', column_names)
            self.log_writer.log(self.file_object, "Table creation Completed!!")

            self.log_writer.log(self.file_object, "Insertion of Data into Table started!!!!")
            self.dBOperation.insertIntoTableGoodData('Prediction')
            self.log_writer.log(self.file_object, "Insertion in Table completed!!!")

            self.log_writer.log(self.file_object, "Deleting Good Data Folder")
            self.raw_data.deleteExistingGoodDataPredictingFolder()
            self.log_writer.log(self.file_object, "Good_Data folder deleted!!!")

            self.log_writer.log(self.file_object, "Moving bad files to Archive and deleting Bad_Data folder!!!")
            self.raw_data.moveBadFilesToArchiveBad()
            self.log_writer.log(self.file_object, "Bad files moved to archive!! Bad folder Deleted!!")
            self.log_writer.log(self.file_object, "Validation Operation completed!!")

            self.log_writer.log(self.file_object, "Extracting csv file from table")
            self.dBOperation.selectingDatafromtableintocsv('Prediction')

        except Exception as e:
            raise e