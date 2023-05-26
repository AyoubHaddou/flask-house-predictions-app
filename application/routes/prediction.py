from flask import Blueprint, render_template, request
from flask_login import current_user
import pandas as pd
import joblib
from application import db 
from application.forms.prediction import  PredictionForm
from application.database.prediction import Prediction
from application.helpers.preprocessing import (data_engineering, data_preprocessing, features_selection, neighbors_dict, 
                                               conditions_dict, sale_condition_dict, clean_columns)

model = joblib.load(open('model/fit/model_16790.joblib', 'rb'))
prediction = Blueprint('prediction', __name__, url_prefix='/prediction')

@prediction.route('/')
def index():
    return render_template('prediction.html', form=PredictionForm())

@prediction.route('/predict', methods=['GET', 'POST'])
def predict():
    form = PredictionForm()
    keys = [i for i in form._fields if i not in ['submit', 'csrf_token']]
    pred = 0
    if form.submit():
        dict_prediction = {}
        for key in keys:
            dict_prediction[key]= form[key].data
        df_prediction = pd.DataFrame(dict_prediction, index=[0])
        # Voir pour changer les noms des colonnnes idem avant de fit le model ? 
        df_prediction = features_selection(data_engineering(data_preprocessing(clean_columns(df_prediction), neighbors_dict, conditions_dict, sale_condition_dict)))
        pred = int(model.predict(df_prediction))
        dict_prediction['price'] = pred
        Prediction(**dict_prediction, user_id=current_user.id).save_to_db()
    return render_template('prediction.html', data=f'{pred} $', form=form)



@prediction.route('/history', methods=['GET','POST'])
def history():
    prediction_id = request.args.get('id')
    if prediction_id:
        Prediction.query.filter(Prediction.id == prediction_id).first().delete_from_db()
        print("user deleted")
    predictions = db.session.query(Prediction).where(Prediction.user_id == current_user.id).all()
    return render_template('history.html', predictions=predictions)
    