# To do List 

Here is the list of the things that have not been done yet. And the list of issues found during the test. 

## To-do List

* Revise config file so that both bash script and Python can read and import it.
* Change to the absolute path or current path. 
* Add function to log the fail events.
* Analyze the probability that the scanning can't find all the other advertisements. BTW, make a slide drawing the timeline with advertising and scanning. 
* Test different scanning and advertising frequency. 
* Random scan time
* Log the key (Lu's work)


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




## Removed from To-do List

1. Change to the new Apple-Google message format. 
2. Removing the judgment of Var1, which is from `... 0x00a 00`. 
3. Integrate the Cryptography Specification from Apple and Google. Currently, the Rolling Proximity Identifier (RPI) is static and I just write some random numbers for it. The Metadata (including Version, TX power, and Reserved) is not encrypted. 
4. Change the MAC address to the random non-resolvable address.
