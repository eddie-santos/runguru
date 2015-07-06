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

@app.route('/')
@app.route('/index')
def index():
    """
    function: renders homepage
    """

    return render_template("index.html")

@app.route('/output')
def output():
    """
    function: calculates answer and renders results
    """

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

        # markov transition probabilities
        prob_table = pd.read_sql("SELECT * FROM act_prob",db)

    # daily metrics for runners
    days = good_runners['days_to_marathon']
    diffs = good_runners['run_difficulty'].astype(int)
    stresses = good_runners['run_stress']
    difficulty = get_difficulty(prob_table,user_pattern)
    day_class = get_class(difficulty)

    with db:
        # get pdf and ints tables for stress and intensity
        # based on difficulty
        if difficulty == 0:
            pdf = [0]
            ints = [0]
        elif difficulty == 1:
            pdf = pd.read_sql("SELECT * FROM easy_pdf",db)['0'].tolist()
            ints = pd.read_sql("SELECT * FROM easy_ints",db)['0'].tolist()
        elif difficulty == 2:
            pdf = pd.read_sql("SELECT * FROM mod_pdf",db)['0'].tolist()
            ints = pd.read_sql("SELECT * FROM mod_ints",db)['0'].tolist()
        elif difficulty == 3:
            pdf = pd.read_sql("SELECT * FROM hard_pdf",db)['0'].tolist()
            ints = pd.read_sql("SELECT * FROM hard_ints",db)['0'].tolist()
        else:
            pdf = pd.read_sql("SELECT * FROM epic_pdf",db)['0'].tolist()
            ints = pd.read_sql("SELECT * FROM epic_ints",db)['0'].tolist() 

    # calculate stress and intensity
    stress = get_stress(pdf)
    intensity = get_intensity(ints)
  
    # information to be displayed for the athlete
    todays_run = get_today(mpace_hr,intensity,stress)
    display = get_display(difficulty,todays_run)
    dist = display[0]
    pace = display[1]

    return render_template("output.html", diff = difficulty,
                     stress = stress, dist = dist, pace = pace, day = day_class)

@app.route('/slides')
def slides():
    """
    function: renders slides page
    """

    return render_template("slides.html")
