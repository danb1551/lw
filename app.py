from flask import Flask, render_template, url_for, send_file, request, jsonify
import db

app = Flask(__name__)

@app.errorhandler(404)
def NotFound(e=None):
    return "Jdeš na to špatně", 404

@app.errorhandler(500)
def InternalServerError():
    "Server jsem naprogramoval blbě, někde se stala chyba", 500

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/messages", methods=["GET", "POST"])
def messages():
    if request.method == "GET":
        if request.args.get("data") == "true":
            return jsonify({"messages": db.getMessages()}), 200
        return render_template("messages.html", db.getMessages()), 200
    elif request.method == "POST":
        db.createMessage(request.form.get("message"))
        return jsonify({}), 201

@app.route("/message/<uuid>", methods=["GET", "PUT", "DELETE"])
def messagesUUID(uuid: str):
    if request.method == "GET":
        message = db.getMessage(uuid)
        if message is not None:
            return jsonify(message), 200
        else:
            return jsonify({"error": "message do not exists"}), 404
    elif request.method == "PUT":
        db.editMessage(uuid, request.form.get("message"))
        return jsonify({"success": "message sucesfully edited"}), 
    elif request.method == "DELETE":
        db.deleteMessage(uuid)
        return jsonify({}), 204

if __name__ == "__main__":
    app.run(port=8000)
