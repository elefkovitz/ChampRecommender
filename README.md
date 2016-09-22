# ChampRecommender
ChampRecommender is a tool to help League of Legends players more effectively choose which champions they should be dedicating their efforts towards.

This tool uses data from Riot's API (as well as plenty of help from the repos thanked below): www.developer.riotgames.com

The actual recommendation is generated from an SVD model based on a matrix of many users crossed with all the champions. It takes a really long time to run this, but that's ok since you only need to run it once (then pickle it/store it in a DB) to use it.

It's hard to conclude that these recommendations are "good", although there is certainly a logical pattern based on what I've seen as recommendations.

Happy recommending!!

Special thanks to :

pseudonum117: RiotWatcher
HeshamAmer: RitoMongo,
jjmaldonis: Riot-API-Code

And, of course...

The entire Metis team for teaching me everything I know :)
