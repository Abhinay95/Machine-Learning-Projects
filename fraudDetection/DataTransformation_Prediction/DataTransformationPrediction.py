from datetime import datetime
import pandas
from os import listdir
from application_logging.logger import App_Logger

class dataTransformPredict:
    def __init__(self):
        self.goodDataPath = "Prediction_Raw_Files_Validated/Good_Raw"
        self.logger = App_Logger()

    def replaceSingleQuotesToDouble(self):
        try:
            log_file = open("Prediction_Logs/dataTransformLog.txt", 'a+')
            onlyfiles = [f for f in listdir(self.goodDataPath)]
            for file in onlyfiles:
                data = pandas.read_csv(self.goodDataPath + '/' + file)
                columns = ["policy_bind_date","policy_state","policy_csl","insured_sex","insured_education_level","insured_occupation","insured_hobbies","insured_relationship","incident_state","incident_date","incident_type","collision_type","incident_severity","authorities_contacted","incident_city","incident_location","property_damage","police_report_available","auto_make","auto_model"]

                for col in columns:
                    data[col] = data[col].apply(lambda x: "'" + str(x) + "'")
                data.to_csv(self.goodDataPath + '/' + file, index=None, header=True)
                self.logger.log(log_file, " %s: File Transformed successfully!!" % file)

        except Exception as e:
            self.logger.log(log_file, "Data Transformation failed because:: %s" % e)
            log_file.close()
            raise e
        log_file.close()


