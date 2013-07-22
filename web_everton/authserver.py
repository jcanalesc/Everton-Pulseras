from flask import Flask, request, jsonify
import hashlib
import bdd

app = Flask(__name__)

@app.route("/authenticate", methods=['POST'])
def autenticar():
	user = request.form["user"]
	passwd = request.form["passwd"]
	userdata = bdd.get_user(user)
	resp = { "auth": False }
	if userdata is not None and userdata["password"] == hashlib.sha256(passwd).hexdigest():
		resp["auth"] = True
	return jsonify(resp)

if __name__ == "__main__":
	app.run("0.0.0.0")
