from PyScripts.divide_and_conquer import guess_socks, rand_num
from PyScripts.n_queens import check_n_queens

from flask import Flask, render_template, request, session
from flask_session import Session
from math import log, ceil

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
    session["max_tries"] = ceil(log(session["total_socks"],2))
    session["num"] = rand_num(1,10)
    session["text"] = "Guess among the socks numbered  1 to {}. Number of tries you have are {}".format(session["total_socks"], session["max_tries"])
    session["wrong_answers"] = 0
    session["hint"] = ''
    return render_template("divide-and-conquer.html")
  elif request.method == "POST":
    if request.form.get("sock"):
      session["guess"] = int(request.form.get("sock"))
      session["text"], session["wrong_answers"] = guess_socks(session["num"], session["guess"], session["wrong_answers"],session["max_tries"])
    elif request.form.get("hint"):
          session["hint"] = "A win in the given amount of tries is guaranteed if one uses the divide and conquer algorithm. Divide the set into two, after recieving the prompt you can then eliminate one of the sets. Keep doing so on the newly required set until you are left with only one sock."
    else:
          session["text"] = "Please choose a sock."
    return render_template("divide-and-conquer.html")
      


@app.route("/n-queens", methods=["GET","POST"])
def n_queens():
  if request.method == "GET":
    hint=''
    session["N"] = 4
    # session["N"] = rand_num(6,15)

    return render_template("n-queens.html",  text='',hint=hint, N = session["N"])
  elif request.method == "POST":
    if request.form.get("check-square"):
      checked = (request.form.getlist("check-square"))
      if len(checked) == session["N"]:
          if check_n_queens(checked, session["N"]) == 1: 
            text = "Congratulations! You have solved the problem. You can look for more solutions if you wish."
          else:
            text = "Sorry, your solution was wrong. Please try again"
      else:
            text = "Please choose EXACTLY {} squares.".format(session["N"])
      return render_template("n-queens.html", text=text,hint='', N = session["N"])
            
    elif request.form.get("hint"):
          hint = "You can use backstrapping to solve the problem."
          return render_template("n-queens.html", text='',hint=hint, N = session["N"])

    else:
          text = "Please choose the positions where you wish to place the queens."
          return render_template("n-queens.html", text=text,hint='', N = session["N"])


@app.route("/dynamic-algorithm")
def dynamic():
    return render_template("dynamic.html")



if __name__ == '__main__':
  app.run(debug=True)