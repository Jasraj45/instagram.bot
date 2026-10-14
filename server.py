from flask import Flask, request, jsonify
from instagrapi import Client
import os

app = Flask(__name__)

ACCOUNTS = [
    {"username": os.environ.get("IG_USER1"), "password": os.environ.get("IG_PASS1")},
    {"username": os.environ.get("IG_USER2"), "password": os.environ.get("IG_PASS2")},
]

clients = []

for acc in ACCOUNTS:
    if not acc["username"] or not acc["password"]:
        continue
    cl = Client()
    try:
        cl.login(acc["username"], acc["password"])
        clients.append(cl)
    except Exception as e:
        print(f"login failed {acc['username']}: {e}")

@app.route('/')
def home():
    return "server running"

@app.route('/follow', methods=['POST'])
def follow():
    data = request.json
    target = data.get('target')
    count = int(data.get('count', 10))
    followed = 0
    for cl in clients:
        if followed >= count:
            break
        try:
            user_id = cl.user_id_from_username(target)
            cl.user_follow(user_id)
            followed += 1
        except Exception as e:
            print(f"follow failed: {e}")
    return jsonify({"followed": followed, "total": len(clients)})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
