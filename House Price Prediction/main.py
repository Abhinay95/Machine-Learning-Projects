from flask import Flask, request, render_template
import pickle
app = Flask(__name__)
model = pickle.load(open('cbr.pkl', 'rb'))

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        bedrooms = int(request.form['bedrooms'])
        bathrooms = float(request.form['bathrooms'])
        livingRoomArea = int(request.form['livingRoomArea'])
        areaOfLot = int(request.form['areaOfLot'])
        floors = float(request.form['floors'])
        waterfront = request.form['waterfront']
        if waterfront == 'Yes':
            waterfront = 1
        else:
            waterfront = 0
        view = request.form['view']
        condition = request.form['condition']
        grade = request.form['grade']
        sqftAbove = int(request.form['sqftAbove'])
        year = int(request.form['year'])
        zipCode = int(request.form['zipCode'])
        lat = float(request.form['lat'])
        long = float(request.form['long'])
        livingRootSqFoot = int(request.form['livingRootSqFoot'])
        lotSquareFoot = int(request.form['lotSquareFoot'])

        prediction = model.predict([[bedrooms, bathrooms, livingRoomArea, areaOfLot, floors, waterfront, view, condition, grade,
                                     sqftAbove, year, zipCode, lat, long, livingRootSqFoot, lotSquareFoot]])
        output = round(prediction[0])

        if output > 0:
            return render_template('index.html', prediction_text = 'You can buy this house at {}'.format(output))
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)