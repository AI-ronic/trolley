import ai21
from dotenv import load_dotenv
import os

load_dotenv()

ai21.api_key = os.getenv("AI21_API_KEY")

print(ai21.api_key)


def cleanup(ai21_result):
    return ai21_result.completions[0]['data']['text'].replace('\n', '')


def tie_up(prompt, track1, track2):
    return prompt.replace('[__track1__]', track1).replace('[__track2__]', track2)


def call_ai21(prompt):
    return cleanup(ai21.Completion.execute(
        model="j2-jumbo-instruct",
        prompt=prompt,
        numResults=1,
        maxTokens=100,
        temperature=0,
        topKReturn=0,
        topP=1,
        countPenalty={
            "scale": 0,
            "applyToNumbers": False,
            "applyToPunctuations": False,
            "applyToStopwords": False,
            "applyToWhitespaces": False,
            "applyToEmojis": False
        },
        frequencyPenalty={
            "scale": 0,
            "applyToNumbers": False,
            "applyToPunctuations": False,
            "applyToStopwords": False,
            "applyToWhitespaces": False,
            "applyToEmojis": False
        },
        presencePenalty={
            "scale": 0,
            "applyToNumbers": False,
            "applyToPunctuations": False,
            "applyToStopwords": False,
            "applyToWhitespaces": False,
            "applyToEmojis": False
        },
        stopSequences=[]
    ))
