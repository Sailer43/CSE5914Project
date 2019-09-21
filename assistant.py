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


def find_action(text: str):
    """
    A support function for send_input

    :param
    text(str): the text from send_input to get the action required.
    :return:
    str: the trimmed message,
    str: the action requested.
    """
    start = text.find("!<+")
    if start == -1:  # The symbol not found
        return text, ''
    return text[:start], text[start + 3:]


def send_input(text: str):
    """
    Get response from Watson Assistant

    :param
    text (str): user input
    :return:
    str: message from Watson,
    str: action required,
    str: intent the user input belongs to
    """
    response = service.message(
        assistant_id='f2ddf51f-1048-44ad-a4a8-3d5a5289178a',
        session_id=sessionId,
        input={
            'message_type': 'text',
            'text': text
        }
    ).get_result()

    message, action = find_action(response['output']['generic'][0]['text'])
    intent = response['output']['intents'][0]['intent']
    return message, action, intent


##send_input('hello')
##print(find_action('I will query the weather information for you. !<+WEATHER'))

print(send_input("What' the weather tomorrow?"))