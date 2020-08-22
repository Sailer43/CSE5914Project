from ibm_watson import TextToSpeechV1, SpeechToTextV1, DetailedResponse

from os import system
from json import loads


class Converter:

    k_s2t_api_key = "0pxCnJQ_r5Yy3SZDRhYS4XshrTMJyZEsuc45SbBcfGgf"
    k_t2s_api_key = "euoR7ZdLMOBd29wP1fNaZFJsqwKt45TUmwcVwpzbQBcA"
    k_s2t_url = "https://stream.watsonplatform.net/speech-to-text/api"
    k_t2s_url = "https://gateway-wdc.watsonplatform.net/text-to-speech/api"
    k_t2s_voice = "en-US_AllisonVoice"
    k_t2s_format = "audio/webm"
    k_st2_model = "en-US_NarrowbandModel"

    def __init__(self):
        self.s2t = SpeechToTextV1(iam_apikey=self.k_s2t_api_key, url=self.k_s2t_url)
        self.t2s = TextToSpeechV1(iam_apikey=self.k_t2s_api_key, url=self.k_t2s_url)

    def read(self, string: str):
        return self.t2s.synthesize(
            string,
            voice=self.k_t2s_voice,
            accept=self.k_t2s_format
        ).get_result().content

    def listen(self, audio_input):
        try:
            result = self.s2t.recognize(audio_input, model=self.k_st2_model)
            result = loads(str(result))
            result = result["result"]["results"][0]["alternatives"][0]['transcript']
        except Exception:
            return False, "I don't understand what you are saying."
        return True, str(result)


def main():
    pass


if __name__ == '__main__':
    main()
