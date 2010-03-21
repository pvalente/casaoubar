#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from foursquare import foursquare
import yql

class MainHandler(webapp.RequestHandler):

  def get(self):
    
    y = yql.Public()
    query_km = "select * from html where xpath=\"//*[@id='lentidao']/strong\" and url='http://cetsp1.cetsp.com.br/monitransmapa/agora/'"

    km = y.execute(query_km)
    
    query_trend = 'select title from html where xpath=\'//*[@id="tendencia"]/img\' and url="http://cetsp1.cetsp.com.br/monitransmapa/agora/"'
    
    trend = y.execute(query_trend)
    
    km = int(km.rows)
    trend = trend.rows['title']

    km = 160
    
    template_values = {
             'km': km,         
             'trend': trend,
             'decision' : decide(km, trend),         
            }
        
    path = os.path.join(os.path.dirname(__file__), 'templates/casaoubar.html')
    self.response.out.write(template.render(path, template_values))

def decide(km, trend):
    
    if trend == "BAIXA":
        if km < 100:
            return "casa"
        return "bar"
    elif trend == "ESTAVEL":
        if km < 90:
            return "casa"
        return "bar"
    elif trend == "ALTA":
        if km < 70:
            return "casa"
        return "bar"
    

class GeoHandler(webapp.RequestHandler):

  def get(self):

   f = foursquare.Api()
   venues = f.get_venues(self.request.get("lat"), self.request.get("lon"), q='bar') 


   template_values = { 
   'venues': venues,
   }

   path = os.path.join(os.path.dirname(__file__), 'templates/casaoubargeo.html')
   self.response.out.write(template.render(path, template_values))

def main():
  application = webapp.WSGIApplication([('/', MainHandler), ('/geo', GeoHandler)],
                                       debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
