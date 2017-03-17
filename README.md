
<snippet>
  <content>
# LoRa Communication App

This repository includes a Flasks Web-App to control a LoRa Gateway Software for the Raspberry Pi Model B.
On the Webpage it is possible to adjust the parameters for the Gateway.

Frequency
Spreading Factor
Coding Rate
Bandwidth

The gateway software has to be compile before using the Flasks Web-App.
The gateway software can receive unencrypted and encrypted payload.
In this repository the default settings of the gateway are set for unencrypted LoRa communication.


### Requirements for the gateway-software
* enable SPI -> check in  ```$ raspi-config``` on RPi
* WiringPi: to access GPIO -> install ```$ sudo apt-get install wiringpi```
* start program as root ``$ sudo ./main``

### Requirements for the Flasks Web-App
* install Flasks App fi you haven't already ``` sudo apt-get install python3-flask ```


## Usage
1. Clone this repository to your Raspberry Pi ```git clone https://github.com/rokigeorg/lora_gateway_app ```
2. Change the directory ``` cd gateway-software```
3. Compile the gateway software ``` make ```
4. Change the directory to again ``` cd .. ```
5. Start the Flasks Web ``` python3 app.py ```
6. Open the Browser and enter the URL ```localhost:5000```
7. Enter Username ``` admin ``` Password empty

Additional information
The gateway software will write all the received LoRa Packages into a file with the corresponding RSSI value.



</content>
  <tabTrigger>readme</tabTrigger>
</snippet>