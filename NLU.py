
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 \
    import Features, EntitiesOptions, KeywordsOptions

natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2019-07-12',
    authenticator=IAMAuthenticator('k7068psCXo7VgHmODIQnaL9N0j4zxD7NdnLi4GtJhjkE')
)
natural_language_understanding.set_service_url('https://gateway-wdc.watsonplatform.net/natural-language-understanding/api')

def nlu(str):
    response = natural_language_understanding.analyze(
            text = str,
        features=Features(
            entities=EntitiesOptions(emotion=True, sentiment=True, limit=2),
            keywords=KeywordsOptions(emotion=True, sentiment=True,
                                     limit=2))).get_result()

    return {"entities": response.get("entities"),"keywords": response.get("keywords")}
