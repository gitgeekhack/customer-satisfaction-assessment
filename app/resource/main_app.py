import json
from flask import render_template, request, Blueprint
from wtforms import Form, StringField, validators
from wtforms.widgets import TextArea

from app.services.data_preparation import ETL
from app.services.make_request import fetch_data_from_url
from app.services.prepare_model import PrepareModel

global data  # for storing messages
flask_app = Blueprint('main_app', __name__)  # create a blueprint of an application


class GetData(Form):  # get data form for the textarea
    txt_field = StringField("Data", [validators.DataRequired()], widget=TextArea())


@flask_app.route("/", methods=['GET', 'POST'])  # index route
def get_data_route():  # method for fetching data from the textarea
    global data
    form = GetData(request.form)
    if request.method == 'POST' and form.validate():  # if data is valid then process further
        data = form.txt_field.data  # fetching data from the textarea
        try:
            data = json.loads(data)
            etl_obj = ETL()
            data, length_of_message = etl_obj.extract_data(data)  # extract JSON data from the file.
            return render_template("loading.html", length=length_of_message)
        except ValueError as e:
            print("Exception Occurred! {}".format(e))
    return render_template("getData.html", form=form)


# perform emotion detection on the json data
@flask_app.route("/processed_data", methods=['GET', 'POST'])
def perform_operation():
    global data
    etl_obj = ETL()  # init object for ETL process
    data = etl_obj.transform_data(data)  # transform data for our purpose
    data = etl_obj.extract_customer_responses()  # extract customer responses from the data
    model_obj = PrepareModel(data)  # initialize object of PrepareModel
    data, emotion_count = model_obj.predict_emotion()  # predict emotions on the messages

    message = list(data['message'])
    emotion = list(data['emotion'])
    return render_template("displayDetection.html", message=message, emotion=emotion,
                           emotion_cnt=emotion_count)


@flask_app.route("/<time>", methods=['GET', 'POST'])  # time route
def gather_data(time):
    global data
    time_dict = {'15m': '15 Minutes', '30m': '30 Minutes', "1h": "1 Hour", "3h": "3 Hours",
                 "6h": "6 Hours", "12h": "12 Hours", "24h": "24 Hours"}

    fetched_data = fetch_data_from_url(time)  # fetched data from the server
    try:
        data = json.loads(fetched_data)
        etl_obj = ETL()  # init object for ETL process
        data, length_of_message = etl_obj.extract_data(data)  # extract JSON data from the file.
        return render_template("loading.html", length=length_of_message)
    except ValueError as e:
        print("Not a Valid Data! {}".format(e))

# # perform emotion detection on the json data
# @flask_app.route("/processed_data", methods=['GET', 'POST'])
# def perform_operation_dashboard():
#     global data
#     etl_obj = ETL()  # init object for ETL process
#
#     data = etl_obj.transform_data(data)  # transform data for our purpose
#     data = etl_obj.extract_customer_responses()  # extract customer responses from the data
#     model_obj = PrepareModel(data)  # initialize object of PrepareModel
#     data, emotion_count = model_obj.predict_emotion()
#
#     return render_template("dashboard.html", emotion_cnt=emotion_count)
