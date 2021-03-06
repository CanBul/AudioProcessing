import speech_recognition as sr_audio
import sounddevice as sd
import soundfile as sf
import os, json, datetime

def sync_record(filename, duration, fs, channels):
    print('recording')
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=channels)
    sd.wait()
    sf.write(filename, myrecording, fs)
    print('done recording')

def transcribe_audio_sphinx(filename):
    # transcribe the audio (note this is only done if a voice sample)
    r=sr_audio.Recognizer()
    with sr_audio.WavFile(filename) as source:
        audio = r.record(source) 
    text=r.recognize(audio)
    print('transcript: '+text)
    
    return text

def store_transcript(filename, transcript):
    jsonfilename=filename[0:-4]+'.json'
    print('saving %s to current directory'%(jsonfilename))
    data = {
        'date': str(datetime.datetime.now()),
        'filename':filename,
        'transcript':transcript,
        }
    print(data)
    jsonfile=open(jsonfilename,'w')
    json.dump(data,jsonfile)
    jsonfile.close()

# record file and print transcript
filename='sync_record.wav'
sync_record(filename, 3, 16000, 1)
transcript=transcribe_audio_sphinx(filename)

# now write the transcript into a .json file
# e.g. sync_record.wav transcript will be stored in sync_record.json
store_transcript(filename, transcript)

