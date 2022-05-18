from flask import Flask, render_template, request, redirect, flash, session
from . vtools import validate

app = Flask(__name__)
app.secret_key = "donkey"
@app.route("/")
def hello_world():
    elf = validate.validate("donkey")
    return render_template('index.html', title="Donkey", stage="password")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return redirect('/')
    else:
        if request.form["stage"] != "otp":
            usr = request.form["usr"]
            pwd = request.form["pwd"]
            result = validate.authenticate(usr, pwd, request)
            if not session["authenticated"]:
                flash("Access denied")
            else:
                return render_template('index.html', title="Donkey", stage="otp", username=usr)
        else:
            result = validate.otpcheck(session["username"], request)
            if session["otp"]:
                return redirect('/secret')
        return render_template('index.html', title="Donkey", stage="password")

@app.route("/secret")
def secret():
    try:
        print(session)
        if session["authenticated"] and session["otp"]:
            print(request.cookies)
            return render_template("secret.html", title="Secret world!", username=session["username"])
        else:
            return redirect('/')
    except Exception as e:
        print("Exception: ", e)
        return redirect('/')

@app.route("/logout")
def logout():
    try:
        validate.logout(session["username"])
    except:
        app.logger.info("Logout function hit with no active session")
    return redirect('/')

if __name__ == '__main__':
   app.run()