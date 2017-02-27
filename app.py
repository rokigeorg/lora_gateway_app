from flask import Flask, render_template, request, redirect, url_for, session
import time
import os
import subprocess
import shlex

app = Flask(__name__)
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'


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
            if getCurrentPath():
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
    print(gt_para["sf"][-2:])
    print (gt_para["cr"][-1])
    print (gt_para["bw"])
    print (gt_para["ofn"])

    # start the gateway with the given parameter
    # inside the gt_app_obj lives the Gateway programm it will start a
    if startGatewayApp(gt_para):
        return render_template('runningGUI.html', gt_para=gt_para)

    else:
        return redirect(url_for('startgui'))


def startGatewayApp(gt_para):
    current_paths = os.getcwd()
    path_to_gtapp = current_paths + "/gateway-software/main"
    print(path_to_gtapp)

    procs = []
    #cmd = "sudo /home/pi/Workspace/Python3_WebApps/testWebserver/gateway-software/main -f 868100000 -sf 12 -cr 5 -bw 500 -o received_data.txt"
    cmd = "sudo " +  path_to_gtapp +" -f " + gt_para["freq"]+ " -sf " + get_sf_value(gt_para["sf"]) + " -cr " + gt_para["cr"][-1]+ " -bw " + gt_para["bw"] +" -o " +gt_para["ofn"]
    #cmd = ["sudo", path_to_gtapp, "-f", gt_para["freq"], "-sf", get_sf_value(gt_para["sf"]), "-cr", gt_para["cr"][-1], "-bw", gt_para["bw"], "-o", gt_para["ofn"]]
    print (cmd)
    try:

        #b = os.popen(cmd,mode="r")
        procs.append(subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True))  # Run program in another process

        print("Process-Object: ", procs[0])
        print("Process-Pid: ", procs[0].pid)
        print("Process-Args: ", procs[0].args)

        #sudo_prompt = procs[0].communicate(sudo_password + '\n')[1]
        #output, error = procs[0].communicate()

        #procs[0].terminat()
        #print(b.read())

        print(procs[0].poll())

        #session['procs'] = procs

        return True
    except subprocess.CalledProcessError as e:
        print("Calledprocerr")
        print(e)
        return False


def getCurrentPath():
    return True


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


def get_sf_value(_sfVa):
    if len(_sfVa) > 3:
        return _sfVa[-2:]
    else:
        return _sfVa[-1]


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
