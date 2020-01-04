import bus_service, time, sys, signal
import binascii
import select

# ---------------------------------------------------------------------------------------------
# example of use of "bus_service.py"
# ---------------------------------------------------------------------------------------------

def signal_handler(sig, frame):
    print('\r\nEND of session')
    sys.exit(0)
# ---------------------------------------------------------------------------------------------

if __name__ == "__main__":
#  print ('Connect server ', str(sys.argv[1]))

  signal.signal(signal.SIGINT, signal_handler)

  telegrams = []
  device = []
  device.append('0')

  sock = bus_service.OpenBus(str(sys.argv[1]))
  if sock:
     sock = bus_service.LoopBus(sock,telegrams)
  while sock:
  
# start applicazione ---------------------------------------------------------------------------
    tel = bus_service.getNext(telegrams)
    telAscii = bus_service.getSameAscii()

    if tel != 0 and tel[0] == 0xA8 and tel[3] == 0x12:
       azione = "xx"
       tipo = "xx"
       if tel[4] == 0x00:  azione = "ON"
       if tel[4] == 0x01:  azione = "OFF"
       if tel[4] == 0x08:  azione = "UP"
       if tel[4] == 0x09:  azione = "DOWN"
       if tel[4] == 0x0A:  azione = "STOP"
       if (tel[4] & 0x0F) == 0x0D:  azione = "CHANGE"
       if (tel[1] > 0xB0):
           device[0] = tel[2]
           tipo = "confirm "
       else:
           device[0] = tel[1]
           tipo = "request "
       dev = binascii.hexlify(bytearray(device)).decode('ascii')
       print ('telegram: ' + str(telAscii) + ' ... Device: 0x' + str(dev) + ' action ' + str(tipo) + str(azione))

       if sock and tel[2] == 0x31 and tel[4] == 0x01:  # se viene spenta la luce 31
          print('power on device 37')
          sock = bus_service.putMessage(sock, 0x01, 0x37, 0x12, 0x00)  #    accende la luce 37

# end applicazione ---------------------------------------------------------------------------
    if sock:
       sock = bus_service.LoopBus(sock,telegrams)
# end while

  if sock:   sock.close()
