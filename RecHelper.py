# Recording file helper

import wave
import time
import numpy as np


class Helper:

    def save_to_file(recording,dtype,sample_rate):
        """
        Save file in WAV format
        """
        filename = f"recording_{int(time.time())}.wav"
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(1)
            # wf.setsampwidth(2)
            wf.setsampwidth(np.dtype(dtype).itemsize)
            wf.setframerate(sample_rate)
            wf.writeframes(recording.tobytes())
        print(f"Saved to {filename}")

    def normalize_audio(data,dtype):
        """
        Function to normalize the audio data
        """
        # Find the maximum absolute value in the data
        max_val = np.max(np.abs(data))
        # Avoid division by zero
        if max_val == 0:
            return data
        # Normalize the data to be within the range of int16
        return (data / max_val * (np.iinfo(dtype).max - 1)).astype(dtype)