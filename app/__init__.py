from flask import Flask, jsonify, request, render_template
from riotwatcher import RiotWatcher, LoLException, \
error_404, error_400 \
,error_500
#error_503, error_401, error_403, error_429,\

from collections import defaultdict
import numpy as np
import pandas as pd
import os
import cPickle as pickle
#---------- MODEL IN MEMORY ----------------#


#First, get your key
res = []
with open('RitoMongo.conf') as f:
    for line in f:
        res.append(line.rstrip('\n'));
Key=res[2];

#Then, use our key to get all champion data
w = RiotWatcher(key=Key)
tags = w.static_get_champion_list(champ_data='tags')
tag_dict = defaultdict(list)
for key, value in tags['data'].iteritems():
    tag_dict[value['id']].append(value['name'])
    tag_dict[value['id']].append(value['tags'])

#These are all my calculations, they should go in a new .py file, but...
file_one = open('app/user_df.pkl','rb')
file_two = open('app/cosine_similarity.pkl','rb')
user_df = pickle.load(file_one)
cos_sim = pickle.load(file_two)
file_one.close()
file_two.close()

#  Find most "similar" user from Cosine Similarity calculation
# (Model is pre-calculated because it takes forever to run)
def computeNearestNeighbor(username, df):
    """creates a sorted list of users based on distance to username"""
    distances = []
    for i in df.columns:
        # make sure user is not self..
        if i != username:
            #pulling values from our pearson Matrix -
            sim = cos_sim[i][username]
            distances.append((sim, i))
    # sort based on distance -- closest first
    distances.sort()
    # Just return the top 4 Neighbors
    return distances[-4:]

#Calculate the User-User recommendation

def recommendation(username,df):
    # first find nearest neighbor
    nearest = computeNearestNeighbor(username, df)[3][1]
    recommendations = []
    # now find bands neighbor rated that user didn't
    neighborRatings = df[nearest]
    userRatings = df[username]
    curr_max = -1
    for champion in neighborRatings.index:
        if np.isnan(neighborRatings[champion]) == False:
            if(np.isnan(userRatings[champion]) & (neighborRatings[champion] > curr_max)):
                curr_max = neighborRatings[champion]
                recom = champion
    recommendations.append(recom)
    return recommendations

def champs_to_play(summoner_name):
    summoner_id = w.get_summoner(name=summoner_name)['id']
    return recommendation(summoner_id, user_df)

#GET INPUT FROM TEXT BOX
def get_summoner_history(summoner_name):

    basic_info = w.get_summoner(name=summoner_name)
    match_history = w.get_ranked_stats(basic_info['id'])
    player_ranked_dict = defaultdict(list)

    for item in match_history['champions']:
        played_games = float(item['stats']['totalSessionsPlayed'])
        won_games = float(item['stats']['totalSessionsWon'])
        win_perc = round(won_games / played_games,2)
        player_ranked_dict[item['id']].append(int(played_games))
        player_ranked_dict[item['id']].append(int(win_perc*100))
    del(player_ranked_dict[0])

    top_five_id = sorted(player_ranked_dict, key=player_ranked_dict.get, reverse=True)[:7]
    top_five_values = []
    for index, item in enumerate(top_five_id):
         top_five_values.append([item,player_ranked_dict[item]])

    return top_five_values
#Get static information about summoner
def get_profile_pic(summoner_name):
    basic_info = w.get_summoner(name=summoner_name)
    return basic_info['profileIconId']

#Get static ranked tier/divison information about summoner
def get_ranked_tier(summoner_name):
    basic_info = w.get_summoner(name=summoner_name)
    player_id = str(basic_info['id'])
    league_entry = w.get_league_entry(summoner_ids=[player_id])
    tier = league_entry[str(player_id)][0]['tier'].lower()
    division = league_entry[player_id][0]['entries'][0]['division']
    division = division.replace("I","1").replace("II","2").replace("I","3")\
    .replace("IV","4").replace("V","5")
    tier_division = [tier, division]
    return tier_division
#---------- URLS AND WEB PAGES -------------#

# Initialize the app
app = Flask(__name__)


@app.context_processor
def my_utility_processor():
#Get list of champions
    def get_champion_name_from_id(champion_id):
        #champ_dict = pickle.load(open('Riot-API-Code/role_id/champion_id_to_name.pkl'))
        champ_dict = tag_dict.copy()
        for k,v in champ_dict.iteritems():
            champ_dict[k][0] = champ_dict[k][0].replace("'"," ").replace(" ","").replace(".","")
        #manual edits because these naming conventions are not consistent...
        champ_dict[31][0] = u'Chogath'
        champ_dict[121][0] = u'Khazix'
        champ_dict[161][0] = u'Velkoz'
        return champ_dict[champion_id]
    return dict(get_champ_name=get_champion_name_from_id)

# Get an example and return it's score from the predictor model
@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def score():
    champ_path = request.form.get("champ_path", "")
    list_of_errors = ['error_400','error_401','error_403','error_404',\
    'error_429' ,'error_500','error_503','error_504']
    if champ_path:
        try:
            results = get_summoner_history(champ_path)
            profile_pic = get_profile_pic(champ_path)
            ranked_tier = get_ranked_tier(champ_path)
            recommended_champs = champs_to_play(champ_path)
            return render_template("results.html", champ_path=champ_path, results=results
                                ,profile_pic=profile_pic, ranked_tier=ranked_tier
                                ,recommended_champs=recommended_champs)
        except LoLException as e:
            if e in list_of_errors:
                error_message = e
            else:
                error_message = "IDK what the deal is"
            return render_template("index.html", error_message=error_message)
    else:
        return render_template("index.html", error_message=None)

@app.route("/results", methods=["GET", "POST"])
def results():
    champ_path = request.form.get("champ_path", "")
    list_of_errors = ['error_400','error_401','error_403','error_404',\
    'error_429' ,'error_500','error_503','error_504']
    if champ_path:
        try:
            results = get_summoner_history(champ_path)
            profile_pic = get_profile_pic(champ_path)
            ranked_tier = get_ranked_tier(champ_path)
            recommended_champs = champs_to_play(champ_path)
            return render_template("results.html", champ_path=champ_path, results=results
                                ,profile_pic=profile_pic, ranked_tier=ranked_tier
                                ,recommended_champs=recommended_champs)
        except LoLException as e:
            if e in list_of_errors:
                error_message = e
            else:
                error_message = "IDK what the deal is"
            return render_template("index.html", error_message=error_message)
    else:
        return render_template("index.html", error_message=None)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
#--------- RUN WEB APP SERVER ------------#

# Start the app server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
