# Pi1 Client-fleet source code

## Overview functionality of pi1 client code
Pi1 is responsible for collecting the data that it is receiving from the Light Dependent Resistor (LDR) and the temperature sensors and send this data to Pi2. All the code for reading the LDR & Temperature Sensor, connecting to pi2, listening to pi2 commands and sending the data to pi2 can be found in the client.py file. 

On start-up pi1 sends a connection request to pi2 on failing to establish the connection it restarts the connection, on successful establishing of connection pi1 waits for commands on pi2 to tell it to start sending data or to send the status of whether the sensors are active or not. If pi1 receives the SensorOn command it turns the sensor on and start sending the data it got from the sensors together with their timestamps. When pi1 receives the SensorOff command it turns the sensors off and stop sending the data.

## Follow the Circuit diagram below to build your sensors circuit connected to the pi1.
![image](https://user-images.githubusercontent.com/62191335/142273981-ee53dde6-bade-45da-b607-f0d658c18159.png)

## How to push the code to Balena and Run it in your pi1
Assuming that you already set-up your pi1 with balena os and you have your pi1 fleet on the Balena Web portal.

You will need to clone this repo locally:
```
$ git clone https://github.com/ZolileMdingi/Prac_6/tree/main/Prac6-master_pi1
```
Open your terminal if on Linux or cmd in windows directly Prac6-master_pi1 folder.
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
It should take a few minutes for the code to push. Once you see a Unicorn it means its done pushing.
You can go do the same thing for the [pi2-server]

## Alternative to Deploy to your fleet
Flow this link [deploy to your fleet method 2] or watch [YouTube Tutorial] timestamp 3:23

## A screenshot of the Balena webportal showing both Pis up and running
<img width="980" alt="balenaFleets" src="https://user-images.githubusercontent.com/62191335/142738862-e085f408-1ec0-4578-b132-668454324121.PNG">


[pi2-server]:https://github.com/ZolileMdingi/Prac_6/tree/main/Prac6-Server-master_pi2
[deploy to your fleet method 2]:https://www.balena.io/docs/learn/deploy/deployment/#:~:text=You%20can%20find%20the%20fleet,run%20git%20push%20balena%20master%20.
[YouTube Tutorial]:https://youtu.be/Tm4N5GcJRLI
