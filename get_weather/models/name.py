# coding: utf-8
# Part of CAPTIVEA. Odoo 12 EE.
from odoo import _, api
from odoo.models import *
from odoo import fields, models
from odoo import http
from datetime import datetime,timedelta
import requests

class class_name(AbstractModel):
    _inherit = 'base'
    @api.model
    def get_weather(self,zipcode,date_time):
        # Enter your API key here
        api_key = "4a8319f9023e1cbf1f38ed381b532dd7"
        currennt=date_time-datetime.now()>timedelta(hours=3)

        if currennt:
            if datetime.now()>date_time or date_time-datetime.now()>timedelta(days=5):
                return "Invalid date"
            base_url = "http://api.openweathermap.org/data/2.5/forecast?"
        else:
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
        # complete url address
        complete_url = base_url + "appid=" + api_key + "&zip=" + str(zipcode)+',us'+"&lang=en"
        # get method of requests module
        # return response object
        response = requests.get(complete_url)
        json_data = response.json()
        if currennt:
            location_data = {
                'city': json_data['city']['name'],
                'country': json_data['city']['country']
            }

            json_data['list'].sort(key=lambda x:abs(datetime.strptime(x['dt_txt'],'%Y-%m-%d %H:%M:%S')-date_time))
            item = json_data['list'][0]
            time = item['dt_txt']
        else:
            item=json_data
            time=datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d %X')
            location_data = {
                'city': item['name'],
                'country': item['sys']['country']
            }
        # Temperature is measured in Kelvin
        temperature = item['main']['temp']
        temperature= '%.2f' % (temperature * 9/5 - 459.67)+'°F'
        weather = item['weather'][0]['main']
        description = item['weather'][0]['description']
        return {"Time":time,"Weather":weather,"Description":description,"Temperature":temperature,"Location":location_data}
