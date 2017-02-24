from flask import Flask, render_template, request, redirect, url_for
import time
from os import system
import subprocess
import shlex

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
        gt_para = {"freq": request.form["frequency"],
                   "sf": request.form["sf"],
                   "cr": request.form["coderate"],
                   "bw": request.form["bandwidth"],
                   "ofn": request.form["outputfile"]
                   }

        if valid_gateway_parameter(gt_para["freq"], gt_para["sf"], gt_para["cr"], gt_para["bw"], gt_para["ofn"]):
            print(gt_para["ofn"])

            # start gate
            if buildGtw():
                return redirect(url_for('runningGUI', freq=request.form["frequency"], sf=request.form["sf"], cr=request.form["coderate"], bw=request.form["bandwidth"], ofn=gt_para["ofn"]))
                #return render_template('runningGUI.html', gt_para=gt_para)
            else:
                return render_template('startGUI.html')
    else:
        return render_template('startGUI.html')


@app.route('/runningGUI',  methods=['POST', 'GET'])
def runningGUI():
    gt_para = {"freq": request.args["freq"],
               "sf": request.args["sf"],
               "cr": request.args["cr"],
               "bw": request.args["bw"],
               "ofn": request.args["ofn"]
               }

    print(gt_para["freq"])
    print(gt_para["sf"][-1])
    print (gt_para["cr"][-1])
    print (gt_para["bw"])
    print (gt_para["ofn"])

    # start the gateway with the given parameter
    if startGatewayApp(gt_para):
        return render_template('runningGUI.html', gt_para=gt_para)
    else:
        return "Fuck" #redirect(url_for('startgui'))


def startGatewayApp(gt_para):

    procs = []
    #cmd = ["sudo ", "./main", "-f", gt_para["freq"], "-sf", gt_para["sf"][-1], "-cr", gt_para["cr"][-1], "-bw", gt_para["bw"], "-o", gt_para["ofn"]]
    #cmd = "sudo ./main -f 868100000 -sf 7 -cr 5 -bw 500 -o received_data.txt"
    cmd = ["make", " run"]
    print (cmd)
    try:
        subprocess.call(cmd, shell=True)
        #procs.append(subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE))  # Run program in another process
        # procs[0].communicate()
        # procs[0] = subprocess.Popen(["./main"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        #print("Process-ID: ", procs[0])
        return True
    except subprocess.CalledProcessError as e:
        print("Calledprocerr")
        print(e)
        return False


def buildGtw():
    # excecute Makefile to build the gateway

    output = system("cd gateway-software && pwd")  # stderr=subprocess.STDOUT)
    print(output)

    return True
#    procs = []
 #   cmd = ["sudo", "./main", "-f", "868100000", "-sf", "12", "-cr", "5", "-bw", "500"]
    #cmd = ["make", "comprun"]
  #  try:
   #     procs.append(subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE))  # Run program in another process
        #procs[0].communicate()
        #procs[0] = subprocess.Popen(["./main"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #run_command(cmd)

    #    print("Process-ID: ", procs[0])
     #   return True
    #except subprocess.CalledProcessError as e:
     #   print("Calledprocerr")
      #  return False


def valid_gateway_parameter(freq, sf, cr, bw, ofn):
    # check freq is a number with
    print(freq, sf, cr, bw)

    if check_sf(sf):
        if check_cr(cr):
            if check_bw(bw):
                if check_ofn(ofn):
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


def check_ofn(_ofn):
    if _ofn == "":
        return False
    else:
        return True


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
