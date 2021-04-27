# Networking
 Contains code for a simple chat application implemented using UDP.
 This allows for client to client messaging and file sharing.

To run the server of chat application, execute following command: 
 
 
$ python3 server.py -p <port_num>

Execute following command to run a client: 
 
 $ python3 client.py -p <server_port_num> -u <username>

List of functionalities: 

Request list of users: list

Send message to another client:



msg <number_of_users> <username1> <username2> ... <message>
 
 
Send file to another client: 



file <number of users> <username1> <username2> ... <filename>
 
 
Prints all the possible user-inputs and their format Input: 

help

Disconnect: 
 
quit

 
