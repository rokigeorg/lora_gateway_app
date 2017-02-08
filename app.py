from flask import Flask, render_template, request, redirect, url_for
import time
from os import system
import subprocess

app = Flask(__name__)
# Global variables
process_id = 0


def log_the_user_in(_name):
    return redirect(url_for('startgui'))


def valid_login(_usern, _pword):
    print(_usern, _pword)
    if _usern == "georg":
        return True


# @app.route('/', methods=['POST', 'GET'])
# def index():
#    return render_template('index.html')


@app.route('/', methods=['POST', 'GET'])
def index():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('index.html', error=error)


@app.route('/startGUI', methods=['POST', 'GET'])
def startgui():
    if request.method == 'POST':
        if valid_Gateway_Parameter(request.form["frequency"], request.form["sf"], request.form["coderate"],
                                   request.form["bandwidth"]):
            gt_para = {"freq": request.form["frequency"], "sf": request.form["sf"], "cr": request.form["coderate"],
                       "bw": request.form["bandwidth"]}

            # start gate
            if buildGtw():
                return render_template('runningGUI.html', gt_para=gt_para)
            else:
                return render_template('startGUI.html')
    else:
        return render_template('startGUI.html')


def buildGtw():
    # excecute Makefile to build the gateway

    output = system("cd gateway-software && pwd")  # stderr=subprocess.STDOUT)
    print(output)

    procs = []
    cmd = ["make", "run"]
    try:
        procs.append(subprocess.Popen(cmd, shell=True))  # Run program in another process
        print("Process-ID: ", procs[0])
        return True
    except subprocess.CalledProcessError as e:
        print("Calledprocerr")
        return False


def valid_Gateway_Parameter(freq, sf, cr, bw):
    # check freq is a number with
    print(freq, sf, cr, bw)

    if check_sf(sf):
        if check_cr(cr):
            if check_bw(bw):
                return True
    return False


def check_freq(_freq):
    f = len(_freq)
    print(f)
    if f == 9:
        return True
    else:
        return False


def check_sf(_sf):
    if _sf == "SF7":
        return True
    elif _sf == "SF8":
        return True
    elif _sf == "SF9":
        return True
    elif _sf == "SF10":
        return True
    elif _sf == "SF11":
        return True
    elif _sf == "SF12":
        return True
    else:
        return False


def check_bw(_bw):
    if _bw == "125":
        return True
    elif _bw == "250":
        return True
    elif _bw == "500":
        return True
    else:
        return False


def check_cr(_cr):
    if _cr == "4/5":
        return True
    elif _cr == "4/6":
        return True
    elif _cr == "4/7":
        return True
    elif _cr == "4/8":
        return True
    else:
        return False


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
