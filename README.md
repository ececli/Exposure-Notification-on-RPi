# Exposure-Notification-on-RPi

Codes and Data for the Exposure Notification on the Raspberry Pi. 

## How to Run The Codes

I write it here in case I forget how to run it in the future. First, the bash script (.sh) needs to be executable. To achieve this, run

`chmod +x ContractTracing_BLE.sh` 

Then, run the bash script by typing `./ContractTracing_BLE.sh`

Done!

## Current Issue(s)

### 1. (4/27/2020) The BLE may die after running a while. The during before it dies is random. 

I have found that the first error usually comes from the Python, i.e., the scanning function. The error code is

`bluepy.btle.BTLEManagementError: Failed to execute management command 'scanend' (code: 3, error: Failed)`

By checking the bluepy source code, the error is from Line 854 to Line 803 to Line 312, and it occurs when running `scan.stop()`. 

My current solution is to reset the BLE by using `sudo hciconfig hci0 reset` when the error happens. It looks that most of time this action fixed the problem and the BLE can run again. However, there is also some time that the BLE is totally dead after the error.

There are some possible solution for this issue (by searching the Internet):

1. The problem maybe caused by using the Bluetooth and Wi-Fi at the same time, since two modules are in one chip. This may be the case since I found that if I disconnected the VNC (remote access), the two RPis could communication again, even though one of them was dead hardly. 

2. Power supply. Since the BLE chip will consume more power. But I do not quite believe this. 

## To do List

1. Revise config file so that both bash script and Python can read and import it.
2. Change to the absolute path or current path. 
3. Add function to log the fail events.
4. Change to the new Apple-Google message format. 
