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
             'iol': 'http://www.iol.co.za/cmlink/1.640'}

# Default query values
default={"city":"London","publication":"bbc"}

# main page
@app.route("/",methods=["GET","POST"])
def main_mathod():
    # a get request by user to be extracted from Html form
    query = request.args.get('publication')
    if not query or query.lower() not in SS_FEEDS:
        publication = default['publication']

    else:
        publication = query.lower()
    # a get request by user to be extracted from Html form
    query2=request.args.get('city')
    if not query2:
        city=default['city']
    else:
        city=query2.lower()
    # Parsing the data extracted from RSS feeds into dictionaries
    all_article=get_news(publication)
    weather = get_weather(city)

    return render_template('newsfeed.html', all_article=all_article,weather=weather)


# a method to get the weather infos from Openweathermap using API keys
def get_weather(query):
    api_url= 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=0ce3d306b8843597c9305743ccb8e4d9'
    query = urllib.quote(query)
    url = api_url.format(query)
    data = urllib2.urlopen(url).read()

    # data=data.content
    parsed = json.loads(data)

    weather = None
    if parsed.get("weather"):
        weather = {"description": parsed["weather"][0]["description"], "temperature": parsed["main"]["temp"],
                   "city": parsed["name"]
                   }
    return weather

def get_news(publication):
    feed = feedparser.parse(SS_FEEDS[publication])
    all_article = feed['entries']
    return all_article

if __name__=="__main__":
    app.run(debug=True)


######On ecan use the following method to use Post request instead of Get request for RSS exctarction

 # if request.method=="POST":
 #        query=request.form['publication']
 #        if query.lower() not in SS_FEEDS:
 #            publication='cnn'
 #        else:
 #            publication=query.lower()
 #        feed = feedparser.parse(SS_FEEDS[publication])
 #        all_article = feed['entries']
 #        return render_template('newsfeed.html', all_article=all_article)
 #    publication='cnn'
 #    feed = feedparser.parse(SS_FEEDS[publication])
 #    all_article = feed['entries']
 #    return render_template('newsfeed.html', all_article=all_article)
 #
 #