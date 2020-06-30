import pandas as pd
import numpy as np
from data_preprocessing import preprocessing
from application_logging import logger
from Prediction_Raw_Data_Validation.predictionDataValidation import Prediction_Data_validation
from file_operations import file_methods
from data_ingestion import data_loader_prediction

class prediction:
    def __init__(self, path):
        self.file_object = open("Prediction_Logs/Prediction_Log.txt", 'a+')
        self.log_writer = logger.App_Logger()
        self.pred_data_val = Prediction_Data_validation(path)

    def predictionFromModel(self):
        try:
            self.pred_data_val.deletePredictionFile()
            self.log_writer.log(self.file_object, 'Start of Prediction')
            data_getter = data_loader_prediction.Data_Getter_Pred(self.file_object, self.log_writer)
            data = data_getter.get_data()

            preprocessor = preprocessing.Preprocessor(self.file_object, self.log_writer)
            data = preprocessor.remove_columns(data, ['policy_number', 'policy_bind_date', 'policy_state', 'insured_zip',
                                                'incident_location', 'incident_date', 'incident_state', 'incident_city',
                                                'insured_hobbies', 'auto_make', 'auto_model', 'auto_year', 'age',
                                                'total_claim_amount'])
            data.replace('?', np.NaN, inplace=True)

            is_null_present, cols_with_missing_values = preprocessor.is_null_present(data)

            if (is_null_present):
                data = preprocessor.impute_missing_values(data, cols_with_missing_values)

            data = preprocessor.encode_categorical_columns(data)
            data = preprocessor.scale_numerical_columns(data)

            file_loader = file_methods.File_Operation(self.file_object, self.log_writer)
            kmeans =file_loader.load_model('KMeans')

            clusters = kmeans.predict(data)
            data['clusters'] =clusters
            clusters = data['clusters'].unique()
            predictions = []
            for i in clusters:
                cluster_data = data[data['clusters']==i]
                cluster_data = cluster_data.drop(['clusters'], axis=1)
                model_name = file_loader.find_correct_model_file(i)
                model = file_loader.load_model(model_name)
                result = (model.predict(cluster_data))
                for res in result:
                    if res == 0:
                        predictions.append('N')
                    else:
                        predictions.append('Y')
            final =pd.DataFrame(list(zip(predictions)), columns=['Predictions'])
            path = "Prediction_Output_File/Predictions.csv"
            final.to_csv("Prediction_Output_File/Predictions.csv",header=True,mode='a+')
            self.log_writer.log(self.file_object, 'End of Prediction')
        except Exception as ex:
            self.log_writer.log(self.file_object,'Error occured while running the prediction!! Error:: %s' % ex)
            raise ex
        return path