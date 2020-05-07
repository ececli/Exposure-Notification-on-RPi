# Exposure Notification (Contact Tracing) System on Raspberry Pi

Codes and Data for the Exposure Notification on the Raspberry Pi. Exposure Notification Service, previous is called Contact Tracing, is named by Apple and Google in their [documents](https://www.apple.com/covid19/contacttracing/). The code here implements the Bluetooth Specification from Apple and Google on Raspberry Pis which run Debian-based systems. 


<!--One Paragraph of project description goes here.  What the software is
about What is the purpose of the software: Reference Implementation, ....

Link back to ANTD/NIST project page to put this project in context.

Example: 
The purpose of this project is to be a guideline for published code.
Published code is defined as code published on github that has an
associated MIDAS record.

And here is a lightly longer description.  It is no easy task to give
things away. Free is not enough. Code that is not re-used is about as
useful as papers that are not referenced. We hope to set standards for
ourselves before others set standards for us. We hope to make our code
well packaged and of high quality so others can use our work.  A PhD is
not required to read this writeup.... blah blah....

-->

## Project Status: [Active development]




## Testing Summary: [complete functional tests]

The developed code has been tested on different models of Raspberry Pi: Raspberry Pi Zero W, Raspberry Pi 3, and Raspberry 4. 


## Getting Started

*Note: This is mandatory*

These instructions will get you a copy of the project up and running on your 
local machine for development and testing purposes. 
See Installing for notes on how to deploy the project on a live system.

### Prerequisites

First, Python 3 and bash commands are used to execute the code. The following libraries are required in Python 3. The [bluepy](https://github.com/IanHarvey/bluepy) library is used for Bluetooth scanning, while [pycryptodome](https://pypi.org/project/pycryptodome/) is used for the cryptography part. To intsall these two, run the following commands:
```
$ sudo pip3 install bluepy
$ sudo pip3 install pycryptodome
```
Next, make sure the bash scripts (.sh) are executable. If not, use the following command:
```
$ chmod +x ContractTracing_BLE.sh
$ chmod +x ContractTracing_BLE_Enpt.sh
```



### System Test

System tests test the whole system.  Add it if relevant to your project.
Publish results here or point to where results are published.  Boast about
the quality of your system tests. It is good for sales.

```
Give an example
```



## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/your/project/CONTRIBUTING.md) 
for details on our code of conduct, and the process for submitting pull requests to us.

## Authors & Main Contributors

Chang Li (ANTD/ITL/NIST): 

Lu Shi (ANTD/ITL/NIST): 

<!--See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.-->

## Related Work

Note: Optional - if there are releated works or background reading
Add links to any papers or publications here if appropriate. 

## Copyright

*Note: Mandatory section. Put the NIST copyright below.*

To see the latest statement, please visit:
https://www.nist.gov/director/copyright-fair-use-and-licensing-statements-srd-data-and-software

Add a directory where you put licenses of any dependent software or if
the project you are working on is a fork.

Also see the [LICENSE.md](https://github.com/your/project/LICENSE.md)

<!--
## Acknowledgments

*Note: Add this if you want to acknowledge people beyond the main contributors.*

* Hat tip to anyone whose code was used
* Inspiration
* etc
-->
## Contact

Please contact Chang Li <chang.li@nist.gov> or Nader Moayeri <nader.moayeri@nist.gov> if you have any questions. Thank you.
