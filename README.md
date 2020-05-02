# Exposure-Notification-on-RPi

## Introduction

Codes and Data for the Exposure Notification on the Raspberry Pi. Exposure Notification Service, previous is called Contact Tracing, is named by Apple and Google in their [documents](https://www.apple.com/covid19/contacttracing/). The code here implements the Bluetooth Specification from Apple and Google on Raspberry Pis which run Debian-based systems. 

## How to Run The Codes

Before running the code, some libraries are needed for Raspberry Pi. Note that [bluepy](https://github.com/IanHarvey/bluepy) is used in Python 3. 
<!--$ sudo apt install pi-bluetooth-->
```
$ sudo apt-get install python-pip libglib2.0-dev
$ sudo pip3 install bluepy
```
I may forget some libraries I installed. I will check the above list again. 

Next, the bash script (.sh) needs to be executable. To achieve this, run
```
$ chmod +x ContractTracing_BLE.sh
```
Finally, run the bash script by typing `$./ContractTracing_BLE.sh`

Done!

**Note:** Remember to change the Rolling Proximity Identifier (RPI) for each device. It can be changed in [ContactTracing_BLE.conf](/ContactTracing_BLE.conf) file. If you clone the code to multiple devices but forget to change it, all the records will have the same RPI. But you can still identify different devices via MAC address. 

## Explanation of the Output

The program records the information of other BLE devices that use the same service (the Exposure Notification Service). The output is in a .csv file. The format of the csv file is as follows. 

<!--<img src="/images/Example_Output_ContactTracing.PNG">-->
<img src="https://github.com/ececli/Exposure-Notification-on-RPi/blob/master/images/Example_Output_ContactTracing.PNG">

The first column is the [Unix Time](https://en.wikipedia.org/wiki/Unix_time) and its unit is second. The second column is the MAC addresses of the other BLE devices. The third column is the received RSSI (dBm). The fourth column is the Service UUID, and it is 0xFD6F for the Exposure Notification Service. The fifth column is the Rolling Proximity Identifier (RPI), which can be seen as the unique ID of each device. The sixth column is the version of the service. Currently it is 0x40. The next column is the transmit power level (dBm). The hex value 0x0C is 12 in decimal. So it is 12dBm. The last column is reserved for future use. The detailed information about Service UUID and RPI can be found [here](https://www.apple.com/covid19/contacttracing/). 



## Current Issue(s)

### 1. (updated 4/28) The BLE may die after running a while. The duration before it dies is random. 

I have found that the first error usually comes from the Python, i.e., the scanning function. The error code is

`bluepy.btle.BTLEManagementError: Failed to execute management command 'scanend' (code: 3, error: Failed)`

By checking the bluepy source code, the error is from Line 854 to Line 803 to Line 312, and it occurs when running `scan.stop()`. 

My current solution is to reset the BLE by using `sudo hciconfig hci0 reset` when the error happens. It looks that this action fixed the problem and the BLE can run again. 

There are some possible solutions for this issue (by searching the Internet):

1. The problem may be caused by using the Bluetooth and Wi-Fi at the same time, since two modules are in one chip. This may be the case since I found that if I disconnected the VNC (remote access), the two RPis could communication again, even though one of them was dead hardly. 

2. Power supply. Since the BLE chip will consume more power. But I do not quite believe this. 

***4/28 Update:*** After fixing this by resetting the BLE, the devices run at least a whole day. However, after analyzing the collected data, I found that there is a chance that two devices can't see each other for at most 14 minites (which occurs once in an 18 hours continuous running). Not sure if this happens due to the BLE problem or other issues. 

## To-do List

1. Revise config file so that both bash script and Python can read and import it.
2. Change to the absolute path or current path. 
3. Add function to log the fail events.
4. Analyze the probability that the scanning can't find all the other advertisements. BTW, make a slide drawing the timeline with advertising and scanning. 


## Removed from To-do List

1. Change to the new Apple-Google message format. 
2. Removing the judgment of Var1, which is from `... 0x00a 00`. 
3. Integrate the Cryptography Specification from Apple and Google. Currently, the Rolling Proximity Identifier (RPI) is static and I just write some random numbers for it. The Metadata (including Version, TX power, and Reserved) is not encrypted. 
4. Change the MAC address to the random non-resolvable address.
