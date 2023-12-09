#  28.11.2023
#  telegraph project
# https://en.wikipedia.org/wiki/History_of_the_telephone

import glob
import os, argparse, sys
import threading
from gpiozero import Button, LED
import sounddevice as sd
import soundfile as sf
import numpy as np
import queue
import time
import SoundHelper as SH
from OpenAIHelper import OpenAIHelper as AIH

# Chat parameters
max_tok=750
temp=0.7
ChatModel="gpt-4-1106-preview"
msglist=[]
ChatRole='Act as a friend, handle deep conversations, reply only by simple text'
AIvoice = ['alloy','echo','fable','onyx','nova','shimmer']
SelectAIvoice = AIvoice[4]

# Recording parameters
sample_rate = 48000
Channels=1
dtype = 'int16'
audio_queue = queue.Queue() # Define a queue to communicate between the recording thread and main thread
dev_index = 1
BlockSize=1024
led = LED(18)
button = Button(23,hold_time=1)
RFlag = False

def SetArgs():
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-l", "--list", help="List USB devices", action='store_true', required=False)
    argParser.add_argument("-d", "--device" , type=int, help="Selected USB device", required=False)
    return argParser.parse_args()

def ListUSBSpeakers():# List all available devices
    print("Available audio devices:")
    devices = sd.query_devices()
    for idx, device in enumerate(devices):
        print(idx, device['name'])
    print('-'*10)

def ButtonThreading():
	button.when_pressed = record_audio
	button.when_released = on_button_released

def on_button_released():
    print('released')

def CleanFiles(FileSet:str): # Delete all files in a folder
    print('deleting files ',FileSet)
    files = glob.glob(FileSet, recursive=True)
    for f in files:
        try:
            os.remove(f)
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))

# Function to record audio
def record_audio():
    audio_data = np.array([], dtype=dtype)
    def callback(indata, frames, time, status):
        global RFlag
        if status:
            print(status)
        # Put the incoming data into the queue
        if RFlag:
            audio_queue.put(indata.copy())
                
    # Start the stream
    with sd.InputStream(samplerate=sample_rate, blocksize=BlockSize, channels=Channels, device=dev_index, callback=callback):
        global RFlag
        while True:
            button.wait_for_press()
            led.on()
            RFlag = True
            print("Recording...")
            while True:
                audio_data = np.append(audio_data, audio_queue.get())
                if not button.is_pressed:  
                    time.sleep(1)
                    RFlag = False
                    break

            led.off()
            print("Recording stopped.")        
            audio_data =SH.RecHelper. normalize_audio(audio_data, dtype) # Normalize the recording
            filenameWAV = f"recording_{int(time.time())}.wav"
            SH.RecHelper.save_to_file(audio_data, dtype, sample_rate,filenameWAV) # Save the recording to a file
            audio_data = np.array([], dtype=dtype)
             
            filenameMP3=filenameWAV.split('.')[0]+'.mp3' # convert to MP3
            SH.PlayHelper.ConvertToMP3(filenameWAV,filenameMP3)
            
            UserTranslation=AIH.STT(filenameMP3).text # transcript to text
            
            msg1={"role": "user", "content": UserTranslation}
            msglist.append(msg1) # adding user message to list

            ChatResponce=AIH.Chat(ChatModel,temp,max_tok,msglist) #sending messages to chat
            msg2={"role": "assistant", "content": ChatResponce}
            msglist.append(msg2)

            filenameMP3Response=filenameWAV.split('.')[0]+'+response.mp3'
            AIH.TTS(ChatResponce,filenameMP3Response,SelectAIvoice) # convert text to speach

            filenameWAVResponse=filenameMP3Response.split('.')[0]+'+ConvWAV.wav'
            SH.FileHelper.ConvertToWAV(filenameMP3Response,sample_rate,filenameWAVResponse)
            SH.PlayHelper.PlayWAVToUSB(filenameWAVResponse,dev_index) #play to USB device

def main():    
    global dev_index
    UserArgs=SetArgs()
    if UserArgs.list:
        ListUSBSpeakers()
        sys.exit()
    elif UserArgs.device is None:
        print('Device ID cannot be none')
        sys.exit()
    dev_index = UserArgs.device
        # clearing previus conversations
    CleanFiles('*.wav')
    CleanFiles('*.mp3')
    print('-- STARTING --')
    led.blink(on_time=0.5,off_time=0.5,n=3) #blink LED 3 time for start
    time.sleep(1)
    # Play welcome massage
    WelcomeMessage='welcome/'+SelectAIvoice+'-welcome.wav'
    SH.PlayHelper.PlayWAVToUSB(WelcomeMessage,dev_index) #play to USB device
    led.off()
    msglist.append({"role": "system", "content": ChatRole})
    # Run the record_audio function in a separate thread
    recording_thread = threading.Thread(target=record_audio)
    recording_thread.start()

if __name__ == "__main__":
    main()