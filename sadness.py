from pythonosc import udp_client
import time


to_send = [
    [[2500, 3000, 2500, 1000], 500],
    [[2200, 4000, 2500, 1000], 4000],
    [[2400, 3500, 2500, 1000], 4000],
]


positionx_min = 1800  # Minimum allowed positionx value
positionx_max = 3200  # Maximum allowed positionx value
positiony_min = 2200  # Minimum allowed positiony value
positiony_max = 2900  # Maximum allowed positiony valueˀ

# Set up the OSC client
ip = "192.168.50.112"  # IP address of the OSC server
port = 9321       # Port of the OSC server
client = udp_client.SimpleUDPClient(ip, port)

def check_position_bounds(positionx, positiony):
    if not (positionx_min <= positionx <= positionx_max):
        print(f"Error: positionx {positionx} is out of bounds!")
        return False
    if not (positiony_min <= positiony <= positiony_max):
        print(f"Error: positiony {positiony} is out of bounds!")
        return False
    return True

def send_data(data):
    positionx, timex, positiony, timey = data[0]
    if not check_position_bounds(positionx, positiony):
        print("Skipping sending due to out-of-bound positions.")
        return
    print('sending ', data[0])
    client.send_message("/bigbee", ['head', positionx, timex, positiony, timey])

    # Wait for the time specified
    wait_time = data[1]
    time.sleep(wait_time / 1000.0)  # Convert milliseconds to seconds

# Send the data
for data in to_send:
    send_data(data)
