from flask import Flask, render_template, request, send_file
import socket
import threading
import os
import csv
from datetime import datetime

# Connection Data
host = '192.168.137.20'
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
### This is the code responsible for displaying the HTML webInterface
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    print(request.method)
    global button_status
    global status
    if request.method == 'POST':
        if request.form.get('SensorOn') == 'SensorOn':
            button_status = "SensorOn"
            client.send(button_status.encode())
            print(button_status)
        elif  request.form.get('SensorOff') == 'SensorOff':
            button_status = "SensorOff"
            client.send(button_status.encode())
            print(button_status)
        elif  request.form.get('Status') == 'Status':
            print("Status")
            if button_status == 'SensorOn':
                status = 'ON'
            else:
                status = 'OFF'
            return render_template("hello.html", status=status, button_status=button_status)
        elif  request.form.get('LogCheck') == 'LogCheck':
            print("LogChek")
            return render_template("hello.html", headings=headings, data=data[-10:], button_status=button_status)
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
            print("Exit()")
        else:
            return render_template("hello.html", button_status=button_status)
    elif request.method == 'GET':
        print("No Post Back Call")
    return render_template("hello.html", button_status=button_status)

# Handle Incoming messages and Sensor data from the client
def handle(client):
    global data
    while True:
            message = client.recv(2048).decode()
            data.append(message)
            print(message)
                

# Listens for the client to connect
def receive():
    while(True):
        # Accept Connection
        global client
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # sends a SensorOff signal at the start to tell the client to wait for a command before it can start sending the data
        global button_status
        client.send(button_status.encode('ascii'))
        # Start Handling Thread For Client
        # This threads handles receiving data as it continually waits for data to come.
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
    


if __name__ == '__main__':
    # This threads handles running the webInterface
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=80, debug=True, use_reloader=False)).start()
    receive()