# Copyright (c) 2021 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import CliExtension
import datetime
import json
import requests
import urllib

class Weather:

   def __init__(self, url=None, apikey=None, locationsfile=None):
      self.url = url
      self.apikey = apikey
      self.locationsfile = locationsfile
      if locationsfile is not None:
         with open(self.locationsfile) as json_file:
            self.locations = json.load(json_file)

   def print_location(self, data=None):
      print("name {}".format(data["name"]))
      print("id {}".format(data["id"]))
      print("pressure {} bar".format(data["pressure"]))
      print("sunset {} UTC".format(data["sunset"]))
      print("sunrise {} UTC".format(data["sunrise"]))
      print("temp {} C".format(data["temp"]))
      print("temp_min {} C".format(data["temp_min"]))
      print("temp_max {} C".format(data["temp_max"]))
      print("feels_like {} C".format(data["feels_like"]))
      print("humidity {} %".format(data["humidity"]))

   def show_weather_locations(self):
      return([ {"name":x["name"], "id": x["id"], "country": x["country"], 
                "lat": x["coord"]["lat"], "lon": x["coord"]["lon"] } 
                for x in self.locations ])

   def show_weather_location(self,location_id=None, location_name=None):
      if location_id is not None:
         d = { "id": location_id, }
      if location_name is not None:
         d = { "q": location_name, }
      d["units"] = "metric"
      d["appid"] = self.apikey
      d_encoded = urllib.urlencode(d)
      url = "{}?{}".format(self.url, d_encoded)
      r = requests.get(url)
      r_json = r.json()
      # DEBUG
      # print(url)
      # print(r_json)
      resp = r_json["main"]
      sunset = r_json["sys"]["sunset"]
      resp["sunset"] = str(datetime.datetime.utcfromtimestamp(sunset).\
                           strftime('%Y-%m-%d %H:%M:%S'))
      sunrise = r_json["sys"]["sunrise"]
      resp["sunrise"] = str(datetime.datetime.utcfromtimestamp(sunrise).\
                            strftime('%Y-%m-%d %H:%M:%S'))
      resp["name"] = r_json["name"]
      resp["id"] = r_json["id"]

      return(resp)

class ShowWeatherLocationsCmd(CliExtension.ShowCommandClass):

   def handler(self, ctx):
      daemon = ctx.getDaemon("WeatherDaemon")
      if daemon is None:
         ctx.addError("unable to get WeatherDaemon info")
         return(None)
      locationsfile = daemon.config.config("locationsfile")

      w = Weather(url=None, apikey=None, locationsfile=locationsfile)

      return(w.show_weather_locations())

   def render(self, data):
      for location in data:
         print("{} {} {} {},{}".format(location["name"], location["country"],
                                       location["id"], location["lat"], 
                                       location["lon"]))

class ShowWeatherLocationIdCmd(CliExtension.ShowCommandClass):

   def handler(self, ctx):
      daemon = ctx.getDaemon("WeatherDaemon")
      if daemon is None:
         ctx.addError("unable to get WeatherDaemon info")
         return(None)
      url = daemon.config.config("url")
      apikey = daemon.config.config("apikey")
      locationid = ctx.args["<id>"]

      w = Weather(url=url, apikey=apikey, locationsfile=None)
      r = w.show_weather_location(location_id = locationid, 
                                  location_name = None)

      return(r)

   def render(self, data):
      w = Weather()
      w.print_location(data)

class ShowWeatherLocationNameCmd(CliExtension.ShowCommandClass):

   def handler(self, ctx):
      daemon = ctx.getDaemon("WeatherDaemon")
      if daemon is None:
         ctx.addError("unable to get WeatherDaemon info")
         return(None)
      url = daemon.config.config("url")
      apikey = daemon.config.config("apikey")
      locationname = ctx.args["<name>"]

      w = Weather(url=url, apikey=apikey, locationsfile=None)
      r = w.show_weather_location(location_id = None, 
                                  location_name = locationname)

      return(r)

   def render(self, data):
      w = Weather()
      w.print_location(data)

class SetWeatherURL(CliExtension.CliCommandClass):
   def handler(self, ctx):
      ctx.daemon.config.configSet("url", ctx.args["<url>"])
   def noHandler(self, ctx):
      ctx.daemon.config.configSet("url", None)

class SetWeatherApiKey(CliExtension.CliCommandClass):
   def handler(self, ctx):
      ctx.daemon.config.configSet("apikey", ctx.args["<apikey>"])
   def noHandler(self, ctx):
      ctx.daemon.config.configSet("apikey", None)

class SetWeatherLocationsFile(CliExtension.CliCommandClass):
   def handler(self, ctx):
      ctx.daemon.config.configSet("locationsfile", ctx.args["<locationsfile>"])
   def noHandler(self, ctx):
      ctx.daemon.config.configSet("locationsfile", None)

def Plugin( ctx ):
   CliExtension.registerCommand("showWeatherLocations", 
                                ShowWeatherLocationsCmd, 
                                namespace="arista.Weather")
   CliExtension.registerCommand("showWeatherLocationId", 
                                ShowWeatherLocationIdCmd, 
                                namespace="arista.Weather")
   CliExtension.registerCommand("showWeatherLocationName", 
                                ShowWeatherLocationNameCmd, 
                                namespace="arista.Weather")
   CliExtension.registerCommand("configWeatherUrl", 
                                SetWeatherURL, 
                                namespace="arista.Weather")
   CliExtension.registerCommand("configWeatherApiKey", 
                                SetWeatherApiKey, 
                                namespace="arista.Weather")
   CliExtension.registerCommand("configWeatherLocationsFile", 
                                SetWeatherLocationsFile, 
                                namespace="arista.Weather")
