from flask import Flask, render_template, jsonify, request, Response
from flask_cors import CORS, cross_origin
import os
from wsgiref import simple_server
import flask_monitoringdashboard as dashboard
from training_Validation_Insertion import train_validation
from trainingModel import trainModel
from prediction_Validation_Insertion import pred_validation
from predictFromModel import prediction

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
dashboard.bind(app)
CORS(app)

@app.route('/', methods = ['GET'])
@cross_origin(app)
def home():
    return render_template('index.html')

@app.route('/train', methods=['POST'])
@cross_origin(app)
def trainRouteClient():
    try:
        if request.json['folderPath'] is not None:
            path = request.json['folderPath']
            train_valObj = train_validation(path)
            train_valObj.train_validation()

            train_modelObj = trainModel()
            train_modelObj.trainingModel()

    except ValueError:

        return Response("Error Occurred! %s" % ValueError)

    except KeyError:

        return Response("Error Occurred! %s" % KeyError)

    except Exception as e:

        return Response("Error Occurred! %s" % e)
    return Response("Training successfull!!")

@app.route('/predict', methods=['POST'])
@cross_origin(app)
def predictClientRoute():
    try:
        if request.json['folderPath'] is not None:
            path = request.json['folderPath']
            pred_valObj = pred_validation(path)
            pred_valObj.prediction_validation()

            pred_model = prediction(path)
            pred_model.predictionFromModel()
            return Response("Prediction file created at %s!!!" % path)


    except ValueError:
        return Response("Error Occurred! %s" %ValueError)
    except KeyError:
        return Response("Error Occurred! %s" %KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" %e)



if __name__ == '__main__':
    app.run(debug=True)
