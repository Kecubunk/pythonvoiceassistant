import webbrowser
import string
import speech_recognition as sr
from gtts import gTTS
from weather import Weather
from pygame import mixer
import time
import subprocess

#obtain audio
weather = Weather()
mixer.init()
r = sr.Recognizer()
i = 0
while i == 0:  
    with sr.Microphone() as source:
        try:
            key = r.listen(source)
            if 'Jackson' in r.recognize_google(key):
                mixer.music.load('on.wav')
                mixer.music.play()
                userinput = r.listen(source)
                userinputtext = r.recognize_google(userinput)
                if 'help' in userinputtext or 'Help' in userinputtext:
                    mixer.music.load('help.mp3')
                    mixer.music.play()
                #this program shits the bed with the weather
                elif 'weather' in userinputtext or 'Weather' in userinputtext:
                    mixer.music.load('cityprompt.mp3')
                    mixer.music.play()
                    print("What city would you like the weather from?")
                    audio = r.listen(source)
                    audiotext = r.recognize_google(audio)
                    try:    
                        location = weather.lookup_by_location(audiotext)
                        condition = location.condition()
                        tts = gTTS(text="It is currently " + condition.text() + " in " + audiotext, lang='en', slow=False)
                        tts.save('currentcondition.mp3')
                        mixer.music.load('currentcondition.mp3')
                        mixer.music.play()
                        print("It is currently " + condition.text() + " in " + audiotext)
                    except:
                        tts = gTTS(text="Error while trying to get the weather for that city", lang='en', slow=False)
                        tts.save('error.mp3')
                        mixer.music.load('error.mp3')
                        mixer.music.play()
                        print("Error while trying to get the weather for that city")

                elif 'time' in userinputtext or 'Time' in userinputtext:
                    now = time.localtime(time.time())
                    curtime = time.asctime(now)
                    thetime = curtime[11:19]
                    minute = thetime[3:5]
                    hour = thetime[0:2]
                    morn = 'AM'
                    altered = False
                    if hour == '00':
                        hour = '12'
                        altered = True
                    elif int(hour) > 12:
                        hour = str(int(hour) - 12)
                        morn = 'PM'
                    if altered:
                        morn = 'AM'     
                    
                    tts = gTTS(text="It is currently " + hour + ":" + minute + ' ' + morn, lang='en', slow=False)
                    tts.save('time.mp3')
                    mixer.music.load('time.mp3')
                    mixer.music.play()
                    
                elif 'alarm' in userinputtext or 'Alarm' in userinputtext:
                    try:
                        mixer.music.load('alarmprompt.mp3')
                        mixer.music.play()
                        audio = r.listen(source)
                        audiotext = r.recognize_google(audio)
                        userinputtext = str(audiotext)
                        if len(userinputtext) == 4:
                            hour = userinputtext[0:2]
                            minute = userinputtext[2:4]
                        elif len(userinputtext) == 2:
                            hour = userinputtext[0:2]
                            minute = '00'
                        elif len(userinputtext) == 5:
                            hour = userinputtext[0:2]
                            minute = userinput[3:5]
                        elif len(userinputtext) == 1:
                            hour = userinputtext[0:1]
                            minute = '00'
                        
                        tts = gTTS(text="An alarm has been set at " + hour + ":" + minute, lang='en', slow=False)
                        tts.save('alarm.mp3')
                        mixer.music.load('alarm.mp3')
                        mixer.music.play()
                    except:
                        mixer.music.load('alarmproblem.mp3')
                        mixer.music.play()
                    
                     
            else:
                continue
        except:
            continue
