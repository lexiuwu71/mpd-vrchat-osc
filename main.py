from pythonosc.udp_client import SimpleUDPClient
from pythonosc import udp_client
from mpd import MPDClient

from datetime import datetime
import time, sys

global settings
settings = {
    "MPD Address": "localhost",
    "MPD Port": 6600,
    "VRchat OSC Address": "127.0.0.1",
    "VRchat OSC Port": 9000,
}

def get_music(addr, port):
    err = ''

    try:
        client = MPDClient()

        client.connect(addr, port)
        client.update()
        
        status = client.status()
        song = client.currentsong()

        if bool(song):
            if status["state"] == "pause":
                toggle ="⏸️"
            elif status["state"] == "stop":
                toggle = "⏹️"
            else:
                toggle = f"▶️"

            artist = song.get('artist', '')
            title = song.get('title', '')
            album = song.get('album', '')

            duration_seconds = float(status['duration'])
            elapsed_seconds = float(status['elapsed'])
            time_left_unix_time = int(time.time()) + int(duration_seconds - elapsed_seconds)
        else:
            return ('', '', '', "No songs in queue")
            
    except ConnectionError:
        return ('', '', '', "MPD Offline")

    return (title, artist, toggle, err, album, time_left_unix_time, int(duration_seconds - elapsed_seconds))

osc_message = ["", True]

def send_message(msg):
    osc_message[0] = msg
    client.send_message("/chatbox/input",osc_message)
    print(osc_message)

def send_vrchat(address, port, mpd_address, mpd_port):
    global client
    client = SimpleUDPClient(address, port)

    while True:
        output = ''
        music = get_music(mpd_address, mpd_port)

        print(music)

        cur_time = datetime.now().strftime('%H:%M')
        if music[3] != '':
            output = str(cur_time)
        else:
            output = f"{cur_time}\n{music[2]} {music[1]} - {music[0]} - {datetime.utcfromtimestamp(int(music[6])).strftime('%M:%S')} left"

        send_message(output)
        time.sleep(2)

def main():
    try:
        print("Starting VRChat OSC...")
        send_vrchat(settings["VRchat OSC Address"], settings["VRchat OSC Port"], settings["MPD Address"], settings["MPD Port"])
    except KeyboardInterrupt:
        exit()

if __name__ == "__main__":
    main()
