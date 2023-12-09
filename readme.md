# TELEGRAPH project

## Wikipedia [link](https://en.wikipedia.org/wiki/History_of_the_telephone)

## About
Lets have a chat with ChatGPT4,

BUT for **REAL**,

Lets have a call.

We are best friends. 

This script is using OpenAI STT, chat and TTS models, to have a real feeling chat.

## Equipment:
- Raspberry pi 3 B
- USB headset (microsoft LiveChat)
- Switch
- 5 mm LED
- 2 X 220 kOhm resistors
- Old wireless telephone.

## The process (Connecting the hardware):
![telephone](https://github.com/sdebby/telegraph/blob/main/Media/panasonic_dect_brezzicni_telefon_kx_tg1611fxh_PKKX-TG1611FXH.jpeg?raw=true)
1. Taking apart an old DECT telephone.
   
![telephone open 1](https://github.com/sdebby/telegraph/blob/main/Media/IMG_7527.jpg?raw=true)

![telephone open 2](https://github.com/sdebby/telegraph/blob/main/Media/IMG_7525.jpg?raw=true)

2. Disconnecting speaker

![Speaker](https://github.com/sdebby/telegraph/blob/main/Media/IMG_7528.jpg?raw=true)

3. Soldering LED + resistors + switch to cable.

![LED](https://github.com/sdebby/telegraph/blob/main/Media/IMG_7529.jpg?raw=true)

![Switch](https://github.com/sdebby/telegraph/blob/main/Media/IMG_7532.jpg?raw=true)

4. Disassemble USB headset:

![Headset](https://github.com/sdebby/telegraph/blob/main/Media/IMG_7534.jpg?raw=true)

5. Testing cable on raspberry pi.

![LED](https://github.com/sdebby/telegraph/blob/main/Media/IMG_7535.jpg?raw=true)

6. Soldering USB speaker and microphone wires to telephone, adhering the button to back cover with hot glue and adhering the LED to front cover with hot glue.
   
![The connection](https://github.com/sdebby/telegraph/blob/main/Media/IMG_7536.jpg?raw=true)

7. Closing all together.

![all together 1](https://github.com/sdebby/telegraph/blob/main/Media/IMG_7541.jpg?raw=true)

![all together 2](https://github.com/sdebby/telegraph/blob/main/Media/IMG_7542.jpg?raw=true)

![all together 3](https://github.com/sdebby/telegraph/blob/main/Media/IMG_7543.jpg?raw=true)

### Schematics
![schematics](https://github.com/sdebby/telegraph/blob/main/Media/schematic_bb.jpg?raw=true)

## Behind the scenes:
1. If there where old message files, they will be deleted from the folder.
2. A pre recorded welcome message will play to the user.
3. User press the button and record a new message.
4. When releasing the button, the message converted to MP3 and sent to OpenAI Whisperer module - Speech To Text (STT).
5. The replied transcript then sent to OpenAI ChatGPT 4 module.
6. The replied generated text then sent to OpenAI Text To Speech module (TTS).
7. The replied MP3 then converted to WAV and played back to the user.

## Demo video

[![](https://markdown-videos-api.jorgenkh.no/youtube/m34_VWeIYn8)](https://youtu.be/m34_VWeIYn8)

## Install:
Install ffmpeg on machine:

https://ffmpeg.org/

```bash
git clone sdebby/telegraph
pip install -r requirements.txt
python ChatWithLinux1.py -d [x]
```
Obtain Open AI API key and save in in environment as "OpenAI_Key" (or replace the key in file OpenAIHelper.py)

### Usage
parameters:

-h help 

-l list of USB devices

-d [x] use USB device no. x

- If using a Raspberry pi (like in this project) and need to adjust volume:
```bash
alsamixer
- Adjust USB device volume and exit
- Save configuration: 
sudo alsactl store
```

### Limitations:
- Due to the ping-pong method (sending voice,receiving text, sending text, ect ...) there is a long delay from when talking to receiving answer.