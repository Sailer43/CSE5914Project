import spacy


def find_keywords(text: str) -> list:
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]


def extract_keywords(tag: str, response: list) -> list:
    return [entry[0] for entry in response if entry[1] == tag]


def main():
    print(extract_keywords("WORK_OF_ART", find_keywords("something")))


if __name__ == '__main__':
    main()
