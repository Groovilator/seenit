from flask import Flask, jsonify
import praw
import re

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

@app.route('/topimages')
def top_images():
	reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     user_agent=USER_AGENT,
                     username=USERNAME,
                     password=PASSWORD)

	images = []
	regexp = re.compile(r'.*\.(jpg|jpeg|png|gif|gifv)$')
	for post in reddit.subreddit("all").top("all"):
		if (regexp.search(str(post.url)) or "imgur.com" in str(post.url)):
			images.append(
				Post(
					post.title,
					post.url, 
					post.thumbnail,
					post.subreddit.display_name,
					post.ups, 
					post.num_comments,
					post.created_utc))

	return jsonify([image.serialize() for image in images])

if __name__ == '__main__':
    app.run()