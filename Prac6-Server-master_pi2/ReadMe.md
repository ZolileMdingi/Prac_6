# Pi2 Server-fleet source code

## Watch Application Demostration video of 6 functionality
[Watch it on YouTube here] alternative [OneDrive]

## Overview functionality of pi2 server code
Pi2 is responsible for hosting the web Interface, creating a tcp_server to listen for when the client connects, receive the data that the client is sending, sends commands to the client telling client to send data, turn off the sensor, send status of the sensors, it also generates the sensorlog.csv that it stores all the sensor data it got from client.

On start-up pi2 starts up the tcp_server and waits for client(pi1) to connect, it then generate the sensorlog.csv that it will use to store the data it from client and start a thread that will host the web interface and pass on the commands from the web interface to the tcp_server so that the server can send the commands to the pi1(client).

## How to push the code to Balena and Run it in your pi2
Assuming that you already set-up your pi2 with balena os and you have your pi2 fleet on the Balena Web portal.

Learn how to [setup your fleet here]

You will need to clone this repo locally:
```
$ git clone https://github.com/ZolileMdingi/Prac_6/tree/main/Prac6-Server-master_pi2
```
Open your terminal if on Linux or cmd in windows directly Prac6-Server-master_pi2 folder.
Then Login to your Balena web portal client (Select Web authorization as is recommended):
```
$ balena login
```
Next run this command to display your fleets if you have forgetten your fleets names( Take a note of your fleets name):
```
$ balena fleets
```
and push the code to the rightful fleet:
```
$ balena push <fleetName>
```
It should take a few minutes for the code to push. Once you see a Unicorn it means its done pushing.To give your device a public URL, access the device page, and choose the Public Device URL toggle. You may also activate this for many devices in your fleet at the same time via the Actions menu on the device list within a fleet.

You can go do the same thing for the [pi1-client]

## Alternative to Deploy to your fleet
Flow this link [deploy to your fleet method 2] or watch [YouTube Tutorial] timestamp 3:23

## A screenshot of the Balena webportal showing both Pis up and running
<img width="980" alt="balenaFleets" src="https://user-images.githubusercontent.com/62191335/142738862-e085f408-1ec0-4578-b132-668454324121.PNG">

## A screenshot of your webpage providing the 6 functions required.
<img width="980" alt="interface" src="https://user-images.githubusercontent.com/62191335/142739212-04cae348-b0a0-44e8-a694-496df2472d5b.PNG">


[pi1-client]:https://github.com/ZolileMdingi/Prac_6/tree/main/Prac6-master_pi1
[deploy to your fleet method 2]:https://www.balena.io/docs/learn/deploy/deployment/#:~:text=You%20can%20find%20the%20fleet,run%20git%20push%20balena%20master%20.
[YouTube Tutorial]:https://youtu.be/Tm4N5GcJRLI
[setup your fleet here]:https://youtu.be/Tm4N5GcJRLI

[Watch it on YouTube here]:https://youtu.be/HTdSyrU7SBQ
[OneDrive]:https://uctcloud-my.sharepoint.com/:v:/g/personal/mdnave001_myuct_ac_za/EWj5S8mYaG5NjAJC8wN7KokBREjG6kPqu2is6rZBHVAOpQ
