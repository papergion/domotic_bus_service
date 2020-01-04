import socket
import sys
import struct
import binascii
import signal
# ---------------------------------------------------------------------------------------------
# domotic  bus_service library
# ---------------------------------------------------------------------------------------------
def OpenBus(ipaddress):
  # Create a TCP/IP socket
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  # Connect the socket to the port where the server is listening
  server_address = (ipaddress, 5045)

  try:
    print('connecting to {} port {}'.format(*server_address))
    sock.connect(server_address)

    # Send initialize stream

    message = b'@\x15@c@MX@F3@Y0@l@\x15'  # @TT
#   print('sending {!r}'.format(message))
    sock.sendall(message)
    return sock

  except:
    print('not open - socket error')
    sock.close()
    return 0

# ---------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------
def LoopBus(sock,telegrams):

  try:
    # Look for the messages
    datl = sock.recv(1)
    if datl:
      dati = struct.unpack('B', datl)[0]
      if dati > 0 and dati < 16:
        r = 0
        data = b''
#        print(dati)
        while (r < dati):
          r += len(data)
          data += sock.recv(dati-r)

#       print('received {!r}'.format(data))
#        print(binascii.hexlify(bytearray(data)).decode('ascii'))

        telegrams.append(data)
#       telegrams.append(binascii.hexlify(bytearray(data)).decode('ascii'))

    return sock

  except:
    print('closing socket')
    sock.close()
    return 0

# ---------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------
def putMessage(sock, fromDev, toDev, typeCmd, valCmd):
  try:
    message = bytearray()
    message.append(0x40)    # '@'
    message.append(0x79)    # 'y'
    message.append(toDev)
    message.append(fromDev)
    message.append(typeCmd)
    message.append(valCmd)

    sock.sendall(message)
#    print('write ok')
    return sock

  except:
    print('write error')
    sock.close()
    return 0
# ---------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------
def getNext(telegrams):
  global row
  if len(telegrams) > 0:
     row = telegrams[0]
     next = telegrams[0]
     del (telegrams[0])
     return next
  else:
     return 0
# ---------------------------------------------------------------------------------------------
def getNextAscii(telegrams):
  global row
  if len(telegrams) > 0:
     row = telegrams[0]
     next = binascii.hexlify(bytearray(telegrams[0])).decode('ascii')
     del (telegrams[0])
     return next
  else:
     return 0
# ---------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------
def getSame():
  global row
  a = row
  row = None
  return a
# ---------------------------------------------------------------------------------------------
def getSameAscii():
  global row
  a = row
  row = None
  return binascii.hexlify(bytearray(a)).decode('ascii')
# ---------------------------------------------------------------------------------------------

def signal_handler(sig, frame):
    print('\r\nEND of session')
    sys.exit(0)

# ---------------------------------------------------------------------------------------------

if __name__ == "__main__":
#  print ('Connect server ', str(sys.argv[1]))

  signal.signal(signal.SIGINT, signal_handler)

  sock = OpenBus(str(sys.argv[1]))

  while sock:
    sock = LoopBus(sock)
