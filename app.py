"""
 Created on 9:37 PM 7/14/2020 using PyCharm

 @author: Raj
"""
# importing the necessary dependencies
from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import pickle
# from sklearn.preprocessing import StandardScaler

app = Flask(__name__) # initializing a flask app

def predict_model(gre_score, toefl_score, university_rating, sop, lor, cgpa, is_research):

    if (is_research == 'yes'):
        research = 1
    else:
        research = 0
    filename = 'finalized_model.pickle'
    # filename1 = 'scalar_obj.pickle'
    loaded_model = pickle.load(open(filename, 'rb'))  # loading the model file from the storage
    scalar = pickle.load(open('scalar_model.pickle', 'rb'))
    # scalar = StandardScaler()
    # predictions using the loaded model file
    # prediction = loaded_model.predict(scalar.transform([[gre_score,toefl_score,university_rating,sop,lor,cgpa,research]]))
    prediction = loaded_model.predict([[gre_score, toefl_score, university_rating, sop, lor, cgpa, research]])
    return prediction

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/from_ui',methods=['POST','GET']) # route to show the predictions in a web UI
@cross_origin()
def from_ui():
    if request.method == 'POST':
        try:
            #  reading the inputs given by the user
            gre_score=float(request.form['gre_score'])
            toefl_score = float(request.form['toefl_score'])
            university_rating = float(request.form['university_rating'])
            sop = float(request.form['sop'])
            lor = float(request.form['lor'])
            cgpa = float(request.form['cgpa'])
            is_research = request.form['research']
            if is_research == 'yes':
                research = 1
            else:
                research = 0
            filename1 = 'finalized_model.pickle'
            filename2 = 'scalar_model.pickle'
            loaded_model = pickle.load(open(filename1, 'rb')) # loading the model file from the storage
            scalar = pickle.load(open(filename2, 'rb')) # loading the scalar model from the storage
            #scalar = StandardScaler()
            # predictions using the loaded model files
            prediction = loaded_model.predict(scalar.transform([[gre_score,toefl_score,university_rating,sop,lor,cgpa,research]]))
            #prediction = loaded_model.predict([[gre_score, toefl_score, university_rating, sop, lor, cgpa, research]])
            print('prediction is', prediction)
            # showing the prediction results in a UI
            return render_template('results.html', prediction=round(100*prediction[0]))

        except Exception as e:
            print('The Exception message is: ', e)
            return 'something is wrong'
    # return render_template('results.html')
    else:
        return render_template('index.html')


@app.route('/from_postman',methods=['POST','GET']) # route to show the predictions using RestAPI
@cross_origin()
def from_postman():
    if request.method == 'POST':
        #  reading the inputs given by the user
        gre_score = float(request.json['gre_score'])
        toefl_score = float(request.json['toefl_score'])
        university_rating = float(request.json['university_rating'])
        sop = float(request.json['sop'])
        lor = float(request.json['lor'])
        cgpa = float(request.json['cgpa'])
        is_research = request.json['research']

        prediction = predict_model(gre_score,toefl_score,university_rating,sop,lor,cgpa,is_research)
        print('prediction is', prediction)
        # showing the prediction results as a JSON response for the request made using REST API here Postman
        return jsonify({"Prediction" : prediction[0]})

if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
	app.run(debug=True) # running the app