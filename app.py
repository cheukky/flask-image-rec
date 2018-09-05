from flask import Flask, render_template
import random

app = Flask(__name__)

# list of cat images
images = [
    "http://img.buzzfeed.com/buzzfeed-static/static/2013-10/enhanced/webdr05/15/9/anigif_enhanced-buzz-26388-1381844103-11.gif",
    "http://img.buzzfeed.com/buzzfeed-static/static/2013-10/enhanced/webdr01/15/9/anigif_enhanced-buzz-31540-1381844535-8.gif",
    "http://img.buzzfeed.com/buzzfeed-static/static/2013-10/enhanced/webdr05/15/9/anigif_enhanced-buzz-26390-1381844163-18.gif",
    "http://img.buzzfeed.com/buzzfeed-static/static/2013-10/enhanced/webdr06/15/10/anigif_enhanced-buzz-1376-1381846217-0.gif",
    "http://img.buzzfeed.com/buzzfeed-static/static/2013-10/enhanced/webdr03/15/9/anigif_enhanced-buzz-3391-1381844336-26.gif",
    "http://img.buzzfeed.com/buzzfeed-static/static/2013-10/enhanced/webdr06/15/10/anigif_enhanced-buzz-29111-1381845968-0.gif",
    "http://img.buzzfeed.com/buzzfeed-static/static/2013-10/enhanced/webdr03/15/9/anigif_enhanced-buzz-3409-1381844582-13.gif",
    "http://img.buzzfeed.com/buzzfeed-static/static/2013-10/enhanced/webdr02/15/9/anigif_enhanced-buzz-19667-1381844937-10.gif",
    "http://img.buzzfeed.com/buzzfeed-static/static/2013-10/enhanced/webdr05/15/9/anigif_enhanced-buzz-26358-1381845043-13.gif",
    "http://img.buzzfeed.com/buzzfeed-static/static/2013-10/enhanced/webdr06/15/9/anigif_enhanced-buzz-18774-1381844645-6.gif",
    "http://img.buzzfeed.com/buzzfeed-static/static/2013-10/enhanced/webdr06/15/9/anigif_enhanced-buzz-25158-1381844793-0.gif",
    "http://img.buzzfeed.com/buzzfeed-static/static/2013-10/enhanced/webdr03/15/10/anigif_enhanced-buzz-11980-1381846269-1.gif"
    ]


@app.route('/')
def index():
    url = random.choice(images)
    return render_template('index.html', url=url)


@app.route('/result')
def result():
    url = "https://vignette.wikia.nocookie.net/gundam/images/4/43/Gundam_Barbatos_standing_over_Sandoval_Rueters_fallen_suit.png/revision/latest/scale-to-width-down/600?cb=20161024131944"
    return render_template('result.html', url=url)


@app.route('/thanks')
def thanks():
    url = "https://vignette.wikia.nocookie.net/gundam/images/a/a7/636723.jpg/revision/latest/scale-to-width-down/600?cb=20141018031606"
    return render_template('thanks.html', url=url)


@app.route('/training')
def training():
    url = "https://vignette.wikia.nocookie.net/gundam/images/9/93/00QanTSwordBitsBeam.jpg/revision/latest/scale-to-width-down/600?cb=20120921123309"
    return render_template('training.html', url=url)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
