from flask import Flask,render_template,url_for
app = Flask(__name__)


posts= [
    {
        "author": "Akanksha Jagtap",
        "title" : "My first Post",
        "content" : "This is my first Post",
        "date_posted" : "April 30 2023"
    },
    {
        "author": "Akanksha Jagtap",
        "title" : "My second Post",
        "content" : "This is my second Post",
        "date_posted" : "April 30 2024"
    }

]

@app.route("/")
def hello():
    return render_template("home.html", posts = posts)

@app.route("/about")
def about():
    return render_template("about.html", title = "About")

if __name__ == "__main__":
    app.run(debug=True)