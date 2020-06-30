from flask import Flask, request, Response
from flask_cors import CORS, cross_origin
import flask_monitoringdashboard as dashboard
import os
from training_Validation_Insertion import train_validation
from trainingModel import trainModel
from prediction_Validation_Insertion import pred_validation
from predictFromModel import Prediction
from wsgiref import simple_server


os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
dashboard.bind(app)
CORS(app)

@app.route('/predict', methods=['POST'])
@cross_origin()
def predictClientRoute():
    try:
        if request.json['folderPath'] is not None:
            path = request.json['folderPath']
            predict_valObj = pred_validation(path)
            predict_valObj.prediction_validation()

            pred = Prediction(path)
            path = pred.predictionFromModel()
            return Response("Prediction File created at %s!!!" % path)

    except ValueError:
        return Response("Error Occurred! %s" %ValueError)
    except KeyError:
        return Response("Error Occurred! %s" %KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" %e)

@app.route('/train', methods=['POST'])
@cross_origin()
def trainClientRoute():
    try:
        if request.json['folderPath'] is not None:
            path =request.json['folderPath']
            train_valObj = train_validation(path)
            train_valObj.train_Validation()

            train_modelObj = trainModel()
            train_modelObj.trainingModel()


    except ValueError:

        return Response("Error Occurred! %s" % ValueError)

    except KeyError:

        return Response("Error Occurred! %s" % KeyError)

    except Exception as e:

        return Response("Error Occurred! %s" % e)
    return Response("Training successfull!!")

port = int(os.getenv("PORT", 5001))
if __name__ == '__main__':
    app.run(port=port, debug=True)