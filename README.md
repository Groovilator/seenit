# seenit

Simple http server that accepts connections over port 8080 and provides a 
sha512 hash if a "password" parameter is provided. Additionally, a graceful
shutdown endpoint is exposed that stops the http server, refuses any 
subsequent requests, and exits.

Simple Flask app that provides endpoints to identify image posts on the Reddit 
frontpage (r/all).

Additionally, a landing page is provided at the root ("localhost:5000/")
that displays trending subreddit information and a simple interface to query 
the API for top/popular image posts (limit 50).


## Endpoints:
**"/topimages"** - Endpoint for requesting the top image posts from the Reddit
frontpage ("r/all"). In addition, the endpoint calculates a normalized 
"Popularity Rating" for each returned image post that consists of the sum of 
the normalized "Up Votes" count and the normalized "Comment" count (rating 
range = [0,2]).

The endpoint accepts a paramter "period" that allows the user to specify the 
time period from which to get the top image posts. If no period is provided or
an invalid period is provide the service defaults the period to "day". 
Valid time periods: "all", "day", "hour", "month", "week", "year"

   Ex. http://localhost:8080/topimages
   	   http://localhost:8080/topimages?period=week

   Response JSON Structure:
   
   `[
	  {
	    "Comment Count": 1223, 
	    "Popularity Rating": 1.7198351971748087, 
	    "Subreddit": "gifs", 
	    "Thumbnail": "https://b.thumbs.redditmedia.com/Rd70omzbQNTTyCfadgSUJWNaAPY2kYAIwA1AY9DbpGU.jpg", 
	    "Title": "Baby Bottle Robot", 
	    "Up Votes": 82308, 
	    "date_utc": 1488813018.0, 
	    "url": "http://i.imgur.com/etyfb3z.gifv"
	  },
	  ...
	]`
      
**"/hotimages"** - Endpoint for requesting image posts that are present on the
hot and rising sections of the "all" subreddit. 
   
   Ex. http://localhost:8080/hotimages

   Response JSON Structure:

   `[
	  {
	    "Comment Count": 242, 
	    "Subreddit": "trebuchetmemes", 
	    "Thumbnail": "https://b.thumbs.redditmedia.com/AQCY_qLWmUm12EWUCsE9jPlEPmsUFQvKK0KCnQQbzMI.jpg", 
	    "Title": "The new algorithm was designed to keep the trebuchet off of the front page, but sadly that won't happen.", 
	    "Up Votes": 27456, 
	    "date_utc": 1488808634.0, 
	    "url": "https://i.redd.it/u67dhfpxmsjy.jpg"
	  }, 
	  ...
	]`

              
## Build/Run
To install python dependencies run
`pip install -r requirements.txt`
in the source directory.

To start the server run
`python app.py`
in the source directory.
