import socket
import threading

# Connection set up
host = '137.113.201.8' #Can use local IP '127.0.0.1' to test.  #Using local IP address to test but CHANGE when configure with Raspberry Pi.
port = 55555 #Avoid using common port numbers.

# Starting server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen() #server is listening

# Lists for clients and their nicknames/usernames
clients = []
nicknames = []

# Sending messages to All connected clients/users
def broadcast(message):
    for client in clients:
        client.send(message)

# Handling messages from clients
def handle(client):
    while True:
        try:
            msg = message = client.recv(1024)
            if msg.decode('ascii').startswith('KICK'): #Condut /kick command (only usable for admin)
                if nicknames[clients.index(client)] == 'admin':
                    name_to_kick = msg.decode('ascii')[5:]
                    kick_user(name_to_kick)
                else:
                    client.send('Command was refused!'.encode('ascii'))
            elif msg.decode('ascii').startswith('BAN'): #Condut /ban command (only usable for admin)
                if nicknames[clients.index(client)] == 'admin':
                    name_to_ban = msg.decode('ascii')[4:]
                    kick_user(name_to_ban)
                    with open('bans.txt', 'a') as f: #For ban record
                        f.write(f'{name_to_ban}\n')
                    print(f'{name_to_ban} was banned!')
                else:
                    client.send('Command was refused!'.encode('ascii'))
            else:
                broadcast(message)
        except:
            if client in clients:
                # Removing and closing clients
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                broadcast('{} left!'.format(nickname).encode('ascii'))
                nicknames.remove(nickname)
                client_count()
                break

# Receiving / listening function
def receive():
    while True:
        # Accept connection
        client, address = server.accept() #Keep accepting users. Enter number in () to constraint the maximum users
        print("Connected with {}".format(str(address))) #Notify client that he/she/they is connected

        # Request and store nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')

        # Check if user is in the ban list
        with open('bans.txt', 'r') as f:
            bans = f.readlines()

        #Refuse connection if user is in the ban list
        if nickname+'\n' in bans:
            client.send('BAN'.encode('ascii'))
            client.close()
            continue

        #Check if user is admin
        if nickname == 'admin':
            client.send('PASS'.encode('ascii'))
            password = client.recv(1024).decode('ascii')
            #Cehck id user enter correct password to get admin role
            if password != 'FunRoboticsClassVMI!':
                client.send('REFUSE'.encode('ascii'))
                client.close()
                continue

        nicknames.append(nickname)
        clients.append(client)

        # Print and broadcast nickname that user/client entered, except for admin
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        client_count()

        # Start handling thread for client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

# Kick user function
def kick_user(name):
    if name in nicknames:
        name_index = nicknames.index(name)
        client_to_kick = clients[name_index]
        clients.remove(client_to_kick)
        client_to_kick.send('You were kicked by an admin!'.encode('ascii'))
        client_to_kick.close()
        nicknames.remove(name)
        broadcast(f'{name} was kicked by an admin!'.encode('ascii'))

# Count total users/clients online
def client_count():
    client_count_msg = f"Online Users: {len(clients)}"
    broadcast(client_count_msg.encode('ascii'))

print("Welcome! Server is listening...")
receive()