#Steps when a user hits "submit"
#Step 1: They enter a name, ping API to find summonerID
#Step 2: Use summonerID to find match history (totalSessionsPlayed) delineated
#        by championID
#Step 3: a) If that summoner's match history already exists in the matrix of users,
#        update it and use it as prediction goal.
#        b) If that summoner's match history isn't in current matrix, append it.
#        Then, use it as prediction goal
#Where does the matrix live? How is it called?
#Step 4: Run it through user-user collab filtering model and predict top 3
#        recommendations for user, print out those champions' picture assets
#Step 5:
