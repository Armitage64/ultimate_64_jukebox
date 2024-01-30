# ultimate_64_jukebox
### Proof-of-concept Python SID jukebox using the Ultimate64 / 1541UII+ REST API

- Uses SID files from the High Voltage SID Collection (HVSC)
- Requires Ultimate Firmware 3.11 or higher
- Uploads SID files directly to C64 and starts playing them in random order with a countdown timer

### To Use
- Download and unzip HVSC
- Create a playlist.txt file containing the full path of the SIDs you want to play
- Edit the configuration at the top of the jukebox.py script
- Install requests module with `python3.8 -m pip install requests`
- CTRL-C will skip to next song and optionally quit the player
- Have fun!

### Resources
- HVSC - https://www.hvsc.c64.org/
- Ultimate64 - https://ultimate64.com
- Retro Bits on YouTube - https://youtube.com/retrobitstv

### TODO
- ~~Stop playback immediately when timer expires, then load next track~~
- ~~Catch SIGINT and stop playback before exiting~~
- ~~Implement a key to skip to the next track~~
- Re-randomize playlist and start again when reaching the end
- Error checking when loading playlist, retriving HVSC data, etc.
- If a .sid file isn't found in Songlengths.md5, display a warning and default to a sane (e.g. 300 sec) value
- Implement a -r switch to enable randomization (default: off)
- Implement a -p switch to specify a playlist file (default: playlist.txt)
- Provide a way to use the entire HVSC archive as a playlist 
