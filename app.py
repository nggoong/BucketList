from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
# SSL 에러를 해결하기 위해 certifi 패키지 설치
import certifi

mongo_connect = "mongodb+srv://test:sparta@sprta.3peol.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(mongo_connect, tlsCAFile=certifi.where())
db = client.dbsparta

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form['bucket_give']

    bucket_list = list(db.bucket.find({}, {'_id': False}))
    count = len(bucket_list) + 1

    doc={
        'num':count,
        'bucket':bucket_receive,
        'done':0
    }

    db.bucket.insert_one(doc)
    return jsonify({'msg': '등록 완료!!'})

@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    num_receive = request.form['num_give']
    db.bucket.update_one({'num': int(num_receive)}, {'$set': {'done': 1}})
    return jsonify({'msg': '버킷 완료!!'})

@app.route("/bucket/cancel", methods=["POST"])
def bucket_cancel():
    num_receive = request.form['num_give']
    db.bucket.update_one({'num': int(num_receive)}, {'$set': {'done': 0}})
    return jsonify({'msg': '취소 완료!!'})


@app.route("/bucket", methods=["GET"])
def bucket_get():
    bucket_list = list(db.bucket.find({}, {'_id': False}))
    return jsonify({'buckets': bucket_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)