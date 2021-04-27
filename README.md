# Networking
Contains code for a simple chat application implemented using UDP.
This allows for client to client messaging and file sharing.

To run the server of chat application, execute following command: 
$ python3 server.py -p <port_num>

Execute following command to run a client:
$ python3 client.py -p <server_port_num> -u <username>
 
List of functionalities: 

Request list of users:
request_users_list: <username>
  
Send message to another client:
msg: <sender username>: <message>
  
Send file to another client:
file: <sender username>: <filename>
  
Disconnect:
disconnect

