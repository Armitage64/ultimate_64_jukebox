# ultimate_64_jukebox
### Proof-of-concept Python SID jukebox using the Ultimate64 / 1541UII+ REST API

- Uses SID files from the High Voltage SID Collection (HVSC)
- Requires Ultimate Firmware 3.11 or higher
- Uploads SID files directly to C64 and starts playing them in random order with a countdown timer

### To Use
- Download and unzip HVSC
- Create a playlist.txt file containing the full path of the SIDs you want to play
- Edit the configuration in the script
- Have fun!

### Resources
- HVSC - https://www.hvsc.c64.org/
- Ultimate64 - https://ultimate64.com
- Retro Bits on YouTube - https://youtube.com/retrobitstv

### TODO
- Stop playback immediately when timer expires, then load next track
- Re-randomize playlist and start again when reaching the end
- Catch SIGINT and stop playback before exiting
- Implement a key to skip to the next track
- Error checking when loading playlist, retriving HVSC data, etc.
