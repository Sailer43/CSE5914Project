from ibm_watson import TextToSpeechV1, SpeechToTextV1

class Converter:

    k_s2t_api_key = "0pxCnJQ_r5Yy3SZDRhYS4XshrTMJyZEsuc45SbBcfGgf"
    k_t2s_api_key = "euoR7ZdLMOBd29wP1fNaZFJsqwKt45TUmwcVwpzbQBcA"
    k_s2t_url = "https://stream.watsonplatform.net/speech-to-text/api"
    k_t2s_url = "https://gateway-wdc.watsonplatform.net/text-to-speech/api"
    k_t2s_voice = "en-US_AllisonVoice"
    k_t2s_format = "audio/mp3"
    k_folder = "music/"

    def __init__(self):
        self.s2t = SpeechToTextV1(iam_apikey=self.k_s2t_api_key, url=self.k_s2t_url)
        self.t2s = TextToSpeechV1(iam_apikey=self.k_t2s_api_key, url=self.k_t2s_url)

    def read(self, string: str):
        with open(self.k_folder + "temp_out.mp3", "wb") as audio_file:
            audio_file.write(
                self.t2s.synthesize(
                    string,
                    voice=self.k_t2s_voice,
                    accept=self.k_t2s_format
                ).get_result().content
            )

    def record(self, string: str = "temp_in.mp3"):
        pass

