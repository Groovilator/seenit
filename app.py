from flask import Flask

app = Flask(__name__)

@app.route('/topimages')
def top_images():
	return "Top Images"

if __name__ == '__main__':
    app.run()