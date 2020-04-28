# Exposure-Notification-on-RPi

Codes and Data for the Exposure Notification on the Raspberry Pi. 

## How to Run The Codes

I write it here in case I forget how to run it in the future. 

Before running the code, some libraries are needed for Raspberry Pi. Note that [bluepy](https://github.com/IanHarvey/bluepy) is used in Python 3. 
```
$ sudo apt install pi-bluetooth
$ sudo apt-get install python-pip libglib2.0-dev
$ sudo pip install bluepy
```
I may forget some libraries I installed. I will check the above list again. 

Next, the bash script (.sh) needs to be executable. To achieve this, run

`$ chmod +x ContractTracing_BLE.sh` 

Finally, run the bash script by typing `$./ContractTracing_BLE.sh`

Done!

## Current Issue(s)

### 1. (4/27/2020) The BLE may die after running a while. The during before it dies is random. 

I have found that the first error usually comes from the Python, i.e., the scanning function. The error code is

`bluepy.btle.BTLEManagementError: Failed to execute management command 'scanend' (code: 3, error: Failed)`

By checking the bluepy source code, the error is from Line 854 to Line 803 to Line 312, and it occurs when running `scan.stop()`. 

My current solution is to reset the BLE by using `sudo hciconfig hci0 reset` when the error happens. It looks that this action fixed the problem and the BLE can run again. (4/28 update: After fixing this by resetting the BLE, the devices runs at least a whole day.)

There are some possible solution for this issue (by searching the Internet):

1. The problem maybe caused by using the Bluetooth and Wi-Fi at the same time, since two modules are in one chip. This may be the case since I found that if I disconnected the VNC (remote access), the two RPis could communication again, even though one of them was dead hardly. 

2. Power supply. Since the BLE chip will consume more power. But I do not quite believe this. 

## To-do List

1. Revise config file so that both bash script and Python can read and import it.
2. Change to the absolute path or current path. 
3. Add function to log the fail events.
4. Removing the judgement of Var1, which is from `... 0x00a 00`.
5. Analyze the probablity that the scanning can't find all the other advertisements. BTW, make a slide drawing the timeline with advertising and scanning. 

## Removed from To-do List

1. Change to the new Apple-Google message format. 
