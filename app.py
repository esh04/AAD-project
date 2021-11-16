from PyScripts.divide_and_conquer import guess_socks, rand_num
from flask import Flask, render_template, request, session
from flask_session import Session

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
    session["num"] = rand_num()
    guess = request.form.get("sock")
    
    return render_template("divide-and-conquer.html")
  elif request.method == "POST":
    return render_template("divide-and-conquer.html")
      


@app.route("/greedy-algorithm")
def greedy():
    return render_template("greedy.html")

@app.route("/dynamic-algorithm")
def dynamic():
    return render_template("dynamic.html")



if __name__ == '__main__':
  app.run(debug=True)