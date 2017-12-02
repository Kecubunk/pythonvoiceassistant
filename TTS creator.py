#this is a program to create a text to speech mp3

from gtts import gTTS

tts = gTTS(text="Please fuck me Ethan", lang='en')
tts.save('ethan.mp3')
