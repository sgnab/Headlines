from flask import Flask,redirect,render_template,request,session
import feedparser



app=Flask(__name__)
BBC_FEED="http://feeds.bbci.co.uk/news/rss.xml"
@app.route("/",methods=["GET"])
def get_news():
    feed = feedparser.parse(BBC_FEED)
    first_article = feed['entries'][0]
    return """<html>
        <body>
            <h1> BBC Headlines </h1>
            <b>{0}</b> <br/>
            <i>{1}</i> <br/>
            <p>{2}</p> <br/>
        </body>
    </html>""".format(first_article.get("title"), first_article.get("published"), first_article.get("summary"))




if __name__=="__main__":
    app.run(debug=True)