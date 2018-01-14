from flask import Flask, render_template, request

app = Flask("portfolio-grapher")

#index page
@app.route('/')
def index():
    name = request.args.get("name")
    if name == None:
        name = "Sean"
    return render_template("index.html", "portfolio-grapher")

#with debug=True, Flask server will auto-reload
#when there are code changes

#if "portfolio-grapher" == 'main':
#app.run(port=5000, debug=True)

