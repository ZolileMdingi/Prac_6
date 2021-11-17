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
Then add your balena application's remote:
```
$ git remote add balena username@git.balena-cloud.com:username/myapp.git
```
and push the code to the newly added remote:
```
$ git push balena master
```
It should take a few minutes for the code to push. Enable device URLs so we can see the server outside of our local network. This option can be toggled on the device summary page or in the `Actions` tab in your device dashboards.

Then in your browser you should be able to open the device URL and see the message "Hello World!".

