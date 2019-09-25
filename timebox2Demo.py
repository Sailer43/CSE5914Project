from assistant import send_input
from Converter import Converter
from NLU import nlu
import webbrowser as wb

FOOD_URL = "https://ohiostatefair.com/food/?search-input={input}&checkbox=on&submit=submit&map=food"
MUSIC_URL = "https://www.lyrics.com/lyrics/{input}"
MOVIE_URL = "https://www.imdb.com/find?ref_=nv_sr_fn&q={input}&s=all"
WEATHER_URL = "https://weather.com/weather/tenday/l/Columbus+OH+USOH0212:1:US"


def query_food(keywords: list):
    wb.open(FOOD_URL.format(input="+".join(keywords)))


def query_music(keywords: list):
    wb.open(MUSIC_URL.format(input="%".join(keywords)))


def query_movie(keywords: list):
    wb.open(MOVIE_URL.format(input="+".join(keywords)))


def query_weather(keywords: list):
    wb.open(WEATHER_URL)


function_map = {"Ask_Recommendation_Movie": query_movie,
                "Ask_Recommendation_Music": query_music,
                "Ask_Recommendation_Restaurant": query_food,
                "Ask_Weather": query_weather}


def main():
    converter = Converter()
    while True:
        print("Start recording")
        converter.record()
        print("End recording")
        user_input = converter.listen()
        if user_input[0]:
            print('"{}"'.format(user_input[1]))
            text, action, intent = send_input(user_input[1])
            print(text)
            if intent in ["Ask_Recommendation_Movie",
                          "Ask_Recommendation_Music",
                          "Ask_Recommendation_Restaurant",
                          "Ask_Weather"]:
                try:
                    r = nlu(user_input[1])
                    keywords = [sub_r["text"] for sub_r in r["keywords"]]
                    print(keywords)
                    function_map[intent](keywords)
                except Exception:
                    pass
                pass
            converter.text2speech(text)
            if intent == "General_Ending":
                break
            input()
        else:
            converter.text2speech(user_input[1])


if __name__ == '__main__':
    main()
