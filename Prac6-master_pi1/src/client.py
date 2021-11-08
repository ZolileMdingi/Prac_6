import busio
import digitalio
import board
import threading
import time
import socket
import datetime
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn


spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI) #setup SPI 
cs = digitalio.DigitalInOut(board.D8) #set up CS/SHDN pin at GPIO pin 8

mcp = MCP.MCP3008(spi, cs) #create MCP3008 instnace to interface with 
ldr_channel = AnalogIn(mcp, MCP.P2) #interface MCP3008 instnace with channel 2 device(ldr)
temp_channel = AnalogIn(mcp, MCP.P1)#interface MCP3008 instnace with channel 1 device(temp sensor)
seconds_change = 10 #default runtime change
theSocket = None
sending = True
TCP_IP = '192.168.137.20'
#TCP_IP = '127.0.0.1'
TCP_PORT = 1234
BUFFER_SIZE = 2048

def temp_in_C(voltageVal):
    ADC_VREF = 5 #vref
    MCP9700_T_COEFF = 0.01 #in datasheet
    MCP9700_OFFSET = 0.5#also in datasheet
    return round((voltageVal-MCP9700_OFFSET)/MCP9700_T_COEFF )# degree celsuis 

def lrd_channelValue():
    return ldr_channel.value

def tempValue():
    value = temp_channel.value
    return value, temp_in_C(temp_channel.voltage)

def connectServer():
    socketVal = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketVal.connect((TCP_IP, TCP_PORT))
    return socketVal

def handleCommands():
    global sending
    while(True):
        data = theSocket.recv(BUFFER_SIZE).decode()
        if data == 'SensorOn':
            sending =True
            theSocket.send('SENDACK'.encode())
        elif data == 'SensorOff':
            sending = False
            theSocket.send('SENDACK'.encode())
        elif data == 'Status':
            sending = False
            theSocket.send('ON'.encode())
            time.sleep(seconds_change)
            sending = True

if __name__ == '__main__':
    theSocket = connectServer()

    thread =  threading.Thread(target=handleCommands,args=())
    thread.start()
    while(True):
        while(sending):
            ldr = lrd_channelValue()
            tempReading, tempC = tempValue()
            data = str(datetime.datetime.now(datetime.timezone.utc).strftime("%H:%M:%S"))+" "+str(ldr)+" "+str(tempReading)+" "+str(tempC)
            print(data)
            theSocket.send(data.encode())
            time.sleep(seconds_change) 
        

    