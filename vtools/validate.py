from flask import session, flash
import datetime as dt
import logging

"""
This file contains fake validation/authentication scripts. 
The attacker will alter the otpcheck function to send all authenticated sessions 
to the attackers, so they can steal the sessions. 
"""

tool_logger = logging.Logger("tools")

users = {
    "anne": {
        "pw": "aabbcc"
    },
    "admin": {
        "pw": "admin"
    }
}

def authenticate(username, password, request):
    session["username"] = username
    session["authenticated"] = False
    if ratelimit(10, request):
        flash('Too many login attempts.')
        return False
    else:
        try:    
            if password == users[username]["pw"]:
                session["authenticated"] = True
                return True
        except Exception as e:
            tool_logger.info('Error in authentication: ', e)
            return False

def otpcheck(username, request):
    try:
        otp = request.form["otp"]
        if otp == '123456':
            session["otp"] = True
            # Time to steal the session....
            return True
        else:
            session["otp"] = False
            return False
    except Exception as e:
        print("Error in OTP check: ", e)
        session["otp"] = False
        return False

def ratelimit(threshold, request):
    if 'lastfailure' not in session.keys():
        session['numfailed'] = 1
        session['lastfailure'] = dt.datetime.utcnow()
    else:
        tdelta = dt.datetime.utcnow() - session['lastfailure'].replace(tzinfo=None)
        if tdelta.total_seconds() > 300:
            session.pop("numfailed", None)
            session.pop("lastfailure", None)
            return False
        else:
            session['numfailed']+=1
            session['lastfailure'] = dt.datetime.utcnow()
            return session['numfailed'] > threshold

def logout(username):
    session.clear()


def validate(username):
    return "Donkeys are cooler than people"

