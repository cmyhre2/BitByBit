from flask import Flask, render_template, request, jsonify
import requests, os
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__, template_folder="templates")
CORS(app)

OPENWEATHER_KEY = os.getenv("OPENWEATHER_API_KEY")
OW_BASE = "https://api.openweathermap.org/data/2.5"

def call_openweather(path, params):
    params = params.copy()
    params["appid"] = OPENWEATHER_KEY
    params.setdefault("units","metric")
    r = requests.get(f"{OW_BASE}/{path}", params=params, timeout=10)
    r.raise_for_status()
    return r.json()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/weather")
def api_weather():
    if not OPENWEATHER_KEY:
        return jsonify({"error":"OPENWEATHER_API_KEY not configured"}),500

    q=request.args.get("q")
    lat=request.args.get("lat")
    lon=request.args.get("lon")
    mode=request.args.get("mode","").lower()

    try:
        if mode=="onecall" and lat and lon:
            data=call_openweather("onecall",{"lat":lat,"lon":lon,"exclude":"minutely,alerts"})
            return jsonify({"source":"onecall","data":data})

        if lat and lon:
            data=call_openweather("weather",{"lat":lat,"lon":lon})
            return jsonify({"source":"weather_coord","data":data})

        if q:
            data=call_openweather("weather",{"q":q})
            return jsonify({"source":"weather_q","data":data})

        return jsonify({"error":"Provide q or lat/lon"}),400

    except Exception as e:
        return jsonify({"error":"OpenWeather error","detail":str(e)}),500

@app.route("/api/ping")
def ping():
    return jsonify({"status":"ok","time":datetime.utcnow().isoformat()+"Z"})

if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000)
