from urllib.request import urlopen
from bs4 import BeautifulSoup


def read_web(url: str):
    fp = urlopen(url)
    html = fp.read()
    html.decode("utf8")
    fp.close()
    converter = BeautifulSoup(html, features="html.parser")
    for script in converter(["script", "style"]):
        script.extract()
    text = converter.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = ' '.join(chunk for chunk in chunks if chunk)
    return text


def main():
    print(read_web("https://open.spotify.com/search/David%20Bowie's%20music"))


if __name__ == '__main__':
    main()