import os
from flask import Flask, jsonify, request
from flask_cors import CORS
# Kaggle credentials: set KAGGLE_USERNAME and KAGGLE_KEY in the environment (or use ~/.kaggle/kaggle.json). Never commit them.

app = Flask(__name__)
CORS(app)

# Instantiate the API class
from kaggle.api.kaggle_api_extended import Competition, KaggleApi
api = KaggleApi()

# Authenticate using your Kaggle credentials
api.authenticate()

@app.route('/leaderboard/<competition>', methods=['GET'])
def get_leaderboard(competition):
    # Get the leaderboard of a competition
    leaderboard = api.competition_view_leaderboard(competition)

    # Prepare the leaderboard for JSON
    leaderboard_json = []
    print('leaderboard: ', leaderboard)
    for rank, team in enumerate(leaderboard['submissions'], start=1):
        leaderboard_json.append({
            'rank': rank,
            'team': team['teamName'],
            'score': team['score']
        })

    return jsonify(leaderboard_json)

@app.route('/leaderboard-full', methods=['POST'])
def get_full_leaderboard():
    def get_leaderboard_info(competition):
        # Get the leaderboard of a competition
        leaderboard = api.competition_view_leaderboard(competition)

        # Prepare the leaderboard for JSON
        leaderboard_json = []
        print('leaderboard: ', leaderboard)
        for rank, team in enumerate(leaderboard['submissions'], start=1):
            leaderboard_json.append({
                'rank': rank,
                'team': team['teamName'],
                'score': team['score']
            })

        return leaderboard_json

    
    # competitions = [
    #     "1b22f135b4d3a31152fa",
    #     "DATAHACK-Collective-Opinion-Spam-Detection",
    #     "datahack-community-detection",
    #     "DATAHACK-Yalidine-Challenge",
    #     "DATAHACK-store-recommendation-system",
    #     "8b971ca63765",
    # ]

    competitions = request.get_json()['competitions']

    # generate leaderboard for each competition
    leaderboard_json = []
    for competition in competitions:
        leaderboard_json.append(get_leaderboard_info(competition))

    # create a list of dictionaries "team_name, score" where score is an list of floats, the score of each challenge 
    teams_scores = []

    # initlaize the list of teams with the names, and empty scores
    for team in leaderboard_json[0]:
        teams_scores.append({'team': team['team'], 'scores': ["0.000"] * len(competitions)})

    # fill the scores of each team, based on the team name in a challenge
    for i, challenge in enumerate(leaderboard_json):
        for team in challenge:
            for t in teams_scores:
                if t['team'] == team['team']:
                    t['scores'][i] = team['score']

    # return jsonify(teams_scores)
    return jsonify({"infos": teams_scores})

if __name__ == '__main__':
    app.run(debug=True)

