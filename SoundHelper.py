# Sound helper file

#  requirements: pip install pydub
# for converting the audio to MP3 you need to download and unpack ffmpeg:
# http://www.ffmpeg.org/
# copy the ffmpeg + ffprobe + ffplay to python folder
# to playback need to install playsound ver 1.2.2
# pip install playsound==1.2.2

import wave
import numpy as np
from pydub import AudioSegment


class RecHelper:

    def save_to_file(recording,dtype:str,sample_rate:int,FileName:str):
        """
        Save file in WAV format\n
        - recording : audio data\n
        - dtype : usualy int16\n
        - sample_rate : usualy 44100\n
        - FileName : WAV file name
        """
        with wave.open(FileName, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(np.dtype(dtype).itemsize)
            wf.setframerate(sample_rate)
            wf.writeframes(recording.tobytes())
        print(f"Saved to {FileName}")

    def normalize_audio(data,dtype:str):
        """
        Function to normalize the audio data\n
        - data : recording data\n
        - dtype : usualy int16
        """
        # Find the maximum absolute value in the data
        max_val = np.max(np.abs(data))
        # Avoid division by zero
        if max_val == 0:
            return data
        # Normalize the data to be within the range of int16
        return (data / max_val * (np.iinfo(dtype).max - 1)).astype(dtype)

class PlayHelper:

    def ConvertToMP3(input:str,output:str):
        """
        Convert WAV file to MP3\n
        - input : input file and path in WAV format\n
        - output : output file in MP3 format
        """
        sound = AudioSegment.from_wav(input)
        print('converting to MP3')
        sound.export(output, format='mp3')

    def PlayMP3ToSpeakers(input:str):
        """
        For Raspbbery pi\n
        Playing MP3 to speakers thru 3.5 mm jack\n
        - input : the input file in MP3 format
        """
        from pydub.playback import play
        print('Playing to speakers')
        song = AudioSegment.from_mp3(input)
        play(song)

    def PlayWAVToUSB(file_name:str, device:int):
        """
        For Raspbbery pi\n
        Playing WAV to USB device\n
        - input : the input file in WAV format\n
        - device : device id
        """
        import soundfile as sf
        import sounddevice as sd
        print('Playing to USB device')
        data, fs = sf.read(file_name, dtype='float32')
        if len(data.shape) > 1:
            data = np.mean(data, axis=1)
        sd.play(data, samplerate=fs, device=device)
        sd.wait()  # Wait until the file is done playing

class FileHelper:

    def ConvertToWAV(input:str,sampleRate:int,output:str):
        """
        Convert MP3 file to WAV\n
        - input : input file and path in MP3 format\n
        - sampleRate : output sample rate\n
        - output : output file in WAV format 
        """
        print('Converting to WAV')
        audio_segment = AudioSegment.from_mp3(input)
        resampled = audio_segment.set_frame_rate(sampleRate)
        resampled.export(output, format='wav')

    def AssembleWAV(input:list,outfile:str):
        """
        Assemble list of WAV files into one single file\n
        - input : list of files to assemble.\n
        - outfile : file name for output.
        """
        data= []
        for infile in input:
            w = wave.open(infile, 'rb')
            data.append( [w.getparams(), w.readframes(w.getnframes())] )
            w.close()
            
        output = wave.open(outfile, 'wb')
        output.setparams(data[0][0])
        for i in range(len(data)):
            output.writeframes(data[i][1])
        output.close()
        print('filished')
