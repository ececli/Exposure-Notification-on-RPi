# Exposure Notification (Contact Tracing) System on Raspberry Pi

Codes and Data for the Exposure Notification on the Raspberry Pi. Exposure Notification Service, previous is called Contact Tracing, is named by Apple and Google in their [documents](https://www.apple.com/covid19/contacttracing/). The code here implements the Apple-Google Protocol on Raspberry Pis which run Debian-based systems. 

## Project Status: [Active development]

* Fully implemented the [Apple-Google Protocol on Privacy-Preserving Contact Tracing](https://www.apple.com/covid19/contacttracing/) on the Raspberry Pi based system.  

  * Each device can do both advertising (broadcasting) and scanning (observing), and record other devices using the same Contact Tracing Service. It is compatible with other types of devices such as iPhones and Android phones.
  
  * Random and non-resolvable MAC address, random ID (called Rolling Proximity Identifier) and encrypted Data change every 15 minutes to protect privacy

  * Record all the data locally, and it has the functionality to auto-delete data more than 14 days ago. 

* Available in two versions:

  * **The Version with Encryption** - A completed version that implemented Apple-Google Protocol. All the advertising data is encrypted. 
  
  * **The Version without Encryption** - A version that does not apply the encryption. The MAC address is not random, the RPI and metadata are unencrypted. This version can be used for research purposes and data collection. 

* It has the capability to handle hardware glitch. No hardware is perfect. The code can detect when the Bluetooth module fails to work and reset the module immediately. 


## Testing Summary: [complete functional tests]

The developed code has been tested on different models of Raspberry Pi: Raspberry Pi Zero W, Raspberry Pi 3, and Raspberry 4. 

## Getting Started

The code can be used in all the Raspberry Pi models that have Bluetooth module. The cheapest and smallest one is [Raspberry Pi Zero W](https://www.raspberrypi.org/products/raspberry-pi-zero-w/), which is under $10. 

We recommend using the latest [Raspbian System](https://www.raspberrypi.org/downloads/) for a Raspberry Pi. The OS has pre-installed Python 3 and git. 

### Prerequisites

First, Python 3 and bash commands are used to execute the code. The following libraries are required in Python 3. The [bluepy](https://github.com/IanHarvey/bluepy) library is used for Bluetooth scanning, while [pycryptodome](https://pypi.org/project/pycryptodome/) is used for the cryptography part. To install these two, run the following commands:
```
$ sudo pip3 install bluepy
$ sudo pip3 install pycryptodome
```
Next, make sure the bash scripts (.sh) are executable. If not, use the following command:
```
$ chmod +x ContractTracing_BLE.sh
$ chmod +x ContractTracing_BLE_Enpt.sh
```

### Using the Version with Encryption
If you are using the version with encryption, you need to set up `Encrypt_RPI_AEM.py` to be executed automatically and periodically. To do so, you need to use `crontab -e` and add 
```
*/15 * * * * cd YOUR_PATH/Exposure-Notification-on-RPi/ && python3 Encrypt_RPI_AEM.py
```
This line ensures that the system will execute `Encrypt_RPI_AEM.py` file every 15 minutes, so that the random MAC address, Rolling Proximity Identifier (RPI) and (Associated Encrypted Metadata) AEM changed every 15 minutes. Remember to change `YOUT_PATH`. 

You can wait after the system executes `Encrypt_RPI_AEM.py` once, or you can manually execute `Encrypt_RPI_AEM.py` to generate the TEK. Once the TEK is generated, you can run the code by typing
```
$ ./ContractTracing_BLE_Enpy.sh
```
The result is stored in a `CTData_XXXX_Enpt.csv` file in the `Data` folder. 

### Using the Version without Encryption

If you do not need the version with encryption, you do not need to set up `Encrypt_RPI_AEM.py`. Instead, you may want to change the RPI in the `STATIC_RPI.conf`. Otherwise, you will see multiple devices that have the same RPI. To execute the code, run
```
$ ./ContractTracing_BLE.sh
```
The result is stored in a `CTData_XXXX.csv` file in the `Data` folder. 

### Explanation of the Output

**1. The Version with Encryption**

The code records the information of other BLE devices that use the same service (the Exposure Notification Service). The output is in a `CTData_XXXX_Enpt.csv` file. An example of the csv file is given below. 

<img src="https://github.com/ececli/Exposure-Notification-on-RPi/blob/master/images/Example_Enctypted_Data.PNG">

The first column is the [Unix Time](https://en.wikipedia.org/wiki/Unix_time) and its unit is second. The second column is the MAC addresses of the other BLE devices. This could be a random non-resolvable MAC address or a public MAC address, depending on the protocol the other devices use.  

The third column is the received RSSI (dBm). The fourth column is the Service UUID, and it is 0xFD6F for the Exposure Notification Service. The fifth column is the RPI of the other devices, and the last column is the encrypted metadata. 

**2. The Version without Encryption**

The code records the information of other BLE devices that use the same service (the Exposure Notification Service). The output is in a `CTData_XXXX.csv` file. The format of the csv file is partially different from the formate of the version with encryption (shown above).

<!--<img src="/images/Example_Output_ContactTracing.PNG">-->
<img src="https://github.com/ececli/Exposure-Notification-on-RPi/blob/master/images/Example_Output_ContactTracing.PNG">

The first five columns are the same as the csv file in the version with encryption. The difference is in the metadata part. The metadata contains the version of the service, the transmit power, and the reserved part. In the encrypted version, the metadata is encrypted. Thus, the receiver cannot decode the information. In the unencrypted version, however, the receiver can obtain all the information in the metadata. Therefore, the sixth column is the version of the service. Currently, it is 0x40. The next column is the transmit power level (dBm). The hex value 0x0C is 12 in decimal. So it is 12dBm. The last column is reserved for future use. The detailed information about Service UUID, RPI, and metadata can be found [here](https://www.apple.com/covid19/contacttracing/). 

## Contributing

Please read [CONTRIBUTING.md](/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors & Main Contributors

Chang Li (ANTD/ITL/NIST): Implemented the Bluetooth communication part based on [Bluetooth Specification](https://www.apple.com/covid19/contacttracing/). Built-up the system and tested it. 

Lu Shi (ANTD/ITL/NIST): Implemented the cryptography part based on [Cryptography Specification](https://www.apple.com/covid19/contacttracing/). Wrote the Python file [cryptolib.py](\cryptolib.py)

<!--See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.-->

## Related Work

This works implements [Apple-Google Protocol on Privacy-Preserving Contact Tracing](https://www.apple.com/covid19/contacttracing/). The detailed information can be found on their website and documents. 



## Copyright

See [LICENSE.md](/LICENSE.md)

<!--
## Acknowledgments

*Note: Add this if you want to acknowledge people beyond the main contributors.*

* Hat tip to anyone whose code was used
* Inspiration
* etc
-->
## Contact

Please contact Chang Li (<chang.li@nist.gov>), Lu Shi (<lu.shi@nist.gov>), or Nader Moayeri (<nader.moayeri@nist.gov>) if you have any questions. Thank you.
