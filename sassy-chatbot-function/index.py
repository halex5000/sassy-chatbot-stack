import os
import ldclient
from ldclient.config import Config
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

# Set sdk_key and feature_flag_key to your LaunchDarkly keys
sdk_key = os.getenv("LAUNCHDARKLY_SDK_KEY") or ''
feature_flag_key = "chatbot-feature"

ldclient.set_config(Config(sdk_key))

target = {
    "key": "5de6fc8b62da8a3d7fc41402624f2319",
    "firstName": "Bill",
    "lastName": "Bobaggins",
    "custom": {
        "groups": "beta_testers",
        "plan": "silver"
    }
}


def handler(event, context):

    question = event["queryStringParameters"]["question"]
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=generate_prompt(question),
        temperature=0.6,
    )

    return response


def generate_prompt(question):
    # Call LaunchDarkly and execute some code based on flag state
    show_feature = ldclient.get().variation(feature_flag_key, target, False)
    if show_feature:
        return """Answer the following question in a helpful way:
        
        Question: Who is the current president of the USA?
        Answer: Good question! The current president is Joe Biden.
        Question: What's your favorite animal?
        Answer: I love all animals, but my favorite is the elephant.
        Question: How many feet are in a mile?
        Answer: What a curious mind you have! There are 5280 feet in a mile.
        Question:{}
        Answer:""".format(
            question.capitalize()
        )
    else:
        return """Answer the following question in a mean way:
        
        Question: Who is the current president of the USA?
        Answer: That's a dumb question! The current president is Joe Biden.
        Question: What's your favorite animal?
        Answer: Animals suck, but if I have to choose one, I pick the mosquito.
        Question: How many feet are in a mile?
        Answer: You're pretty stupid! There are 5280 feet in a mile, lazybones.
        Question:{}
        Answer:""".format(
            question.capitalize()
        )
