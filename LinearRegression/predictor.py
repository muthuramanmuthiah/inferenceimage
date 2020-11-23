from flask import Flask, request, jsonify, Response
import pickle
import os
import json
import boto3
import logging

#Define the path
prefix = '/opt/ml/'
model_path = os.path.join(prefix, 'model/')
logging.info("Model Path" + str(model_path))

# Load the model components
# regressor = joblib.load(os.path.join(model_path, 'model.pkl'))
regressor=pickle.load(open(model_path+'model.pkl','rb'))
logging.info("Regressor" + str(regressor))

app=Flask(__name__)


@app.route('/ping', methods=['GET'])
def ping():
    # Check if the classifier was loaded correctly
    try:
        status = 200
        logging.info("Status : 200")
    except:
        status = 400
    return Response(response= json.dumps(' '), status=status, mimetype='application/json' )

@app.route('/invocations', methods=['POST'])
def transformation():
    ''' Method calling Model '''

    #Get input data
    data=request.get_json(force=True)
    l=data['input'].split(',')
    l_int = [[ int(x) for x in l ]]
    
    #predict
    outcome = regressor.predict(l_int)
    result = {
        'output': outcome[0]
        }
    j_outcome= json.dumps(result)
    return Response(response=j_outcome, status=200, mimetype='application/json')





