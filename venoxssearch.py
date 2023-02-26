import json
import socket
import os
import threading

# Installing requirements automatically
try:
    from shodan import Shodan
except ImportError:
    os.system("python -m pip install shodan")
    from shodan import Shodan

# config.json
CONFIG = {}

query = "Minecraft "
scan_data = []


def request_shodan():
    IP_List = []  # (ip, port, country, city, version) for each tuple
    api = Shodan(CONFIG["API_KEY"])
    try:
        result = api.search(query=f'{query}')
    except Exception as e:
        print(e)
        exit()
    for i in result['matches']:
        IP_List.append((i['ip_str'], i['port'], i['location']['country_name'], i['location']['city'], i['version']))
    if len(IP_List) == 0:
        print(
            "\nCouldn't find anything using your entered Minecraft version.\nMaybe you wrote it incorrectly in config.json!")
        exit()
    return IP_List


def scan_ip(IP, index):
    # Connect to the server and get data
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)  # 5 seconds timeout
    try:
        s.connect((IP[0], IP[1]))
        s.send(b'\xFE\x01')  # Send handshake packet
        data = s.recv(1024)  # Receive answer
        s.close()
        # Analyze and output data
        if data and data.startswith(b'\xFF\x00'):  # Successful answer
            motd = data[3:].decode('utf-16be')  # Message of the Day
            motd = motd.split('\x00')
            user_data = (index, motd[-2], motd[-1])  # (index, online, max)
            scan_data.append(user_data)
    except Exception:
        pass


if __name__ == "__main__":
    print("VenoxsSearch 2023 - Minecraft Server Finder")

    # Load config.json
    try:
        with open("config.json") as f:
            CONFIG = json.loads(f.read())
    except Exception as e:
        print(f"\nFailed to load config.json!\n{e}")
        exit()

    # See if API_KEY is present
    if CONFIG["API_KEY"] == "":
        print("API_KEY must be set!")
        exit()

    # Adding Minecraft Version to query
    if CONFIG["MC_VERSION"] != "":
        query += f"{CONFIG['MC_VERSION']} "

    # Adding Online User Search to query
    if CONFIG["ONLINE_USER_SEARCH"] >= 0:
        query += f"Online Players: {CONFIG['ONLINE_USER_SEARCH']} "

    print("\nSearching for servers...")
    IP_List = request_shodan()

    print("Scanning IP's...")

    # Creating all threads
    threads = []
    for index, IP in enumerate(IP_List):
        thread = threading.Thread(target=scan_ip, args=(IP, index))
        threads.append(thread)

    # Start all threads
    for thread in threads:
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print(" ")

    # Outputting the data and creating final_data
    final_data = []
    for i in scan_data:
        data = f"User: {i[1]}/{i[2]} | {IP_List[i[0]][0]}:{IP_List[i[0]][1]} | {IP_List[i[0]][2]} | {IP_List[i[0]][3]} | {IP_List[i[0]][4]}"
        try:
            if CONFIG["CURRENTLY_ACTIVE_ONLY"] == True:
                if int(i[1]) > 0:
                    final_data.append(data)
                    columns = data.split(" | ")
                    formatted_data = ""
                    for col in columns:
                        formatted_data += col.ljust(26)
                    print(formatted_data)
            else:
                final_data.append(data)
                columns = data.split(" | ")
                formatted_data = ""
                for col in columns:
                    formatted_data += col.ljust(26)
                print(formatted_data)
        except Exception as e:
            print(e)
            exit()


    # Writes to OUTPUT_FILE if specified in config.json
    if CONFIG["OUTPUT_FILE"] != "":
        try:
            with open(CONFIG["OUTPUT_FILE"], "w", encoding="utf-8") as f:
                for data in final_data:
                    columns = data.split(" | ")
                    formatted_data = ""
                    for col in columns:
                        formatted_data += col.ljust(23)
                    f.write(formatted_data + "\n")
        except Exception as e:
            print(f"Failed to open OUTPUT_FILE!\n{e}")
            exit()
