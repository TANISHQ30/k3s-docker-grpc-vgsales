from cProfile import label
from flask import Flask, request, render_template
import redis
import pandas as pd
import json
import plotly
import plotly.express as px

app = Flask(__name__, template_folder='templates')

result_data = {
        "Total game sold in all regions":"",
        "Average game sold in all regions":"",
        "Top selling game genre":"",
        "Top selling game":""
    }

@app.route('/test')
def cumulative_result():
    return result_data

@app.route('/')
def print_logs():
    output = ""
    index = 0
    labels = []
    values = []
    rolling_metric_res = {}

    game_review_result = {
        "Game title":"",
        "User rating":""
    }

    ar = ["Highest_selling_game", "Average_sell_of_games",
                    "Highest_selling_genre", "Lowest_selling_genre"]
    try:
        conn = redis.StrictRedis(host='redis', port=6379)
        for key in conn.scan_iter("log.greeter_server*"):
            
            k = str(key)
            
            val = str(conn.get(key))
            val = val.strip("b")
            val = val.strip("'")

            # Receive data from sales server (1st dataset)
            if k=="b'log.greeter_server.msg1'":
                result_data["Total game sold in all regions"] = val + " million"
            elif k=="b'log.greeter_server.msg2'":
                result_data["Average game sold in all regions"] = val + " million"
            elif k=="b'log.greeter_server.msg3'":
                result_data["Top selling game genre"] = val
            elif k=="b'log.greeter_server.msg4'":
                result_data["Top selling game"] = val
            # Receive data from review server (2nd dataset)
            elif k=="b'log.greeter_server.game_title'":
                game_review_result["Game title"] = val
            elif k=="b'log.greeter_server.user_rating'":
                game_review_result["User rating"] = val
        
        seconds_passed = int(conn.get("secondsPassed"))

        rolling_metric_res = json.loads(conn.get("metrics"))
        if len(rolling_metric_res.keys()) != 0 and seconds_passed >= 180:
            labels = list(rolling_metric_res.keys())
            values = list(rolling_metric_res.values())
            index = 1
        if index == 0:
            labels = []
            values = []

    except Exception as ex:
        output = 'Error: ' + str(ex)

    df = pd.DataFrame({
      'Game genre': labels,
      'Average sales (in millions)': values,
    })

    fig = px.bar(df, x='Game genre', y='Average sales (in millions)')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template('index.html', data=result_data, data_new=game_review_result, graphJSON=graphJSON, label=list(labels))

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

