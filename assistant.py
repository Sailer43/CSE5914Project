import json
import ibm_watson

service = ibm_watson.AssistantV2(
    iam_apikey="A4LMwqnkIQac81v88v14_AZLj5F__wjY83S9WOgjqAXw",
    version='2019-02-28',
    url='https://gateway-wdc.watsonplatform.net/assistant/api'
)

session = service.create_session(
    assistant_id='f2ddf51f-1048-44ad-a4a8-3d5a5289178a'
).get_result()

sessionId = session["session_id"]


def send_input(user_in):
    response = service.message(
        assistant_id='f2ddf51f-1048-44ad-a4a8-3d5a5289178a',
        session_id = sessionId,
        input={
            'message_type': 'text',
            'text': user_in
        }
    ).get_result()
    message = response['output']['generic'][0]['text']
    return message


send_input('hello')

