from flask import render_template, request
import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from app import app

#index page
@app.route('/')
def index():
    name = request.args.get("name")
    if name == None:
        name = "Sean"
    return render_template("base.html", name=name)


feature_names = ['ETF1','ETF2']

# # Load the Iris Data Set
# iris_df = pd.read_csv("data/iris.data",
#     names=["Sepal Length", "Sepal Width", "Petal Length", "Petal Width", "Species"])
# feature_names = iris_df.columns[0:-1].values.tolist()
#
# # Create the main plot
def create_figure(current_feature_name, bins):
    p = figure(title=current_feature_name, plot_width=300, plot_height=300)
    if current_feature_name == 'ETF1':
        p.multi_line(xs=[[1,2,3],[2,3,4],[1,2,3]], ys = [[6,7,2],[4,5,7],[10,1,2]], color=['red','green','blue'])
    if current_feature_name == 'ETF2':
        p.line(x=[1,2,3,4,5], y=[6,7,2,4,5])

    # Set the x axis label
    p.xaxis.axis_label = current_feature_name
    # Set the y axis label
    p.yaxis.axis_label = 'Count'
    return p


@app.route('/plotswag')
def plot_swag():
    # Determine the selected feature
    current_feature_name = request.args.get("feature_name")
    if current_feature_name == None:
        current_feature_name = "Sepal Length"

    # Create the plot
    plot = create_figure(current_feature_name, 10)

    # Embed plot into HTML via Flask Render
    script, div = components(plot)
    return render_template("plotswag.html", script=script, div=div,
                           feature_names=feature_names, current_feature_name=current_feature_name)