from flask import Flask,redirect,render_template,request,session
import feedparser
import urllib2,urllib,requests
import json



app=Flask(__name__)
SS_FEEDS = {"voa":'http://ir.voanews.com/api/zuiypepjy_',
    'bbcp':'http://feeds.bbci.co.uk/persian/rss.xml',
    'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640'}
@app.route("/",methods=["GET","POST"])
def get_news():
    query = request.args.get('publication')
    if not query or query.lower() not in SS_FEEDS:
        publication = 'bbc'

    else:
        publication = query.lower()

    feed = feedparser.parse(SS_FEEDS[publication])
    weather = get_weather("London,UK")
    all_article = feed['entries']
    return render_template('newsfeed.html', all_article=all_article,weather=weather)



def get_weather(query):
    api_url= 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=0ce3d306b8843597c9305743ccb8e4d9'
    query = urllib.quote(query)
    url = api_url.format(query)
    data = urllib2.urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather = {"description": parsed["weather"][0]["description"], "temperature": parsed["main"]["temp"],
                   "city": parsed["name"]
                   }
    return weather


if __name__=="__main__":
    app.run(debug=True)




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