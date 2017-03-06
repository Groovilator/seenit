from flask import Flask, jsonify, request
import praw
import re

VALID_PERIODS = ["all", "day", "hour", "month", "week", "year"]

USER_AGENT = "seenit v0.1"

CLIENT_ID = "***REPLACE ME***"
CLIENT_SECRET = "***REPLACE ME***"
USERNAME = "***REPLACE ME***"
PASSWORD = "***REPLACE ME***"

app = Flask(__name__)

class Post(object):
	def __init__(self, title, url, thumbnail, subreddit, 
				 ups, num_comments, date_utc):
		self.title = title
		self.url = url
		self.thumbnail = thumbnail
		self.subreddit = subreddit
		self.ups = ups
		self.num_comments = num_comments
		self.date_utc = date_utc
	def serialize(self):
		return {
			'Title': self.title, 
			'url': self.url,
		    'Thumbnail': self.thumbnail,
		    'Subreddit': self.subreddit,
		    'Up Votes': self.ups,
		    'Comment Count': self.num_comments,
		    'date_utc': self.date_utc
		}

def add_popularity(posts, maxUps, minUps, maxComs, minComs):
	for i in xrange(len(posts)):
		upNorm = float(posts[i]['Up Votes'] - minUps)/float(maxUps - minUps)
		comNorm = float(posts[i]['Comment Count'] - minComs)/float(maxComs-minComs)
		posts[i]['Popularity Rating'] = upNorm + comNorm
	return posts

@app.route('/topimages')
def top_images():
	period = request.args.get('period')
	if period not in VALID_PERIODS:
		period = "day"

	reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     user_agent=USER_AGENT,
                     username=USERNAME,
                     password=PASSWORD)

	images = []
	minUps = 0
	maxUps = 0
	minComs = 0
	maxComs = -1
	regexp = re.compile(r'.*\.(jpg|jpeg|png|gif|gifv)$')
	for post in reddit.subreddit("all").top(period):
		if (regexp.search(post.url.encode('utf-8')) or "imgur.com" in post.url.encode('utf-8')):
			images.append(
				Post(
					post.title,
					post.url, 
					post.thumbnail,
					post.subreddit.display_name,
					post.ups, 
					post.num_comments,
					post.created_utc))
			if post.ups > maxUps:
				maxUps = post.ups
			if post.ups < minUps or minUps == 0:
				minUps = post.ups
			if post.num_comments > maxComs:
				maxComs = post.num_comments
			if post.num_comments < minComs or minComs == -1:
				minComs = post.num_comments

	serialized_posts = [image.serialize() for image in images]
	return jsonify(add_popularity(
		serialized_posts, maxUps, minUps, maxComs, minComs))

if __name__ == '__main__':
    app.run()