from time import sleep
import webbrowser as wb
from ibm_watson import TextToSpeechV1
from os import system


MUSIC_DIR = "music/"

class MusicPlayer:

    def __init__(self):
        self.i = 0

    def play_music(self):
        self.i += 1
        system("open " + MUSIC_DIR + str(self.i) + ".mp3")


def print_sentence(string: str):
    for s in string.split(" "):
        print(s, end=" ")
        sleep(0.5)
    print()


def dl_sound(i: int, string: str):
    speaker = TextToSpeechV1(iam_apikey="euoR7ZdLMOBd29wP1fNaZFJsqwKt45TUmwcVwpzbQBcA",
                             url="https://gateway-wdc.watsonplatform.net/text-to-speech/api")
    with open("music/{i}.mp3".format(i=i), "wb") as audio_file:
        audio_file.write(
            speaker.synthesize(
                string,
                voice="en-US_AllisonVoice",
                accept="audio/mp3"
            ).get_result().content)


def main():
    mp = MusicPlayer()

    input()
    print(">>>Setup<<<")
    mp.play_music()
    print("What's your name?")
    input()

    mp.play_music()
    print("What do you usually do during weekends?")
    input()
    mp.play_music()
    print("What's you favorite food?")
    input()
    mp.play_music()
    print("Do you have any pets?")
    input()
    mp.play_music()
    print("What kind of music do you like?")
    input()
    mp.play_music()
    print("Could you name some movies you like?")
    print(">>>Setup Finished<<<")

    input()
    print_sentence(">>>I broke up with my girlfriend.")
    mp.play_music()
    print("<<<You probably need to check out this movie.")
    sleep(2)
    wb.open("https://www.imdb.com/title/tt1187043/")
    print()

    input()
    print_sentence(">>>My dog passed out today.")
    mp.play_music()
    print("<<<I have a music clip for you.")
    sleep(2)
    wb.open("https://www.youtube.com/watch?time_continue=10&v=vTnWFT3DvVA")
    print()

    input()
    print_sentence(">>>What day is it today?")
    mp.play_music()
    print("<<<It's Monday.")
    sleep(2)
    print_sentence(">>>OH... I don't wanna go work.")
    mp.play_music()
    print("<<<Here are 12 excuses for missing work.")
    sleep(2)
    wb.open("https://www.cleverism.com/12-excuses-missing-work/")
    print()

    input()
    print_sentence(">>>Do you know any good Chinese restaurants around here?")
    mp.play_music()
    print("<<<Here are 10 best Chinese restaurants in Columbus.")
    sleep(2)
    wb.open("https://www.tripadvisor.com/Restaurants-g50226-c11-Columbus_Ohio.html")
    print()

    input()
    print_sentence(">>>Today is my payday.")
    mp.play_music()
    print("<<<I guess you really wanna spend some money today, right?")
    sleep(2)
    wb.open("https://www.amazon.com")

    input()
    print_sentence(">>>What's the weather today?")
    mp.play_music()
    print("<<<Here is the weather today.")
    sleep(2)
    wb.open("https://weather.com/weather/today/l/40.01,-83.03?par=google&temp=f")


if __name__ == '__main__':
    main()
