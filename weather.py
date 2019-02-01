from tkinter import*
import locale
import threading
import requests
import json
#import Adafruit_DHT as dht
from configparser import SafeConfigParser
import traceback
from PIL import Image, ImageTk
from contextlib import contextmanager

class Weather(Frame):

    @contextmanager
    def setLocale(name):
        with LOCALE_LOCK:
            saved = locale.setLocale(locale.LC_ALL)
            try:
                yield locale.setLocale(locale.LC_ALL, name)
            finally:
                locale.setLocale(locale.LC_ALL, saved)

    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')

        self.LOCALE_LOCK = threading.Lock()

        config = 'config.ini'
        self.parser = SafeConfigParser()
        self.parser.read(config)

        self.ui_locale = ''
        self.weather_api_token = self.parser.get('creds', 'token')
        self.ip_api_token = self.parser.get('creds', 'token2')
        self.weather_lang = 'en'
        self.weather_unit = 'si'
        self.latitude = '65.01236' #You can set this to None if IP tracing works well
        self.longitude = '25.46816' #You can set this to None if IP tracing works well
        self.temperature = ''
        self.apparentTemp = ''
        self.forecast = ''
        self.location = ''
        self.currently = ''
        self.icon = ''
        self.indoorHumi = ''
        self.indoorTemp = ''
        self.degreeFrm = Frame(self, bg='black')
        self.degreeFrm.pack(side=LEFT, anchor=E)
        self.temperatureLbl = Label(self.degreeFrm, font=('Helvetica', 94), fg='white', bg='black')
        self.temperatureLbl.pack(side=LEFT, anchor=N)
        self.apparentTempLbl = Label(self.degreeFrm, font=('Helvetica', 18), fg='white', bg='black')
        self.apparentTempLbl.pack(side=LEFT, anchor=S)
        self.iconLbl = Label(self.degreeFrm, bg='black')
        self.iconLbl.pack(side=LEFT, anchor=N, padx=20)
        self.currentlyLbl = Label(self, font=('Helvetica', 28), fg='white', bg='black')
        self.currentlyLbl.pack(side=TOP, anchor=W)
        self.forecastLbl = Label(self, font=('Helvetica', 18), fg='white', bg='black')
        self.forecastLbl.pack(side=TOP, anchor=W)
        self.locationLbl = Label(self, font=('Helvetica', 18), fg='white', bg='black')
        self.locationLbl.pack(side=TOP, anchor=W)
        self.indoorLbl = Label(self, font=('Helvetica', 18), fg='white', bg='black')
        self.indoorLbl.pack(side=LEFT, anchor=S)
        self.get_weather()
        #self.get_indoor_temperature()

    def get_ip(self):
        try:
            ip_url = 'http://jsonip.com/'
            req = requests.get(ip_url)
            ip_json = json.loads(req.text)
            return ip_json['ip']
            print(ip_json)
        except Exception as e:
            traceback.print_exc()
            return 'Error: %s. Cannot get ip.' % e

    def get_weather(self):

        #Outdoor weather
        try:
            icon_lookup = {
                'clear-day': "assets/Sun.png",
                'wind': "assets/Wind.png",
                'cloudy': "assets/Cloud.png",
                'partly-cloudy-day': "assets/PartlySunny.png",
                'rain': "assets/Rain.png",
                'snow': "assets/Snow.png",
                'snow-thin': "assets/Snow.png",
                'fog': "assets/Haze.png",
                'clear-night': "assets/Moon.png",
                'partly-cloudy-night': "assets/PartlyMoon.png",
                'thunderstorm': "assets/Storm.png",
                'tornado': "assests/Tornado.png",
                'hail': "assests/Hail.png"
            }
            if self.latitude is None and self.longitude is None:
                location_req_url = 'http://api.ipstack.com/%s?access_key=%s' %(self.get_ip(), self.ip_api_token)
                r = requests.get(location_req_url)
                location_obj = json.loads(r.text)
                lat = location_obj['latitude']
                lon = location_obj['longitude']
                location2 = '%s, %s' % (location_obj['city'], location_obj['region_code'])
                weather_req_url = 'https://api.darksky.net/forecast/{}/{},{}?lang={}&units={}'.format(self.weather_api_token, lat, lon, self.weather_lang, self.weather_unit)
            else:
                location2 = ''
                weather_req_url = 'https://api.darksky.net/forecast/{}/{},{}?lang={}&units={}'.format(self.weather_api_token, self.latitude, self.longitude, self.weather_lang, self.weather_unit)

            r = requests.get(weather_req_url)
            weather_obj = json.loads(r.text)

            degree_sign=u'\N{DEGREE SIGN}'
            temperature2 = "%s%s" % (str(int(weather_obj['currently']['temperature'])), degree_sign)
            apparentTemp2 = "%s%s" % (str(int(weather_obj['currently']['apparentTemperature'])), degree_sign)
            currently2 = weather_obj['currently']['summary']
            forecast2 = weather_obj['hourly']['summary']

            icon_id = weather_obj['currently']['icon']
            icon2 = None

            if icon_id in icon_lookup:
                icon2 = icon_lookup[icon_id]
            else:
                print("Couldnt get the image")

            if icon2 is not None:
                if self.icon != icon2:
                    self.icon = icon2
                    image = Image.open(icon2)
                    image = image.resize((100,100), Image.ANTIALIAS)
                    image = image.convert('RGB')
                    photo = ImageTk.PhotoImage(image)

                    self.iconLbl.config(image=photo, text=None)
                    self.iconLbl.image = photo

                    print("Updated icon")
                else:
                    print("No icon update needed")
                    pass
            else:
                self.iconLbl.config(text='ERR')

            if self.currently != currently2:
                    self.currently = currently2
                    self.currentlyLbl.config(text=currently2)
            if self.forecast != forecast2:
                    self.forecast = forecast2
                    self.forecastLbl.config(text=forecast2)
            if self.temperature != temperature2:
                    self.temperature = temperature2
                    self.temperatureLbl.config(text=temperature2)
            if self.apparentTemp != apparentTemp2:
                    self.apparentTemp = apparentTemp2
                    self.apparentTempLbl.config(text=apparentTemp2)
            if self.location != location2:
                if location2 == ', ':
                    self.location = 'Cannot pinpoint location'
                    self.locationLbl.config(text='Cannot pinpoint location')
                else:
                    self.location = location2
                    self.locationLbl.config(text=location2)


        except Exception as e:
            traceback.print_exc()
            print ('Error: %s. Cannot get weather.' % e)

        self.after(600000, self.get_weather)

    '''def get_indoor_temperature(self):
        try:
            indoorHumi2, indoorTemp2 = dht.read_retry(11,4)
            if self.indoorTemp != indoorTemp2:
                self.indoorTemp = indoorTemp2
                tempString = "Indoor temperature: {}{}".format(self.indoorTemp, degree_sign)
                self.indoorLbl.config(text=tempString)
                print('Indoor temp updated')
            else:
                print('No indoor temperature update needed')

        except (Exception) as e:
            traceback.print_exc()
            print('Error: %s. Cannot get indoor temperature' % e)

        self.after(300000, self.get_indoor_temperature)'''


    @staticmethod
    def conver_kelvin_to_farenheit(kelvin_temp):
        return 1.8 * (kelvin_temp - 273) + 32
