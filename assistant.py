from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import ibm_watson

APIKEY = "A4LMwqnkIQac81v88v14_AZLj5F__wjY83S9WOgjqAXw"
APIVERSION = '2019-02-28'
APIURL = 'https://gateway-wdc.watsonplatform.net/assistant/api'
ASSISTANT_ID = 'f2ddf51f-1048-44ad-a4a8-3d5a5289178a'

service = ibm_watson.AssistantV1(
    version = APIVERSION,
    authenticator=IAMAuthenticator(APIKEY)
)
service.set_service_url(APIURL)

workspaceID = service.list_workspaces(
    assistant_id=ASSISTANT_ID
).get_result()["workspaces"][0]["workspace_id"]


def find_action(text: str) -> (str, str):
    """
    A support function for send_input

    :param
    text(str): the text from send_input to get the action required.
    :return:
    str: the trimmed message
    str: the action requested. Empty if no action required.
    """
    start = text.find("!<+")
    if start == -1:  # The symbol not found
        return text, ''
    return text[:start], text[start + 3:]


def send_input(text: str) -> (str, str, str):
    """
    Get response from Watson Assistant

    :param
    text (str): user input
    :return:
    str: message from Watson
    str: action required. empty string if no action required
    str: intent the user input belongs to
    """
    # noinspection PyTypeChecker
    response = service.message(
        workspace_id=workspaceID,
        input={
            'message_type': 'text',
            'text': text
        }
    ).get_result()

    message, action = find_action(response['output']['text'][0])
    intent = response['intents'][0]['intent']
    return message, action, intent


def add_example_to_intent(user_input: str, intent: str) -> (bool, str):
    """
    add an example to an intent.

    :param user_input: The user input which would be put under the intent specified behind.
    :param intent: Name of the intent.

    :return: return if successfully updated the intent. If returned false, the string will be the message from the API.
    """
    try:
        # origin_response = \
        service.create_example(
            workspace_id=workspaceID,
            intent=intent,
            text=user_input
        )
        # response = origin_response.get_result()
        # status = origin_response.get_status_code()
        return True, ''
    except ibm_cloud_sdk_core.api_exception.ApiException as e:
        return False, e.message


def add_counterexample_to_intent(user_input: str, intent: str) -> (bool, str):
    """
    add an counterexample to an intent.

    :param user_input: The user input which would not be put under the intent specified behind.
    :param intent: Name of the intent.

    :return: return if successfully updated the intent. If returned false, the string will be the message from the API.
    """
    try:
        # origin_response = \
        service.create_counterexample(
            workspace_id=workspaceID,
            intent=intent,
            text=user_input
        )
        # response = origin_response.get_result()
        # status = origin_response.get_status_code()
        return True, ''
    except ibm_cloud_sdk_core.api_exception.ApiException as e:
        return False, e.message


if __name__ == "__main__":
    # send_input('hello')
    # print(find_action('I will query the weather information for you. !<+WEATHER'))
    # print(send_input("Hello"))
    print(add_example_to_intent("Test if it works?", "TestIntents"))
