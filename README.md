# VenoxsSearch
This script uses Shodan to search for Minecraft servers that are connected to the public Internet and have been discovered by Shodan. 

The found servers are then scanned directly with the script to get the exact number of current online players, because Shodan's information is usually several days old. The servers are mostly private servers, created by private people and not advertised to the public. However, there are also servers that have been publicly advertised.

It should also be noted that some servers may have a whitelist. From my experience it is about 40% of the found servers.

Results are output in the following format: ```User: <online>/<maximum>   <ip>:<port>  <country>  <city>  <version>```
 

# Setup
1. First create a free account at https://shodan.io/. Then go to https://account.shodan.io/, copy your API key and paste it between the empty quotes after "API_KEY": in config.json. Do not share this API key with anyone!

2. Install **Python 3** and the **pip package manager**, if not already installed.

3. Install the shodan library: ```$ python3 -m pip install shodan```.
Script automatically installs this library after running it, so you don't have to install it yourself. Only if the script doesn't make it

4. Clone this repository: ```$ git clone https://github.com/Venoxs/VenoxsSearch```

5. Edit ```config.json``` according to your preferences. See the Configuration section for more details.

6. Run the script: ```$ python3 venoxssearch.py```

# Configuration
This section documents the settings in ```config.json```. You only need to edit the **API key**, otherwise the choice is yours if you want to change something or not.
- ```API_KEY``` - This must be set. Get your API key from https://account.shodan.io/.

- ```MC_VERSION``` - Search for a specific Minecraft server version. You can leave this field empty, then you will get servers with random versions, but I would recommend you to specify a version.

- ```CURRENTLY_ACTIVE_ONLY``` - If you set this to ```true```, then only servers where people are currently online will be output. By default it is set to ```false```

- ```ONLINE_USER_SEARCH``` - When you search for Minecraft servers with Shodan, you get the following information of each server: **"Online Players: x"**. You can specify the ```x``` here and thus only search for servers that were ```x``` number of players online at the time of Shodan's scan. If you want to search for servers where people are currently online, then I recommend you put a number between ```2-5``` here. If you want it to be random, then put ```-1```.

- ```OUTPUT_FILE``` - If you set that to a filename, then the script will save the results to the file you specified. If you don't want to save it, then just leave it empty.
