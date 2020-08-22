from json import loads, dumps


PROFILE_PATH = "User Profile"


class Profiler:

    def __init__(self, alpha=0.75):
        with open(PROFILE_PATH, "r") as profile_file:
            profile = "\n".join(profile_file.readlines())
            self.profile_dict = loads(profile)
        self.alpha = 0.75

    def record(self, keywords: list, entities: list):
        profile_keywords = self.profile_dict["keywords"]
        profile_entities = self.profile_dict["entities"]
        for keyword in keywords:
            text = keyword["text"]
            sentiment = keyword["sentiment"]["score"]
            relevance = keyword["relevance"]
            emotion = keyword["emotion"]
            sadness = emotion["sadness"]
            joy = emotion["joy"]
            fear = emotion["fear"]
            disgust = emotion["disgust"]
            anger = emotion["anger"]
            count = keyword["count"]
            if text in profile_keywords.keys():
                entry = profile_keywords[text]
                entry["sentiment"] = self.value_decedent(entry["sentiment"], sentiment)
                entry["relevance"] = self.value_decedent(entry["relevance"], relevance)
                entry["sadness"] = self.value_decedent(entry["sadness"], sadness)
                entry["joy"] = self.value_decedent(entry["joy"], joy)
                entry["fear"] = self.value_decedent(entry["fear"], fear)
                entry["disgust"] = self.value_decedent(entry["disgust"], disgust)
                entry["anger"] = self.value_decedent(entry["anger"], anger)
                entry["count"] += count
            else:
                profile_keywords[text] = dict()
                entry = profile_keywords[text]
                entry["sentiment"] = sentiment
                entry["relevance"] = relevance
                entry["sadness"] = sadness
                entry["joy"] = joy
                entry["fear"] = fear
                entry["disgust"] = disgust
                entry["anger"] = anger
                entry["count"] = count

        for entity in entities:
            text = entity["text"]
            m_type = entity["type"]
            count = entity["count"]
            confidence = entity["confidence"]
            if text in profile_entities.keys():
                entry = profile_entities[text]
                entry["count"] += count
                entry["confidence"] = self.value_decedent(entry["confidence"], confidence)
            else:
                profile_entities[text] = dict()
                entry = profile_entities[text]
                entry["type"] = m_type
                entry["count"] = count
                entry["confidence"] = confidence
        self.write_to_file()

    def get_keyword(self, entity_name: str):
        profile_keywords = self.profile_dict["keywords"]
        if entity_name in profile_keywords.keys():
            return profile_keywords[entity_name]
        else:
            return None

    def get_entity(self, entity_name: str):
        profile_entities = self.profile_dict["entities"]
        if entity_name in profile_entities.keys():
            return profile_entities[entity_name]
        else:
            return None

    def write_to_file(self):
        with open(PROFILE_PATH, "w") as profile_file:
            profile_file.write(dumps(self.profile_dict))

    def value_decedent(self, original_val, new_val):
        return original_val * (1 - self.alpha) + new_val * self.alpha
