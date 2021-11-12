from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def home():
  return render_template("index.html")

@app.route("/divide-and-conquer")
def divide_and_conquer():
    return render_template("divide-and-conquer.html")


if __name__ == '__main__':
  app.run(debug=True)