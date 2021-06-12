import os
from gnewsclient import gnewsclient
import dialogflow_v2 as dialogflow

# use pip install dialogflow, gnewsclient

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "client.json"
"""To get this client.json file, on your dialogflow agent settings, click on project_id, this will take you to
google console.. over there make a service account(Make it as owner).. then download a key for it in json format"""


dialogflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = "newsbot-9ymg"

client = gnewsclient.NewsClient()


def detect_intent_from_text(text, session_id, language_code='en'):
    session = dialogflow_session_client.session_path(PROJECT_ID, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
    print(response)
    return response.query_result


def get_reply(query, chat_id):
    response = detect_intent_from_text(query, chat_id)

    if response.intent.display_name == 'get_news':
        return "get_news", dict(response.parameters)
    else:
        return "small_talk", response.fulfillment_text


def fetch_news(parameters):
    news = []
    client.language = parameters.get('language')
    client.topic = parameters.get('topic')
    if len(parameters.get('geo-country'))==0:
        return client.get_news()[:5]
    else:
        for country in parameters.get('geo-country'):
            client.location = country
            news_from_one_country = client.get_news()[:5]
            news.extend(news_from_one_country)
    
        return news

topics_keyboard = [
    ["Top Stories", 'World', "Nation"],
    ["Business", "Technology", "Entertainment"],
    ["Sports", "Science", "Health"]
]