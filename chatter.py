import os
import asyncio
import sys


def getUserInput(upperbnd):
    num = input("Pick an option: ").strip()   
    # Check if the input is an integer
    if num.isdigit():
        num = int(num)
        if num >= 0 and num < upperbnd+1:
            return num
        else:
            return -1
    else:
        return -1

users = ["Alice", "Bob"]
        
async def startAsyncServer(port):
    server = await asyncio.start_server(handle_chat, '127.0.0.1', port)
    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    async with server:
        print(f"{USERNAME} is serving on {addrs}")
        print(f"Users can contact you on port {port}\n")
        await server.serve_forever()


async def handle_chat(reader, writer):
    name = OTHERUSER
    print(f"Starting a convo with {name}")
    print("messaging, type !q to quite")
    try:
        read_task = asyncio.create_task(read_messages(reader))
        await write_messages(writer)
        read_task.cancel()
    finally:
        writer.close()
        await writer.wait_closed()
        print(f"Ending Chat")
        os.system('clear')
        
async def write_messages(writer):
    while True:
        message = await asyncio.to_thread(sys.stdin.readline)
        msg_bytes = message.encode()
        writer.write(msg_bytes)
        await writer.drain()
        if message.strip() == '!q':
            break

async def read_messages(reader):
    while True:
        result_bytes = await reader.readline()
        response = result_bytes.decode()
        if response.strip() == '!q':
            print(f"{OTHERUSER} has left the chat please type !q to leave as well")
            break
        print(f"{OTHERUSER}: {response.strip()}")
        await asyncio.sleep(1)


async def startChat(targetuser):
    user_index = users.index(targetuser) 
    port = 9999-user_index
    try:
        reader, writer = await asyncio.open_connection('127.0.0.1', port)        
        read_task = asyncio.create_task(read_messages(reader))
        await write_messages(writer)
        read_task.cancel()
        print('Ending chat')
        writer.close()
        await writer.wait_closed()
    except ConnectionRefusedError:
        print(f"Could not connect to {targetuser} on port {port}. Server may be down.")
    except asyncio.TimeoutError:
        print(f"Connection to {targetuser} timed out.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    os.system('clear')

async def main():
    os.system('clear')
    while True:
        print("Welcome to chatbot3000! \nLogin as:")
        for i, u in enumerate(users, start=1):
            print(f"{i}. {u}")
        print("0. Exit")  
        
        choice = getUserInput(4)
        if choice == 0:
            quit()
        elif choice < 3 and choice > 0:
            os.system('clear')
            global USERNAME 
            USERNAME = users[choice-1]
            global OTHERUSER
            other_users = [user for user in users if user != USERNAME]
            OTHERUSER = other_users[0]
            port = 9999-choice+1
            server_task = asyncio.create_task(startAsyncServer(port))
            print(f"You are now logged in")
            await asyncio.sleep(1)
            break
        else:
            os.system('clear')
            print("Please provide a valid input \n")
    while True:         
        print(f"Hello {USERNAME}!")
        print(f"\n1 = Send message \n0 = Quit")
        choice = getUserInput(2)
        if choice == 0:
            quit()

        elif choice == 1:
            os.system('clear')
            sendmessagetask = asyncio.create_task(startChat(OTHERUSER))
            await sendmessagetask  

if __name__ == "__main__":
   asyncio.run(main())

