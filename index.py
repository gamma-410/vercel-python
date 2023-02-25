# 2022 / 12 / 12 writing sourceCode.
# copyright (c) 2022 @gamma410 All rights reserved.
# Teal Social networking service.
# This sourceCode is Teal's serverSystem.


from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from json_serializable import JSONSerializable  # SpecialThanks...!

import datetime
import pytz


app = Flask(__name__)

CORS(
    app,
    supports_credentials=True
)

JSONSerializable(app)  # SpecialThanks...!


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tealDB.db'
app.config['SCRET_KEY'] = '5730292743938474948439320285857603'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    postdate = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(20), nullable=False)
    tweet = db.Column(db.Text, nullable=False)

db.create_all()

@app.route('/')
def index():
    timeline = Post.query.order_by(Post.id.desc()).all()
    return jsonify(timeline)


@app.route('/tweet/<int:id>')
def tweet(id):
    tweet = Post.query.filter_by(id=id).order_by(Post.id.desc()).all()

    return jsonify(tweet)


@app.route('/post', methods=['GET', 'POST'])
def post():
    postdate = datetime.datetime.now(pytz.timezone('Asia/Tokyo')).strftime('%Y/%m/%d - %H:%M:%S')
    username = request.args['username']
    tweet = request.args['tweet']

    createPost = Post(
        postdate=postdate,
        username=username,
        tweet=tweet
    )

    db.session.add(createPost)
    db.session.commit()

    return "post"


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    tweetId = request.args['id']
    removePost = Post.query.get(tweetId)

    db.session.delete(removePost)
    db.session.commit()

    return "delete"
