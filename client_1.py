import socket


def main():

    SERVER_IP = '127.0.0.1'
    connected = False

    #Connecting to server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((SERVER_IP, 54321))
        connected = True
        print "connected"
        sock.send(raw_input("Enter username: "))
        sock.send(raw_input("Enter password: "))
    except socket.error:
        print "Server not found!"
    while connected:
        pass


if __name__ == '__main__':
    main()