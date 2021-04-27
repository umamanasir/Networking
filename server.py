'''
This module defines the behaviour of server in your Chat Application
'''
import sys
import getopt
import socket
import util 


class Server:
    '''
    This is the main Server Class. You will to write Server code inside this class.
    '''
    def __init__(self, dest, port, window):
        self.server_addr = dest
        self.server_port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(None)
        self.sock.bind((self.server_addr, self.server_port))
        self.window = window

    def start(self):
        '''
        Main loop.
        continue receiving messages from Clients and processing it
        '''
        usernm_available = True
        clientInfo = {} #empty dict to store client username and address
        
        while True:
         message, address = self.sock.recvfrom(2048) #receive a message
         message = message.decode("utf-8")
         _,_, msg,_ = util.parse_packet(message)
         msgg = msg.split() 
         client_num = len(clientInfo)
         if msg[:4] == "join":
            username = msgg[2]
            for key in clientInfo: #check if it is available
               if key == username:
                  usernm_available = False
              
            if client_num > 10: # max number of clients reached
               self.sock.sendto(("err_server_full").encode("utf-8"), address)
               print("disconnected. server full.")
               break
            elif usernm_available == False: # check username availability.
               self.sock.sendto(("err_username_unavailable").encode("utf-8"), address)
               print("disconnected. username not available.")
            else:
               clientInfo.update({username: address})  #add data to dictionary
               print("join:", username)
               
         elif msg[:18] == "request_users_list":
            users_list = ""
            list_user = ""
            activeUsersList = []
            for key, values in clientInfo.items():
                if address == values:
                   list_user = key #name of user who requested list.
                   break
            print("request_users_list:", list_user)
            for key,values in clientInfo.items(): 
                activeUsersList.append(key)
            activeUsersList.sort()
            for i in activeUsersList:
                users_list = users_list + i + " " #name of all active users
           
            message = util.make_message("response_users_list", 3, users_list)
            packet = util.make_packet(msg = message)
            encodePac = packet.encode("utf-8")
            self.sock.sendto(encodePac, address) #request for list send.
         elif msg[:12] == "send_message":
             msg_content = msgg
             senders_address = address
             sender_name = ""
             for key,value in clientInfo.items():
                 if senders_address == value:
                     sender_name = key  #find username of sender
                     break
             noOfUsers = int(msgg[2]) #no of users to send msg to.
             
             usersToMessage = msg_content[3: noOfUsers+3]  #usernames to forward text to.
             message_forward = msg_content[noOfUsers + 3:]  #message to forward to users
             noOfValidUsers = 0
             message_user = ""
             check = False
             for i in message_forward:
                 if not check:
                     check = True
                     message_user = message_user +" "+ i
                 else:
                     message_user = message_user + " "  + i 
             print("msg:", sender_name)
             messageToSend = str(noOfUsers) + " "+ sender_name + message_user  #correct formatting of message
             message = util.make_message("forward_message", 4, messageToSend)
             packet = util.make_packet(msg = message)
             encodePac = packet.encode("utf-8")
             nonexistantUser = True
             for i in range(noOfUsers):    
               for key, values in clientInfo.items():
                 if usersToMessage[i] == key: #finding address of users to forward the message to
                     self.sock.sendto(encodePac, values) #send the message when you find the address.
                     noOfValidUsers += 1 #checking for any invalid username.
                     nonexistantUser = False
               if nonexistantUser == True:
                 print("msg:", sender_name, "to non-existent user", usersToMessage[i])
            
                
         elif msg[:9] == "send_file":
           UsersFileNo = msgg[2] #no of users to forward file to. 
           usersFileForward = msgg [3: 3 + int(UsersFileNo)] #users to forward file to. 
           sender = ""
           for key, value in clientInfo.items(): 
               if value == address: 
                    sender = key #for sender name of file. 
                    break
           fileNam = msgg[3 + int(UsersFileNo): 4 + int(UsersFileNo)]
           fileContents = msgg[4 + int(UsersFileNo): ]  
           fileMess = ""
           for i in fileContents:
               fileMess = fileMess + " " + i 
           nameOfFile = "" 
           for i in fileNam: 
                nameOfFile = nameOfFile + " " + i
           fileToSend = "1 "  + sender + nameOfFile + fileMess
           message = util.make_message("forward_file", 4, fileToSend)
           packet = util.make_packet(msg = message)
           encodePac = packet.encode("utf-8")
           for i in usersFileForward:
                for key, values in clientInfo.items(): 
                     if key == i: 
                        print("file: " + sender)
                        self.sock.sendto(encodePac, values)
         elif msg[:10] == "disconnect":
             for key, values in clientInfo.items():
                    if address == values:
                        print("disconnected:", key)
                        del clientInfo[key]
                        break
         else: 
             for key, values in clientInfo:
                 if value == address: 
                     sender = key
             print("disconnected", sender, "send unknown command")
             message = util.make_message("err_unknown_message", 2)
             packet = util.make_packet(msg = message)
             encodePac = packet.encode("utf-8")
             elf.sock.sendto(encodePac, address)
             for key, values in clientInfo():
                 if value == address: 
                     sender = key
                     del clientInfo[key]
                     break
      #  raise NotImplementedError
     

# Do not change this part of code
if __name__ == "__main__":
    def helper():
        '''
        This function is just for the sake of our module completion
        '''
        print("Server")
        print("-p PORT | --port=PORT The server port, defaults to 15000")
        print("-a ADDRESS | --address=ADDRESS The server ip or hostname, defaults to localhost")
        print("-w WINDOW | --window=WINDOW The window size, default is 3")
        print("-h | --help Print this help")

    try:
        OPTS, ARGS = getopt.getopt(sys.argv[1:],
                                   "p:a:w", ["port=", "address=","window="])
    except getopt.GetoptError:
        helper()
        exit()

    PORT = 15000
    DEST = "localhost"
    WINDOW = 3

    for o, a in OPTS:
        if o in ("-p", "--port="):
            PORT = int(a)
        elif o in ("-a", "--address="):
            DEST = a
        elif o in ("-w", "--window="):
            WINDOW = a

    SERVER = Server(DEST, PORT,WINDOW)
    try:
        SERVER.start()
    except (KeyboardInterrupt, SystemExit):
        exit()
