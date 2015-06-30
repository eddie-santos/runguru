from bisect import bisect
import datetime
import random

#method: get_difficulty(prob_list,last_acts)
#function: determines daily run difficulty
#arguments:
# - prob_list: markov chain probability dictionary (matrix)
# - last_acts: users last three activities
#returns: daily run difficulty
def get_difficulty(prob_list,last_acts):
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

#method: get_stress(pdfs,diff)
#function: select today's exact numerical run stress
#arguments:
# - pdfs: probability distribution function for run stresses
#         based on run difficulty
# - diff: today's run difficulty determined in get_difficulty()
# returns: numerical run stress
def get_stress(pdfs,diff):
    stress = random.choice(pdfs[diff])
    # determines stress from class pdf
    while stress > 0.87:
        stress = random.choice(pdfs[diff])
    return stress

#method: get_class(diff)
#function: gets text belonging to run class
#arguments:
# - diff: run class
#returns: string version of run class
def get_class(diff):
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

#method: get_today(mpace_hr,intesnity,stress,diff)
#function: determines distance and pace for the day
#arguments:
# - mpace_hr: marathon pace in hours
# - intensity: run intensity determined from pace
# - stress: run stress for today
# - diff: run difficulty for today
#returns: [dist,space] in string format    
def get_today(mpace_hr,intensity,stress,diff):
    mdist = 26.2

    # calculates pace in seconds/mile
    mpace = mpace_hr*60*60/mdist 
    pace = 0

    # determines pace and distance if not a rest day
    if diff != 0:
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

#method: get_display(diff,today)
#function: converts results to display format
#arguments: 
# - diff: today's run difficulty
# - today: [dist,pace] for today
#returns: results to be displayed   
def get_display(diff,today):
    if diff == 0:
        dist = '0 miles'
        pace = 'rest!'
    else:
        dist = str(round(today[0],1)) + ' miles'
        pace = today[1] + ' / mile'
    return [dist,pace]

#method: get_intensity(diff,intensities)
#function: calculates run intensity based on run class
#arguments:
# - diff: today's run class
# - intensities: dictionary containing intensity distributions
#                for each run class
#returns: today's intensity
def get_intensity(diff,intensities):
    intensity = 0
    # limits intensity to reasonable range and random selects
    while (intensity < 0.8) or (intensity > 1.2):
        intensity = random.choice(intensities[int(diff)]) 
    return intensity
