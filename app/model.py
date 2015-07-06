import datetime
import random
from bisect import bisect

def get_pattern(days):
    """
    function: creates difficulty pattern string
    arguments:
        1) days: list of last three days activities
    returns: last three days activities (string) 
    """

    p = ''
    for day in days:
        if day == 'rest':
            p = p + '0'
        elif day == 'easy':
            p = p + '1'
        elif day == 'moderate':
            p = p + '2'
        elif day == 'hard':
            p = p + '3'
        elif day == 'epic':
            p = p + '4'
    return p

def get_difficulty(prob_list,last_acts):
    """
    function: determines daily run difficulty
    arguments:
        1) markov chain probability dictionary
        2) last_acts: users last three activities  
    returns: daily run difficulty (int)
    """

    diff = 0
    # builds cdf from probabilities
    probs = prob_list[last_acts]
    cdf = [probs[0]]
    for i in xrange(1,len(probs)):
        cdf.append(cdf[-1] + probs[i])
    # forces user to run after three rest days
    if last_acts == '000':
        while (diff == 0):
            diff = bisect(cdf,random.random())
    else:
        diff = bisect(cdf,random.random())

    return diff 

def get_stress(pdf):
    """
    function: select today's exact numerical run stress
    arguments:
        1) pdf: probability distribution function for run
                stress based on run difficulty
        2) diff: today's run difficulty determined in 
                 get_difficulty()
    return: run stress (float)
    """

    stress = random.choice(pdf)
    # determines stress from class pdf
    while stress > 0.87:
        stress = random.choice(pdf)
    return stress

def get_class(diff):
    """
    function: gets text belonging to run class
    arguments:
        1) diff: numeric label for run difficulty 
    return: run class description (string)
    """

    if diff == 0:
        return 'rest'
    elif diff == 1:
        return 'easy'
    elif diff == 2:
        return 'moderate'
    elif diff == 3:
        return 'hard'
    elif diff == 4:
        return 'epic'
    else:
        return 'whoops!'

def get_today(mpace_hr,intensity,stress):
    """
    function: determine distance and pace for the day
    arguments:
        1) mpace_hr: marathon pace in hours
        2) intensity: run intensity determined from pace
        3) stress: numerical run stress for today
    returns: [dist, pace] (string) 
    """

    #marathon distance
    mdist = 26.2

    # calculates pace in seconds/mile
    mpace = mpace_hr*60*60/mdist 
    pace = 0

    # determines pace and distance if not a rest day
    if stress >= 0:
        pace = mpace / intensity
    dist = stress * mdist / (intensity ** 2) 

    # if a weekday, set pace to marathon pace and distance accordingly
    today = datetime.datetime.today().weekday()
    if (today == 5) or (today == 6): 
        pace = mpace
        dist = stress * mdist

    # gets minuntes and seconds of pace
    pace = float(pace) / 60
    secs = float((pace % 1) * 60) 
    mins = float(pace - (pace % 1)) 

    # gets dist and pace in appropriate format to display
    mod = ''
    if secs / 10 < 1:
        mod = '0' 
    space = str(int(mins)) + ':' + mod + str(int(secs))
    dist = round(dist,1)

    return [dist,space]

def get_display(diff,today):
    """
    function: converts results to display format
    arguments:
        1) diff: today's run difficulty class
        2) today: list of today's distance and pace
    returns: results to be displayed (string)
    """

    if diff == 0:
        dist = '0 miles'
        pace = 'rest!'
    else:
        dist = str(round(today[0],1)) + ' miles'
        pace = today[1] + ' / mile'
    return [dist,pace]

def get_intensity(ints):
    """
    function: calculates run intensity based on run class
    arguments:
        1) diff: today's run class
        2) ints: intensity distribution for run class
    returns: today's run intensity (float)
    """

    intensity = 0
    # limits intensity to reasonable range and random selects
    while (intensity < 0.8) or (intensity > 1.2):
        intensity = random.choice(ints) 
    return intensity
