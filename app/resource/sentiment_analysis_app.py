import aiohttp_jinja2
import json
import pandas as pd
from aiohttp import web

from app.service.data_preparation import ETL
from app.service.make_request import fetch_data_from_url
from app.service.ensemble_model import EnsembleModel


class Index(web.View):  # class for Index route
    @aiohttp_jinja2.template("index.html")
    async def get(self):  # get method to load the index.html
        return {'response': ""}

    @aiohttp_jinja2.template("index.html")
    async def post(self):  # post method to gather form data and detect emtion
        fetched_data = await self.request.post()  # fetched data from the textarea
        lst_message = [fetched_data['txt_area']]  # preparing list of the fetched data
        df = pd.DataFrame()
        df['message'] = lst_message  # storing fetched data into 'message' column
        etl_obj = ETL()  # create an object for ETL Process
        data = etl_obj.transform_data(df)  # transformation data
        model_obj = EnsembleModel(data)  # initialize object of EnsembleModel
        data, emotion_count = model_obj.ensemble_predicted_emotion()  # predict emotions on the messages
        message = data['message'].tolist()
        emotion = data['final_result'].tolist()
        context = {
            'message': message,
            'emotion': emotion,
        }
        return {'response': context}


class Dashboard(web.View):  # class for Dashboard route
    @aiohttp_jinja2.template("dashboard.html")
    async def get(self):  # get method for make requests and detect emotion
        fetched_data = fetch_data_from_url(self.request.match_info['time'])  # make request and fetched data from server
        print(self.request.match_info['time'])
        data = json.loads(fetched_data)  # converting fetched_data into json format
        etl_obj = ETL()
        data = etl_obj.extract_data(data)  # extract data from json format
        data = etl_obj.transform_data(data)  # transformation of extracted data
        data = etl_obj.extract_customer_responses()  # extracting customer responses from the data
        model_obj = EnsembleModel(data)  # initialize object of EnsembleModel
        data, emotion_count = model_obj.ensemble_predicted_emotion()  # predict emotions on the messages
        message = data['message'].tolist()
        emotion = data['final_result'].tolist()
        context = {
            'message': message,
            'emotion': emotion,
            'emotion_count': emotion_count
        }
        return {'response': context}
