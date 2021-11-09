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
TCP_PORT = 1234
BUFFER_SIZE = 2048

def temp_in_C(voltageVal):
    ADC_VREF = 5 #vref
    MCP9700_T_COEFF = 0.01 #in datasheet
    MCP9700_OFFSET = 0.5#also in datasheet
    return round((voltageVal-MCP9700_OFFSET)/MCP9700_T_COEFF )# degree celsuis 

# gets channelValue
def lrd_channelValue():
    return ldr_channel.value

# gets tempValue
def tempValue():
    value = temp_channel.value
    return value, temp_in_C(temp_channel.voltage)

# connects to the tcp_server and returns a a communication object
def connectServer():
    socketVal = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketVal.connect((TCP_IP, TCP_PORT))
    return socketVal

# This function is responsible for receiving commands from the server
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
        elif data == 'exit':
            exit()
        elif data == 'Status':
            sending = False
            theSocket.send('ON'.encode())
            time.sleep(seconds_change)
            sending = True

if __name__ == '__main__':
    theSocket = connectServer()

    thread =  threading.Thread(target=handleCommands,args=()) # This thread makes sure that the clients is always listening to commands
    thread.start()
    # Sending the sensored data from the ldr and the tempReading to the server with the time stamp
    while(True):
        while(sending):
            ldr = lrd_channelValue()
            tempReading, tempC = tempValue()
            data = str(datetime.datetime.now(datetime.timezone.utc).strftime("%H:%M:%S"))+" "+str(ldr)+" "+str(tempReading)+" "+str(tempC)
            print(data)
            theSocket.send(data.encode())
            time.sleep(seconds_change) 
        

    