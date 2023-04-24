import openai
import ai21
from dotenv import load_dotenv
import os

load_dotenv()

ai21.api_key = os.getenv("AI21_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")

def tie_up(prompt, track1, track2):
    return prompt.replace('[__track1__]', track1).replace('[__track2__]', track2)


def cleanup_ai21(ai21_result):
    return ai21_result.completions[0]['data']['text'].replace('\n', ' ').strip()


def call_ai21(prompt):
    return cleanup_ai21(ai21.Completion.execute(
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


def cleanup_oai(oai_result):
    return oai_result['choices'][0]['text'].replace('/n', ' ').strip()


def call_openai_complete(prompt):
    return openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )


def call_openai_chat(prompt):
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": 'system', "content": "you are a good person"},
            {"role": "user", "content": prompt}
        ]
    )
