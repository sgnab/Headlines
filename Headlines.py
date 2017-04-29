from flask import Flask,redirect,render_template,request,session
import feedparser



app=Flask(__name__)
SS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640'}
@app.route("/<publication>",methods=["GET"])
def get_news(publication):
    feed = feedparser.parse(SS_FEEDS[publication])
    all_article = feed['entries']
    return render_template('newsfeed.html',all_article=all_article)



if __name__=="__main__":
    app.run(debug=True)