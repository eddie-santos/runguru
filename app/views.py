import datetime
import pandas as pd
import pymysql as mdb
import random
import re
from app import app
from flask import render_template, request
from model import *

# db is the database containing all relevant data
db = mdb.connect(user="root", host="localhost", db="runnersdb", charset='utf8')

# method: index()
# function: renders home page
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

# method: output()
# function: calculates answer and renders results
@app.route('/output')
def output():
    # reads in pace and activities from options
    mpace_hr = float(request.args.get('mpace'))
    day1 = request.args.get('day1')
    day2 = request.args.get('day2')
    day3 = request.args.get('day3')
    user_pattern = get_pattern([day3,day2,day1])
  
    # loads data from database
    with db:
        cur = db.cursor()

        # list of runners
        good_runners = pd.read_sql("SELECT * FROM good_runners;",db)

        # daily metrics for runners
        days = good_runners['days_to_marathon']
        diffs = good_runners['run_difficulty'].astype(int)
        stresses = good_runners['run_stress']

        # pdfs for different run classes
        easy_pdf = pd.read_sql("SELECT * FROM easy_pdf",db)['0'].tolist()
        mod_pdf = pd.read_sql("SELECT * FROM mod_pdf",db)['0'].tolist()
        hard_pdf = pd.read_sql("SELECT * FROM hard_pdf",db)['0'].tolist()
        epic_pdf = pd.read_sql("SELECT * FROM epic_pdf",db)['0'].tolist()

        # intensities for different run classes
        intensity_ez = pd.read_sql("SELECT * FROM easy_ints",db)['0'].tolist()
        intensity_m = pd.read_sql("SELECT * FROM mod_ints",db)['0'].tolist()
        intensity_h = pd.read_sql("SELECT * FROM hard_ints",db)['0'].tolist()
        intensity_ep = pd.read_sql("SELECT * FROM epic_ints",db)['0'].tolist()

        # markov transition probabilities
        prob_table = pd.read_sql("SELECT * FROM act_prob",db)

    # combines pdfs and intensities to a dictionary
    pdfs = {0:[0],1:easy_pdf,2:mod_pdf,3:hard_pdf,4:epic_pdf}
    intensities = {0:[0],1:intensity_ez,2:intensity_m,3:intensity_h,4:intensity_ep}

    # determines difficulty, day_class, stress, and intensity from user input
    difficulty = get_difficulty(prob_table,user_pattern)
    day_class = get_class(difficulty)
    stress = get_stress(pdfs,difficulty)
    intensity = get_intensity(difficulty,intensities)
  
    # information to be displayed for the athlete
    todays_run = get_today(mpace_hr,intensity,stress,difficulty)
    display = get_display(difficulty,todays_run)
    dist = display[0]
    pace = display[1]

    return render_template("output.html", diff = difficulty, stress = stress, dist = dist, pace = pace, day = day_class)

# method: slides()
# function: renders slides page
@app.route('/slides')
def slides():
    return render_template("slides.html")
