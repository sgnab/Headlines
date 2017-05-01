from flask import Flask,redirect,render_template,request,session,make_response
import feedparser
import urllib2,urllib,requests,datetime
import json



app=Flask(__name__)

# sample of RSS Feeds
SS_FEEDS = {"voa":'http://ir.voanews.com/api/zuiypepjy_',
    'bbcp':'http://feeds.bbci.co.uk/persian/rss.xml',
    'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640'
            }

# Default query values
default={"city":"London","publication":"bbc",
         'curr_from':"USD",
            'curr_to': "GBP"}

# main page
@app.route("/",methods=["GET","POST"])
def main_mathod():
    # a get request by user to be extracted from Html form
    publication=query_handler('publication')
    all_article = get_news(publication)


    #extracting weather data
    city=query_handler('city')
    weather = get_weather(city)

    # Currency from and currency_to handling
    curr_from=query_handler('curr_from')
    curr_to=query_handler('curr_to')
    #getting exchange rate
    rate,currencies=currency_conversion(curr_from,curr_to)
    # setting cookies
    response=make_response(render_template('newsfeed.html', all_article=all_article,weather=weather,
                                           curr_from=curr_from,curr_to=curr_to,rate=rate,currencies=sorted(currencies))
                                                      )
    expires=datetime.datetime.now()+datetime.timedelta(days=365)
    response.set_cookie('publication',publication,expires=expires)
    response.set_cookie('city',city,expires=expires)
    response.set_cookie('curr_from',curr_from,expires=expires)
    response.set_cookie('curr_to',curr_to,expires=expires)
    return response



# a method to get the weather infos from Openweathermap using API keys
def get_weather(query):
    api_url= 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=0ce3d306b8843597c9305743ccb8e4d9'
    query = urllib.quote(query)
    url = api_url.format(query)
    data = urllib2.urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather = {"description": parsed["weather"][0]["description"], "temperature": parsed["main"]["temp"],
                   "city": parsed["name"],
                   'country': parsed['sys']['country']}
    return weather
# a method to extract an parse the data from RSS feeds
def get_news(publication):
    feed = feedparser.parse(SS_FEEDS[publication])
    all_article = feed['entries']
    return all_article

def currency_conversion(curr_from,curr_to):
    curr_url = "https://openexchangerates.org//api/latest.json?app_id=7d92caed59234f05b12717523885adc3"
    all_currs=urllib2.urlopen(curr_url).read()
    data=json.loads(all_currs).get("rates")
    f_rate=data.get(curr_from.upper())
    to_rate=data.get(curr_to.upper())
    return (to_rate/f_rate,data.keys())

def query_handler(form_input):
    if  request.args.get(form_input):
        return request.args.get(form_input)
    if request.cookies.get(form_input):
        return request.cookies.get(form_input)
    return default[form_input]


if __name__=="__main__":
    app.run(debug=True)


