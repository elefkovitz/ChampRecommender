# __ChampRecommender__

![Teemo](https://sk2.op.gg/images/lol/champion/Teemo.png)

### What is ChampRecommender?
ChampRecommender is a tool to help League of Legends players more effectively choose which champions they should be dedicating their efforts towards.

This tool uses data from Riot's API, as well as plenty of help from the repos thanked below.

### How do I use it?

If you're curious about just playing around and getting personalized recommendations, you can do that here:

http://54.67.67.56:8000/

If you don't play League of Legends and want to test it, you can use this random player I chose (sadly I haven't played ranked this season):
 __ly lose__

__EDIT (07/10/17):__ Riot has updated their API endpoints, so all of my API calls are currently broken! Very sorry for the inconvenience, I will get this up and running again ASAP :)

### How is the app built?

This is a Flask app hosted on an EC2 instance. I used Python and HTML/CSS (poorly) to design this small application. I am a Data Scientist, not a Web Developer, so please excuse the lack of anything fancier than a simple HTML/CSS framework :)

If you're familiar with these frameworks, I think my code is pretty self-explanatory with the comments I included in the init.py file.

If something is unclear or you want to know how/why I implemented something the way I did, shoot me a message!

### How does the recommendation work?

The actual recommendation is generated from an SVD model based on a matrix of many users crossed with all the champions. It takes a really long time to run this, but that's ok since you only need to run it once (then pickle it/store it in a DB) to use it.

### Where is the actual recommendation calculated?

That code is available in the iPython Notebook file, but is unused in the app. The SVD matrix is pre-calculated (because it takes 12 hours to run), pickled, and called into memory when the Flask app is initialized.

#### Happy recommending!!

## Special thanks to:

__Riot Games:__ [Riot API](https://developer.riotgames.com/)

__pseudonum117:__ [RiotWatcher](https://github.com/pseudonym117/Riot-Watcher)

__HeshamAmer:__ [RitoMongo](https://github.com/HeshamAmer/Riot-API-datasource)

__jjmaldonis:__ [Riot-API-Code](https://github.com/jjmaldonis/Riot-API-Code)

And, of course...

The entire [Metis](http://www.thisismetis.com/) team for teaching me everything I know :)

##### Required Legal Disclaimer:

_ChampRecommender isn’t endorsed by Riot Games and doesn’t reflect the views or opinions of Riot Games or anyone officially involved in producing or managing League of Legends. League of Legends and Riot Games are trademarks or registered trademarks of Riot Games, Inc. League of Legends © Riot Games, Inc._
