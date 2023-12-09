import os
from openai import OpenAI
client = OpenAI(api_key=os.environ['OpenAI_Key'])

class OpenAIHelper:

    def TTS(input:str,outputFile:str,voice:str):
        """
        Open AI Text To Speach\n
        - input : text input\n
        - outputFile : file path and name for output\n
        - voice - Chose form : 'alloy','echo','fable','onyx','nova','shimmer'
        """
        AIModel=['tts-1','tts-1-hd']
        response = client.audio.speech.create(
        model=AIModel[0],
        voice=voice,
        response_format='mp3',
        speed=0.94,
        input=input,)
        response.stream_to_file(outputFile)
        print('Sending Text to speach')
    
    def Chat(ChatModel:str,temp:float,max_tok:int,msglist:list):
        """
        Open AI Chat GPT response\n
        - ChatModel : Open AI chat model (like gpt-4)\n
        - temp : chat temprature (creativity)- can set to 0.7\n
        - max_tok :  the maximum tokens alowed.\n
        - msglist : The message in json format.
        """
        response = client.chat.completions.create(
            model=ChatModel,
            temperature=float(temp),
            max_tokens=max_tok,
            messages=msglist)
        Result=response.choices[0].message.content
        print('Sending Text to Chat model: '+ChatModel)
        return Result
    
    def STT(file:str):
        """
        Open AI Speach to text\n
        - file : the audio file to transcript.
        """
        audio_file= open(file, "rb")
        print('Sending Speach to text')
        transcript = client.audio.translations.create( model="whisper-1", file=audio_file)
        return transcript