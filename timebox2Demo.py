from assistant import send_input
from Converter import Converter
from NLU import nlu
import webbrowser as wb
from nltk_functions import extract_keywords, find_keywords
from fetch_web import read_web

FOOD_URL = "https://ohiostatefair.com/food/?search-input={input}&checkbox=on&submit=submit&map=food"
MUSIC_URL = "https://www.lyrics.com/lyrics/{input}"
MOVIE_URL = "https://www.imdb.com/find?ref_=nv_sr_fn&q={input}&s=all"
WEATHER_URL = "https://weather.com/weather/tenday/l/Columbus+OH+USOH0212:1:US"


def query_food(keywords: list):
    wb.open(FOOD_URL.format(input="+".join(keywords)))
    return


def query_music(keywords: list):
    url = MUSIC_URL.format(input="+".join(keywords))
    keyword_list = extract_keywords("WORK_OF_ART", find_keywords(read_web(url)))
    wb.open(url)
    keyword_list = [k for k in keyword_list if k not in ["» Lyrics:"]]
    return keyword_list[1:5]


def query_movie(keywords: list):
    url = MOVIE_URL.format(input="+".join(keywords))
    keyword_list = extract_keywords("WORK_OF_ART", find_keywords(read_web(url)))
    wb.open(url)
    return keyword_list[1:5]


def query_weather(keywords: list):
    wb.open(WEATHER_URL)
    return


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
            try:
                text, action, intent = send_input(user_input[1])
            except IndexError:
                text = "I don't understand what you are saying."
                intent = None
            if intent in ["Ask_Recommendation_Movie",
                          "Ask_Recommendation_Music",
                          "Ask_Recommendation_Restaurant",
                          "Ask_Weather"]:
                try:
                    r = nlu(user_input[1])
                    keywords = [sub_r["text"] for sub_r in r["keywords"]]
                    keyword_list = list()
                    for keyword in keywords:
                        keyword_list.extend([k for k in keyword.split() if k not in ["HESITATION", "movie", "song"]])
                    result = function_map[intent](keyword_list)
                    if result:
                        text = str(text)
                        text = text.format(result=", ".join(result))
                except Exception as e:
                    print(e)
                pass
            print(text)
            converter.text2speech(text)
            if intent == "General_Ending":
                break
            input()
        else:
            converter.text2speech(user_input[1])


if __name__ == '__main__':
    main()
