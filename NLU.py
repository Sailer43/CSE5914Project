
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 \
    import Features, EntitiesOptions, KeywordsOptions

natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2019-07-12',
    iam_apikey='k7068psCXo7VgHmODIQnaL9N0j4zxD7NdnLi4GtJhjkE',
    url='https://gateway-wdc.watsonplatform.net/natural-language-understanding/api'
)


def nlu(str):
    response = natural_language_understanding.analyze(
            text = str,
        features=Features(
            entities=EntitiesOptions(emotion=True, sentiment=True, limit=2),
            keywords=KeywordsOptions(emotion=True, sentiment=True,
                                     limit=2))).get_result()

    return {"entities": response.get("entities"),"keywords": response.get("keywords")}

print(nlu("""WASHINGTON — A potentially explosive complaint by a whistle-blower in the intelligence community said to involve President Trump was related to a series of actions that go beyond any single discussion with a foreign leader, according to interviews on Thursday.

The complaint was related to multiple acts, Michael Atkinson, the inspector general for American spy agencies, told lawmakers during a private briefing, two officials familiar with it said. But he declined to discuss specifics, including whether the complaint involved the president, according to committee members.

Separately, a person familiar with the whistle-blower’s complaint said it involves in part a commitment that Mr. Trump made in a communication with another world leader. The Washington Post first reported the nature of that discussion. But no single communication was at the root of the complaint, another person familiar with it said.

The complaint cleared an initial hurdle when Mr. Atkinson deemed it credible and began to pursue an investigation. But it has prompted a standoff between lawmakers and the acting director of national intelligence, Joseph Maguire, who has refused to turn it over to Congress, as is generally required by law. It has become the latest in a series of fights over information between the Democratic-led House and the White House."""))