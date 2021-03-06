import socket
import select
import msvcrt
import sys
import concurrent.futures


open_client_sockets = []
requested_clients = []
messages = []
try:
    requested_file = sys.argv[1]
except IndexError:
    requested_file = "test.jpg"


def main():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(('0.0.0.0', 54321))
    server_sock.listen(5)
    print "started"

    while True:
        if msvcrt.kbhit():
            if msvcrt.getch() == "\x1b":
                for client in open_client_sockets:
                    client.close()
                print "ended sockets"
                break
        rlist, wlist, xlist = select.select([server_sock] + open_client_sockets, open_client_sockets, [])
        for current in rlist:
            if current is server_sock:
                (new, addr) = server_sock.accept()
                print "new connection\nIP:", addr[0], "\nPort:", addr[1]
                open_client_sockets.append(new)
            else:
                data = current.recv(1024)
                if not data:
                    open_client_sockets.remove(current)
                    print "connection closed"
                else:
                    messages.append((current, "server received: " + data))
                    print "received:", data
                    if data.startswith("GET"):
                        requested_clients.append(current)
        send_messages(wlist)
        for request in requested_clients:
            concurrent.futures.ThreadPoolExecutor(max_workers=4).submit(send_file, request)
            requested_clients.remove(request)


def send_file(client):
    messages.append((client, "!!START!!"))
    print "started reading..."
    f = open(requested_file, 'rb')
    b = f.read()
    messages.append((client, b))
    print "finished reading"
    f.close()
    messages.append((client, "!!END!!"))
    return


def send_messages(wlist):
    for message in messages:
        (client_sock, data) = message #message is a tuple
        if client_sock in wlist:
            client_sock.send(data)
            messages.remove(message)

if __name__ == "__main__":
    main()
