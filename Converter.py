from ibm_watson import TextToSpeechV1, SpeechToTextV1, DetailedResponse
import pyaudio as pa

from os import system
from threading import Thread
from wave import open as w_open
from json import loads


class Converter:

    m_isRecording = False
    m_thread = None

    k_s2t_api_key = "0pxCnJQ_r5Yy3SZDRhYS4XshrTMJyZEsuc45SbBcfGgf"
    k_t2s_api_key = "euoR7ZdLMOBd29wP1fNaZFJsqwKt45TUmwcVwpzbQBcA"
    k_s2t_url = "https://stream.watsonplatform.net/speech-to-text/api"
    k_t2s_url = "https://gateway-wdc.watsonplatform.net/text-to-speech/api"
    k_t2s_voice = "en-US_AllisonVoice"
    k_t2s_format = "audio/mp3"
    k_st2_model = "en-US_NarrowbandModel"
    k_folder = "music/"
    k_music_temp_out = "temp_out.mp3"
    k_music_temp_in = "temp_in.wav"
    k_fs = 44100
    k_chuck = 1024
    k_format = pa.paInt16
    k_channels = 1

    def __init__(self):
        self.s2t = SpeechToTextV1(iam_apikey=self.k_s2t_api_key, url=self.k_s2t_url)
        self.t2s = TextToSpeechV1(iam_apikey=self.k_t2s_api_key, url=self.k_t2s_url)
        self.py_audio = pa.PyAudio()

    def read(self, string: str):
        with open(self.k_folder + self.k_music_temp_out, "wb") as audio_file:
            audio_file.write(
                self.t2s.synthesize(
                    string,
                    voice=self.k_t2s_voice,
                    accept=self.k_t2s_format
                ).get_result().content
            )

    def play_music(self):
        system("open " + self.k_folder + self.k_music_temp_out)

    def record(self):
        self.m_thread = Thread(target=self._record, args=())
        self.m_isRecording = True
        self.m_thread.start()
        input()
        self.m_isRecording = False
        self.m_thread.join()

    def listen(self):
        with open(self.k_folder + self.k_music_temp_in, "rb") as audio_file:
            result = self.s2t.recognize(audio_file, model=self.k_st2_model)
            result = loads(str(result))
            result = result["result"]["results"][0]["alternatives"]
            return result

    def _record(self):
        stream = self.py_audio.open(format=self.k_format,
                                    channels=self.k_channels,
                                    rate=self.k_fs,
                                    frames_per_buffer=self.k_chuck,
                                    input=True,
                                    output=True)
        frames = []
        while self.m_isRecording:
            frames.append(stream.read(self.k_chuck))
        stream.stop_stream()
        stream.close()
        self._write_audio(frames)

    def _write_audio(self, frames: list):
        wf = w_open(self.k_folder + self.k_music_temp_in, 'wb')
        wf.setnchannels(self.k_channels)
        wf.setsampwidth(self.py_audio.get_sample_size(self.k_format))
        wf.setframerate(self.k_fs)
        wf.writeframes(b''.join(frames))
        wf.close()

    def on_stop(self):
        self.py_audio.terminate()

    def text2speech(self, string: str):
        self.read(string)
        self.play_music()


def main():
    converter = Converter()
    converter.record()
    print(converter.listen())


if __name__ == '__main__':
    main()
