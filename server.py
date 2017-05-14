import socket
import select
import msvcrt
import concurrent.futures


open_client_sockets = []
requested_clients = []
messages = []
f = open("D:\\PycharmProjects\\end_of_the_year_project\\test.jpg", 'rb')


def main():
    server_sock = socket.socket()
    server_sock.bind(('0.0.0.0', 54321))
    server_sock.listen(5)
    print "started"

    while True:
        if msvcrt.kbhit():
            if msvcrt.getch() == "\x1b":
                for client in open_client_sockets:
                    client.send("")
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
    copy = f
    byte_read = copy.read(1024)
    packet_num = 0
    messages.append((client, "(START)({})".format(packet_num)))
    packet_num += 1
    while byte_read:
        messages.append((client, "(" + byte_read + ")" + "({})".format(packet_num)))
        byte_read = copy.read()
        packet_num += 1
    messages.append((client, "(END)({})".format(packet_num)))
    return


def send_messages(wlist):
    for message in messages:
        (client_sock, data) = message #message is a tuple
        if client_sock in wlist:
            client_sock.send(data)
            messages.remove(message)

if __name__ == "__main__":
    main()