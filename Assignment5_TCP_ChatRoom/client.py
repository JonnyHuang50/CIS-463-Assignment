import socket
import threading

# Ask user to choose a nickname
nickname = input("Please enter your nickname: ")
# Ask user to enter password if choose to login as admin. Password is "FunRoboticsClassVMI!"
if nickname == 'admin':
    password = input("Enter password for admin: ")

# Connecting to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('137.113.201.8', 55555)) #Using local IP address '127.0.0.1' to test but CHANGE when configure with Raspberry Pi. Avoid using common port numbers.

stop_thread = False

# Listening to server and sending nickname
def receive():
    while True:
        global stop_thread
        if stop_thread:
            break
        try:
            # Receive message from server
            # If 'NICK' send nickname
            # Check password
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
                next_message = client.recv(1024).decode('ascii')
                if next_message == 'PASS':
                    client.send(password.encode('ascii'))
                    if client.recv(1024).decode('ascii') == 'REFUSE':
                        print("Connection was refused! Wrong password!")
                        client.close()
                        stop_thread = True
                elif next_message == 'BAN':
                    print('Connection refused because of ban!')
                    client.close()
                    stop_thread = True
            else:
                print(message)
        except:
            # Close connection when error
            print("An error occured!")
            client.close()
            break

# Send messages to server
def write():
    while True:
        if stop_thread:
            break
        message = f'{nickname}: {input("")}'
        if message[len(nickname)+2:].startswith('/'): #Make sure commands can only executed by admin role, not general users
            if nickname == 'admin':
                if message[len(nickname)+2:].startswith('/kick'):
                    client.send(f'KICK {message[len(nickname)+2+6:]}'.encode('ascii'))
                elif message[len(nickname)+2:].startswith('/ban'):
                    client.send(f'BAN {message[len(nickname)+2+5:]}'.encode('ascii'))
            else:
                print("Commands can only be executed by the admin!")
        else:
            #message = '{}: {}'.format(nickname, input(''))
            client.send(message.encode('ascii'))

# Start threads for listening and writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
