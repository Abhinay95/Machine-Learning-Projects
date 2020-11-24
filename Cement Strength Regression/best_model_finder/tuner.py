from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score

class Model_Finder:
    def __init__(self, file_object, logger_object):
        self.file_object = file_object
        self.logger_object = logger_object
        self.lr = LinearRegression()
        self.rf = RandomForestRegressor()

    def get_best_params_for_linearReg(self, train_X, train_y):
        self.logger_object.log(self.file_object, 'Entered the get_best_params_for_linearReg method of the Model_Finder class')
        try:
            self.param_grid_lr = {
                'fit_intercept' : [True, False], 'normalize' : [True, False], 'copy_X' : [True, False]
            }
            self.grid = GridSearchCV(estimator=self.lr, param_grid=self.param_grid_lr, verbose=3, cv=5)
            self.grid.fit(train_X, train_y)

            self.fit_intercept = self.grid.best_params_['fit_intercept']
            self.normalize = self.grid.best_params_['normalize']
            self.copy_X = self.grid.best_params_['copy_X']

            self.linreg = LinearRegression(fit_intercept=self.fit_intercept, normalize=self.normalize, copy_X=self.copy_X)
            self.linreg.fit(train_X, train_y)
            self.logger_object.log(self.file_object, 'LinearRegression best params: ' + str(
                                       self.grid.best_params_) + '. Exited the get_best_params_for_linearReg method of the Model_Finder class')
            return self.linreg
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in get_best_params_for_linearReg method of the Model_Finder class. Exception message:  ' + str(
                                       e))
            self.logger_object.log(self.file_object,
                                   'LinearReg Parameter tuning  failed. Exited the get_best_params_for_linearReg method of the Model_Finder class')
            raise Exception()

    def get_best_params_for_Random_Forest_Regressor(self, train_X, train_y):
        self.logger_object.log(self.file_object, 'Entered the RandomForestReg method of the Model_Finder class')
        try:
            self.param_grid_rf = {
                                "n_estimators": [10,20,30],
                                "max_features": ["auto", "sqrt", "log2"],
                                "min_samples_split": [2,4,8],
                                "bootstrap": [True, False]
                                                     }
            self.grid = GridSearchCV(estimator=self.rf, param_grid=self.param_grid_rf, verbose=3, cv=5)
            self.grid.fit(train_X, train_y)

            self.n_estimators = self.grid.best_params_['n_estimators']
            self.max_features = self.grid.best_params_['max_features']
            self.min_samples_split = self.grid.best_params_['min_samples_split']
            self.bootstrap = self.grid.best_params_['bootstrap']

            self.rfr = RandomForestRegressor(n_estimators=self.n_estimators, max_features=self.max_features, min_samples_split=self.min_samples_split, bootstrap=self.bootstrap)
            self.rfr.fit(train_X, train_y)
            self.logger_object.log(self.file_object,
                               'RandomForestRegressor best params: ' + str(
                                   self.grid.best_params_) + '. Exited the get_best_params_for_linearReg method of the Model_Finder class')
            return self.rfr
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in RandomForestReg method of the Model_Finder class. Exception message:  ' + str(
                                       e))
            self.logger_object.log(self.file_object,
                                   'RandomForestReg Parameter tuning  failed. Exited the knn method of the Model_Finder class')
            raise Exception()


    def get_best_model(self, train_X, train_y, test_X, test_y):
        self.logger_object.log(self.file_object, 'Entered the get_best_model method of the Model_Finder class')
        try:
            #Linear Regression
            self.LinearReg = self.get_best_params_for_linearReg(train_X, train_y)
            self.prediction_LinearReg = self.LinearReg.predict(test_X)
            self.LinearReg_error = r2_score(test_y, self.prediction_LinearReg)

            #Random Forest Regression
            self.rfReg = self.get_best_params_for_Random_Forest_Regressor(train_X, train_y)
            self.prediction_rfReg = self.rfReg.predict(test_X)
            self.rfReg_error = r2_score(test_y, self.prediction_rfReg)

            if(self.LinearReg_error < self.rfReg_error):
                return 'RandomForestRegressor', self.rfReg
            else:
                return 'LinearRegression', self.LinearReg

        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in get_best_model method of the Model_Finder class. Exception message:  ' + str(
                                       e))
            self.logger_object.log(self.file_object,
                                   'Model Selection Failed. Exited the get_best_model method of the Model_Finder class')
            raise Exception()
