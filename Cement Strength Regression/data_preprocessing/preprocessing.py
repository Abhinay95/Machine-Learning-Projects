import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler

class Preprocessor:
    def __init__(self, file_object, logger_object):
        self.file_object = file_object
        self.logger_object = logger_object

    def is_null_present(self, data):
        self.logger_object.log(self.file_object, 'Entered the is_null_present method of the Preprocessor class')
        self.null_present = False
        self.column_with_missing_values = []
        self.columns = data.columns

        try:
            self.null_counts = data.isna().sum()
            for i in range(len(self.null_counts)):
                if self.null_counts[i] > 0:
                    self.null_present = True
                    self.column_with_missing_values.append(self.columns[i])
            if(self.null_present):
                self.dataframe_with_null = pd.DataFrame()
                self.dataframe_with_null['columns'] = data.columns
                self.dataframe_with_null['missing_values_counts'] = np.array(data.isna().sum())
                self.dataframe_with_null.to_csv('preprocessing_data/null_values.csv')
            self.logger_object.log(self.file_object, 'Finding missing values is a success.Data written to the null values file. Exited the is_null_present method of the Preprocessor class')
            return self.null_present, self.column_with_missing_values
        except Exception as e:
            self.logger_object.log(self.file_object, 'Exception occured in is_null_present method of the Preprocessor class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object, 'Finding missing values failed. Exited the is_null_present method of the Preprocessor class')
            raise Exception()

    def impute_missing_values(self, data):
        self.logger_object.log(self.file_object, 'Entered the impute_missing_values method of the Preprocessor class')
        self.data = data
        try:
            imputer = KNNImputer(n_neighbors=3, weights='uniform', missing_values= np.nan)
            self.new_array = imputer.fit_transform(self.data)
            self.new_data = pd.DataFrame(data = (self.new_array), columns= self.data.columns)
            self.logger_object.log(self.file_object, 'Imputing missing values Successful. Exited the impute_missing_values method of the Preprocessor class')
            return self.new_data
        except Exception as e:
            self.logger_object.log(self.file_object, 'Exception occured in impute_missing_values method of the Preprocessor class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object, 'Imputing missing values failed. Exited the impute_missing_values method of the Preprocessor class')
            raise Exception()

    def separate_label_feature(self, data, label_column_name):
        self.logger_object.log(self.file_object, 'Entered the separate_label_feature method of the Preprocessor class')
        try:
            self.X = data.drop(labels = label_column_name, axis=1)
            self.y = data[label_column_name]
            self.logger_object.log(self.file_object, 'Label Separation Successful. Exited the separate_label_feature method of the Preprocessor class')
            return self.X, self.y
        except Exception as e:
            self.logger_object.log(self.file_object, 'Exception occured in separate_label_feature method of the Preprocessor class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object, 'Label Separation Unsuccessful. Exited the separate_label_feature method of the Preprocessor class')
            raise Exception()

    def logTransformation(self, X):
        for column in X.columns:
            X[column] += 1
            X[column] = np.log(X[column])
        return X

    def standardScalingData(self, X):
        scalar = StandardScaler()
        X_scaled = scalar.fit_transform(X)
        return X_scaled
