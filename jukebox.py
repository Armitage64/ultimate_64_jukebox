#!/usr/bin/python3.8

# jukebox.py - Upload and play HVSC SID files on Ultimate64 / UII+
# Matthew R. Demicco - 1/20/2024
# https://youtube.com/retrobitstv
#
# Note: this is just a proof of concept, there's minimal error checking!

import requests, random, hashlib, pathlib, re, os, time, sys, signal, argparse

# Configuration Starts Here

# IP address of your Ultimate64 or UII+
ultimateIP = '192.168.1.234'

# Local path where you have unzipped High Voltage SID Collection
# Download - https://www.hvsc.c64.org/
HVSCPath = '/home/armitage/retrobits/C64Music'

# HVSC songs to play, one file (full path) per line
# e.g. /home/armitage/retrobits/C64Music/MUSICIANS/J/Jammer/Gliding_Gladly_2SID.sid
playlist = '/home/armitage/retrobits/playlist.txt'

# End of Configuration

apiSidplay = 'http://' + ultimateIP + '/v1/runners:sidplay'
apiReset = 'http://' + ultimateIP + '/v1/machine:reset'
clearLine = '\x1b[2K'
sigInt = False

# Reset C64
def resetMachine():
    try:
        req = requests.put(apiReset)
        return True

    except requests.exceptions.RequestException as e:
        print("Failure talking to Ultimate device: " + str(e))
        return False

# Handle SIGINT (ctrl-c)
def sigintHandler(signalNumber,frame):
    global sigInt
    sigInt = True

signal.signal(signal.SIGINT,sigintHandler)

# Parse arguments
parser = argparse.ArgumentParser(
        prog='jukebox',
        description='SID jukebox for C64 Ultimate REST API',
        epilog='Blame: Matthew R. Demicco')
parser.add_argument('-p', '--playlist', help='Override default playlist.tx', action='store')
args = parser.parse_args()

# Are we using a custom playlist?
if args.playlist:
    playlist = args.playlist

# Load and randomize the playlist
sidFiles = open(playlist).read().splitlines()
random.shuffle(sidFiles)

# Iterate through the random playlist
for sidFile in sidFiles:

    # Calculate MD5 hash of the next file to play
    md5 = hashlib.md5(pathlib.Path(sidFile).read_bytes()).hexdigest()

    # Locate the MD5 hash in the HVSC Songlengths file
    with open(HVSCPath + '/DOCUMENTS/Songlengths.md5', 'r') as songLengths:
        for line in songLengths.readlines():
            if md5 in line:
                songLength = line

    # Extract time from the line we found (discard microseconds)
    runTime = re.search('.*=(\d+):(\d+).*', songLength)
    seconds = int(runTime.group(1)) * 60 + int(runTime.group(2))

    # Inform the user
    filePath = os.path.split(sidFile)
    print('\nPlaying ' + filePath[1] + ' (' + runTime.group(1) + ':' + runTime.group(2) + ')')

    # Make the REST API call to upload and play the next SID
    postReq = {"file": open(sidFile, 'rb')}
    try:
        req = requests.post(apiSidplay, files=postReq)
        if(not(req.status_code >= 200 and req.status_code < 300)):
             print("REST API Error: " + str(req.status_code))
             continue

    except requests.exceptions.RequestException as e:
        print("Failure talking to Ultimate device: " + str(e))
        continue

    # Count Down
    for timeLeft in range(seconds, 0, -1):
        sys.stdout.write('\r{:2d} seconds remaining.'.format(timeLeft))
        sys.stdout.flush()

        # Have we received a ctrl-c?
        if (sigInt):
            print(end=clearLine)
            print('\rInterrupt Received, Skipping... (ctrl-c again to quit.)')
            sigInt = False

            # Sleep for 2 seconds to allow user to exit gracefully
            time.sleep(2)
            if (sigInt):
                # Reset C64 and exit
                print('\rOkay, bye!!!')
                resetMachine()
                sys.exit()
            else:
                # Skip to the next song
                break

        else:
            # Sleep and continue the countdown
            time.sleep(1)

    # Done with song
    print(end=clearLine)
    print('\rDone!')

    # Reset the machine to stop playback
    resetMachine()

    # End of loop, move on to the next file

# Done with all files
print("\nNo more files to play, calling it a day!")
