from PyScripts.divide_and_conquer import guess_socks, rand_num
from flask import Flask, render_template, request, session
from flask_session import Session

app = Flask(__name__)

@app.route("/")
def home():
  return render_template("index.html")

@app.route("/divide-and-conquer", methods=["GET","POST"])
def divide_and_conquer():
    num = rand_num()
    guess = request.form.get("sock")
    
    return render_template("divide-and-conquer.html")


@app.route("/greedy-algorithm")
def greedy():
    return render_template("greedy.html")

@app.route("/dynamic-algorithm")
def dynamic():
    return render_template("dynamic.html")



if __name__ == '__main__':
  app.run(debug=True)