from flask import Flask, render_template, url_for
import random 

app = Flask(__name__)

@app.route('/')
def hello_world():
    quote = random.choice(["live free or die", "jeff is cool", "hire jeff to work for you"])
    return render_template("index.html", quote=quote)


if __name__ == "__main__":
    # app.debug()
    app.run(host="0.0.0.0", port=5005, debug=True)