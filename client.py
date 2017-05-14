# -*- coding: utf-8 -*-
import socket
import select
import msvcrt
import os


def main():

    file_num = 1
    reading_flag = False
    process_file_packets = []

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 54321))
    print "connected"
    request = ""
    messages = []
    while True:
        rlist, wlist, xlist = select.select([sock], [sock], [])
        if msvcrt.kbhit():
            char = msvcrt.getch()
            if char == '\r':
                print
                messages.append(request)
                request = ""
            elif char == '\x1b':
                sock.close()
                break
            else:
                if char == "\x08":
                    request = request[:-1]
                    print request, ' \b\r',
                else:
                    request += char
                    print request + '\r',
        if rlist:
            data = sock.recv(1024)
            if data == "":
                break
            else: #there is data to be read
                if reading_flag:
                    if "!!END!!" in data:
                        reading_flag = False
                        if data != "!!END!!":
                            process_file_packets.append(data[data.find("!!END!!") + 7:])
                        process_file_packets, file_num = reassemble_file(process_file_packets, file_num)
                    else:
                        process_file_packets.append(data)
                elif "!!START!!" in data:
                    reading_flag = True
                    if data != "!!START!!":
                        process_file_packets.append(data[data.find("!!START!!") + 9:])
                else:
                    print data
        for message in messages:
            sock.send(message)
            messages.remove(message)
    print "connection closed"
    raw_input("press any key to continue...")


def reassemble_file(pfp, file_num):
    file_name = "file_{}.jpg".format(file_num)
    while file_name in os.listdir(os.getcwd()):
        file_num += 1
        file_name = "file_{}.jpg".format(file_num)
    f = open(file_name, "ab")
    for item in pfp:
        f.write(item)
    f.close()
    return [], file_num


if __name__ == "__main__":
    main()
