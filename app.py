from PyScripts.divide_and_conquer import guess_socks, rand_num
from flask import Flask, render_template, request, session
from flask_session import Session
import math

app = Flask(__name__)

# Configure session to use as filesystem
app.secret_key = 'superSecretKey'
app.config['SESSION_TYPE'] = 'filesystem'
app.config.from_object(__name__)
Session(app)

@app.route("/")
def home():
  return render_template("index.html")

@app.route("/divide-and-conquer", methods=["GET","POST"])
def divide_and_conquer():
  if request.method == "GET":
    session["total_socks"] = rand_num(10,50)
    session["max_tries"] = math.log(session["total_socks"],2)
    session["num"] = rand_num(1,10)
    session["text"] = "Guess a number between 1 and {}".format(session["total_socks"])
    session["wrong_answers"] = 0
    print("get")
    return render_template("divide-and-conquer.html")
  elif request.method == "POST":
    if request.form.get("sock"):
      session["guess"] = int(request.form.get("sock"))
      session["text"], session["wrong_answers"] = guess_socks(session["num"], session["guess"], session["wrong_answers"],session["max_tries"])
    else:
          session["text"] = "Please choose an option."
    return render_template("divide-and-conquer.html")
      


@app.route("/greedy-algorithm")
def greedy():
    return render_template("greedy.html")

@app.route("/dynamic-algorithm")
def dynamic():
    return render_template("dynamic.html")



if __name__ == '__main__':
  app.run(debug=True)