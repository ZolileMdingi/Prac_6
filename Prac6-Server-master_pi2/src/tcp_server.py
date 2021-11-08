from flask import Flask, render_template, request, send_file
import socket
import threading
import os
import csv
from datetime import datetime

# Connection Data
host = '192.168.137.20'
#host = '127.0.0.1'
port = 1234

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Variables
client = None
nicknames = []
button_status = 'SensorOff'
status = 'OFF'
headings = ["No.","Date_Time", "Temp_Readings", "LDR_Readings"]
data =[]


### The WebInterface part
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    print(request.method)
    global button_status
    global status
    if request.method == 'POST':
        if request.form.get('SensorOn') == 'SensorOn':
            # pass
            button_status = "SensorOn"
            client.send(button_status.encode())
            print(button_status)
        elif  request.form.get('SensorOff') == 'SensorOff':
            # pass # do something else
            button_status = "SensorOff"
            client.send(button_status.encode())
            print(button_status)
        elif  request.form.get('Status') == 'Status':
            print("Status")
            if button_status == 'SensorOn':
                status = 'ON'
            else:
                status = 'OFF'
            return render_template("hello.html", status=status)
        elif  request.form.get('LogCheck') == 'LogCheck':
            # pass # do something else
            print("LogChek")
            return render_template("hello.html", headings=headings, data=data)
        elif  request.form.get('LogDownload') == 'LogDownload':
            with open('sensorlog.csv', 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                # Writing the header
                writer.writerow(headings)

                # writing the body data
                for row in data:
                    writer.writerow(row)
            print("LogDownload")
            path = os.getcwd()+"/sensorlog.csv"
            return send_file(path, as_attachment=True)
        elif  request.form.get('Exit()') == 'Exit()':
            # pass # do something else
            print("Exit()")
        else:
            # pass # unknown
            return render_template("hello.html")
    elif request.method == 'GET':
        # return render_template("index.html")
        print("No Post Back Call")
    return render_template("hello.html")

# Handling Messages From Clients
def handle(client):
    global data
    while True:
                message = client.recv(2048).decode()
                data.append(message)
                print(message)
                


        

# Receiving / Listening Function
def receive():
    #
    #why is this while tru
    while(True):
        # Accept Connection
        global client
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        global button_status
        client.send(button_status.encode('ascii'))
        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
    


if __name__ == '__main__':
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=80, debug=True, use_reloader=False)).start()
    receive()