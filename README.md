# domotic_bus_service
A library for interact with domotic bus (scs, konnex) using esp_scsgate and esp_knxgate devices

This is a python3 application - can be used in linux environment (raspberry).

[![version](https://img.shields.io/badge/version-1.0.0-brightgreen.svg)](CHANGELOG.md)
[![home](https://img.shields.io/static/v1?label=home&message=guidopic&color=orange)](https://guidopic.altervista.org)

## History

First version. Sorry for the trivial software solution. This is my first try with python.

## Usage

The software is very easy to use:
	import bus_service
	functions and parameters:
		bus_service.OpenBus(ipaddress)    open tcp communication with ESP_SCSGATE or ESP_KNXGATE at <ipaddress>
						return socket address of channel  or  zero if failed

		bus_service.LoopBus(socket, telegrams)		provide non-blocking function for verify, read, accumulate 
		                                telegrams readed from bus. This function MUST be called minimum 10 times 
							per second to ensure to not lose any telegram
                                               	socket must be tcpip socket provided by OpenBus
						telegrams must be a buffer area for received data - in example define it 
						    as  telegrams[] 
						return socket address of channel  or  zero if failed

		bus_service.getNext(telegrams)	read and delete fron queue next telegram to elaborate
						telegrams must be the same buffer user in LoopBus function 
						return telegram in byte literal hex format 
							or zero if no telegrams are waiting

		bus_service.getNextAscii(telegrams)	read and delete fron queue next telegram to elaborate
						telegrams must be the same buffer user in LoopBus function 
						return telegram in ascii format or zero if no telegrams are waiting

		bus_service.getSame()		return the same telegram alreay elaborated
						return telegram in byte literal hex format 
							or zero if no telegrams are waiting

		bus_service.getSameAscii()	return the same telegram alreay elaborated
						return telegram in ascii format or zero if no telegrams are waiting

		bus_service.putMessage(socket, fromDev, toDev, typeCmd, valCmd)	 ==>SCS<== request write of telegram
                                               	socket must be tcpip socket provided by OpenBus
						fromDev is address of sender, in byte format
						toDev   is address of destination, in byte format
						typeCmd is type of command in SCS bus (0x12 for command type)
						valCmd  is value of command in byte format
						return socket address of channel  or  zero if failed

		bus_service.putMessage(socket, fromDev, toLineSect, toDev, valCmd)   ==>KNX<== request write of telegram
                                               	socket must be tcpip socket provided by OpenBus
						fromDev is address of sender, in byte format
						toLineSect  is address of destination line and sector, in byte format
						toDev   is address of destination device, in byte format
						valCmd  is value of command in byte format
						return socket address of channel  or  zero if failed

## Example

The software in example connect to ESP_SCSGATE, then display and explain the telegrams found.
When receive a telegram that poweroff light 31 it poweron light 37.

## Example usage

        python3 bus_service_example.py xxx.xxx.xxx.xxx   (ip address of gate device)
                          exit with ctrl/c

## Known issues
	- in Windows environment ctrl/c don't work - close cmd window instead
	- in raspbian (python 3.5) , after putMessage function the service receive another time 
		the last tcp buffer received
