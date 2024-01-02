import socket, struct
#from rpi_ws281x import * 
def Initialize_Rasppi(IP,port):
                    #IP string             
                    #port int
                 
    # serverAddressPort   = (IP, port)
    # UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)# Create a UDP socket at client side
    # return serverAddressPort, UDPClientSocket
    
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    clientSocket.connect((IP, port))
    return clientSocket

def send(Data, clientSocket):
        Data_list=Data.tolist()
        Format = '1808B'
        bytesToSend  = struct.pack(Format, *Data_list)
        try:
            clientSocket.sendall(bytesToSend)
            return True
        except:
            print("could not send data")
            print("Attempted to send:")
            print(Data_list)
            print("As Bytes")
            print(bytesToSend)
            return False
            pass