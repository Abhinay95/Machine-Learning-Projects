from application_logging import logger
import pandas as pd
from Prediction_Raw_Data_Validation.predictionDataValidation import Prediction_Data_Validation
from data_ingestion.data_loader_prediction import Data_Getter_Pred
from data_preprocessing import preprocessing
from file_operations import file_methods

class Prediction:
    def __init__(self, path):
        self.log_writer = logger.AppLogger()
        self.file_object = open("Prediction_Logs/Prediction_Log.txt", 'a+')
        self.pred_data_val = Prediction_Data_Validation(path)

    def predictionFromModel(self):
        try:
            self.pred_data_val.deletePredictionFile()
            self.log_writer.log(self.file_object, "Start of Prediction!!")
            data_getter = Data_Getter_Pred(self.file_object, self.log_writer)
            data = data_getter.get_data()

            preprocessor = preprocessing.Preprocessor(self.file_object, self.log_writer)

            data = preprocessor.replaceInvalidValuesWithNull(data)

            is_null_present, cols_with_missing_values = preprocessor.is_null_present(data)

            if(is_null_present):
                data = preprocessor.impute_missing_values(data, cols_with_missing_values)

            file_loader = file_methods.File_Operation(self.file_object, self.log_writer)
            kmeans =file_loader.load_model('KMeans')

            clusters = kmeans.predict(data)
            data['clusters'] = clusters
            clusters = data['clusters'].unique()
            results = []

            for i in clusters:
                cluster_data = data[data['clusters']==i]
                cluster_data = cluster_data.drop(['clusters'],axis=1)
                model_name = file_loader.find_correct_model_file(i)
                model =file_loader.load_model(model_name)
                for val in (model.predict(cluster_data)):
                    results.append(val)
            results = pd.DataFrame(results, columns=['Predictions'])
            path = "Prediction_Output_File/Predictions.csv"
            results.to_csv("Prediction_Output_File/Predictions.csv",header=True)
            self.log_writer.log(self.file_object, 'End of Prediction')
        except Exception as e:
            self.log_writer.log(self.file_object, 'Error occured while running the prediction!! Error:: %s' % e)
            raise e
        return path