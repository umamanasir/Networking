'''
This module defines the behaviour of a client in your Chat Application
'''
import sys
import getopt
import socket
import random
from threading import Thread
import os
import util


'''
Write your code inside this class. 
In the start() function, you will read user-input and act accordingly.
receive_handler() function is running another thread and you have to listen 
for incoming messages in this function.
'''

class Client:
    '''
    This is the main Client Class. 
    '''
    def __init__(self, username, dest, port, window_size):
        self.server_addr = dest
        self.server_port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(None)
        self.sock.bind(('', random.randint(10000, 40000)))
        self.name = username
        self.window = window_size

    def start(self):
        '''
        Main Loop is here
        Start by sending the server a JOIN message.
        Waits for userinput and then process it
        '''
     
        message = util.make_message("join", 1, self.name)
        packet = util.make_packet(msg = message)
        encodePac = packet.encode("utf-8")
        self.sock.sendto(encodePac, (self.server_addr, self.server_port)) #request to join send.
       
        while True:
            usermsg = input()
            checkFile = usermsg[0] + usermsg[1] + usermsg[2] + usermsg[3] #to check if input is file. 
            to_msg = usermsg[0] + usermsg[1] + usermsg[2]
            if usermsg == "list":
                 message = util.make_message("request_users_list", 2, self.name)
                 packet = util.make_packet(msg = message)
                 encodePac = packet.encode("utf-8")
                 self.sock.sendto(encodePac, (self.server_addr, self.server_port)) #request for list send.
            elif to_msg == "msg": #for client to client communication
                 userMsg = usermsg[4: ]
                 message = util.make_message("send_message", 4, userMsg)
                 packet = util.make_packet(msg = message)
                 encodePac = packet.encode("utf-8")
                 self.sock.sendto(encodePac, (self.server_addr, self.server_port)) 
            elif checkFile == "file":
                userInputSplit = usermsg.split()
                noOfUsers = userInputSplit[1] #no of users to send file to. 
                fileName = userInputSplit[2 + int(noOfUsers): ]
                fileName = ''.join(fileName)
                usersToSendFile = userInputSplit[2: int(noOfUsers) + 2]
                openFile = open(fileName, "r")
                readFile = openFile.read()
                breakFile = readFile.splitlines()
                fileString = "" 
                for i in breakFile: 
                    fileString = fileString + " " + i
                fileUsernames = ""
                for i in usersToSendFile: 
                    fileUsernames = fileUsernames + " " + i
                    
                fileString2 = str(noOfUsers) + fileUsernames+" " + fileName + fileString
                message = util.make_message("send_file", 4, fileString2)
                packet = util.make_packet(msg = message)
                encodePac = packet.encode("utf-8")
                self.sock.sendto(encodePac, (self.server_addr, self.server_port))
                #raise NotImplementedError
            elif usermsg == "help": 
                print("list")
                print("Input: msg <number_of_users> <username1> <username2> ... <message>")
                print("file <number_of_users> <username1> <username2> ... <file_name>")
            elif usermsg == "quit":
                message = util.make_message("disconnect", 1, self.name)
                packet = util.make_packet(msg = message)
                encodePac = packet.encode("utf-8")
                self.sock.sendto(encodePac, (self.server_addr, self.server_port)) #send a message to quit. 
                print("quitting") 
                self.sock.close() 
                sys.exit() 
            else:
                print("Incorrect userinput format")
         
                
   
    def receive_handler(self):
        '''
        Waits for a message from server and process it accordingly
        '''     
        while True: 
            message, address = self.sock.recvfrom(4096) #receive a message
            _, _, parsedMessage, _ =  util.parse_packet (message.decode("utf-8") )
            splitMessage = parsedMessage.split()
            if (splitMessage[0] == "response_users_list"):
                active_users = splitMessage[2: ]
                activeUsersString = ""
                for i in active_users:
                    activeUsersString =  activeUsersString + " " + i 
                activeUsersString = activeUsersString[1:]
                print("list:", activeUsersString) 
            elif (splitMessage[0] == "forward_message"):
                senders_name = splitMessage[3]
                senders_msg = splitMessage[4: ]
                check = False
                finalMsg = ""
                for i in senders_msg: 
                    finalMsg = finalMsg + i + " "
                finalMsg = finalMsg[: -1]
                print("msg:", senders_name+ ":", finalMsg)
                
            elif (parsedMessage[:12] =="forward_file"):
                _, _, forw_file, _ = util.parse_packet(message.decode("utf-8"))
                fileSplit = forw_file.split()
                fileSender = fileSplit[3]
                fileNoOfUser = fileSplit[2]
                filesName = fileSplit[3 + int(fileNoOfUser)]
                filesContentList = fileSplit[4+int(fileNoOfUser): ]
                filesContentString = ""
                for i in filesContentList:
                    filesContentString = filesContentString + " " + i
                fileWrite = open(self.name + " " + filesName, 'w')
                writeOnFile = fileWrite.write(filesContentString)
                fileWrite.close()
                print( "file:", fileSender+ ": "+ filesName)
                
            elif (message.decode("utf-8") == "err_server_full"):
                print("disconnected: server full")
                self.sock.close()
                sys.exit()
            elif (message.decode("utf-8") == "err_username_unavailable"):
                print("disconnected: username not available")
                self.sock.close()
                sys.exit()
            elif (message.decode("utf-8") == "err_unknown_message"):
                print("disconnected: server received an unknown command")
                self.sock.close()
                sys.exit()
                
            
        #raise NotImplementedError
        

# Do not change this part of code
if __name__ == "__main__":
    def helper():
        '''
        This function is just for the sake of our Client module completion
        '''
        print("Client")
        print("-u username | --user=username The username of Client")
        print("-p PORT | --port=PORT The server port, defaults to 15000")
        print("-a ADDRESS | --address=ADDRESS The server ip or hostname, defaults toself.server_addr")
        print("-w WINDOW_SIZE | --window=WINDOW_SIZE The window_size, defaults to 3")
        print("-h | --help Print this help")
    try:
        OPTS, ARGS = getopt.getopt(sys.argv[1:],
                                   "u:p:a:w", ["user=", "port=", "address=","window="])
    except getopt.error:
        helper()
        exit(1)

    PORT = 15000
    DEST = "localhost"
    USER_NAME = None
    WINDOW_SIZE = 3
    for o, a in OPTS:
        if o in ("-u", "--user="):
            USER_NAME = a
        elif o in ("-p", "--port="):
            PORT = int(a)
        elif o in ("-a", "--address="):
            DEST = a
        elif o in ("-w", "--window="):
            WINDOW_SIZE = a

    if USER_NAME is None:
        print("Missing Username.")
        helper()
        exit(1)

    S = Client(USER_NAME, DEST, PORT, WINDOW_SIZE)
    try:
        # Start receiving Messages
        T = Thread(target=S.receive_handler)
        T.daemon = True
        T.start()
        # Start Client
        S.start()
    except (KeyboardInterrupt, SystemExit):
        sys.exit()
