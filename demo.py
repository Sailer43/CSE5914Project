from time import sleep
import webbrowser as wb


def print_sentence(string: str):
    for s in string.split(" "):
        print(s, end=" ")
        sleep(0.5)
    print()


def main():

    print(">>>Setup<<<")
    print("What's your name?")
    input()

    print("What do you usually do during weekends?")
    input()
    print("What's you favorite food?")
    input()
    print("Do you have any pets?")
    input()
    print("What kind of music do you like?")
    input()
    print("Could you name some movies you like?")
    print(">>>Setup Finished<<<")

    input()
    print_sentence(">>>I broke up with my girlfriend.")
    print("<<<You probably need to check out this movie.")
    sleep(2)
    wb.open("https://www.imdb.com/title/tt1187043/")
    print()

    input()
    print_sentence(">>>My dog passed out today.")
    print(">>>I have a music clip for you.")
    sleep(2)
    wb.open("https://www.youtube.com/watch?time_continue=10&v=vTnWFT3DvVA")
    print()

    input()
    print_sentence(">>>What day is it today?")
    print("<<<It's Monday.")
    sleep(2)
    print_sentence(">>>OH... I don't wanna go work.")
    print("<<<Here are 12 excuses for missing work.")
    sleep(2)
    wb.open("https://www.cleverism.com/12-excuses-missing-work/")
    print()

    input()
    print_sentence(">>>Do you know any good Chinese restaurants around here?")
    print("<<<Here are 10 best Chinese restaurants in Columbus.")
    sleep(2)
    wb.open("https://www.tripadvisor.com/Restaurants-g50226-c11-Columbus_Ohio.html")
    print()

    input()
    print_sentence(">>>Today is my payday.")
    print("<<<I guess you really wanna spend some money today, right?")
    sleep(2)
    wb.open("https://www.amazon.com")

    input()
    print_sentence(">>>What's the weather today?")
    print("<<<Here is the weather today.")
    sleep(2)
    wb.open("https://weather.com/weather/today/l/40.01,-83.03?par=google&temp=f")


if __name__ == '__main__':
    main()
