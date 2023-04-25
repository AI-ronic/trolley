import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
import openai
import ai21
from dotenv import load_dotenv
import os

load_dotenv()

ai21.api_key = os.getenv("AI21_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")
serviceAccount_path = os.getenv("GCP_SERVICE_ACCOUNT_PATH")


cred = credentials.Certificate(serviceAccount_path)
app = firebase_admin.initialize_app(cred)
db = firestore.client()

model_list = ["j2-jumbo-instruct",
              "text-davinci-003", "gpt-3.5-turbo", "gpt-4"]


def tie_up(prompt, track1, track2):
    return prompt.replace('[__track1__]', track1).replace('[__track2__]', track2)


def cleanup_ai21(ai21_result):
    return ai21_result.completions[0]['data']['text'].replace('\n', ' ').replace(",", " ").strip()


def call_ai21(prompt, model_name="j2-jumbo-instruct"):
    return cleanup_ai21(ai21.Completion.execute(
        model=model_name,
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
    return oai_result['choices'][0]['text'].replace('/n', ' ').replace(",", " ").strip()


def call_openai_complete(prompt, model_name="text-davinci-003"):
    return cleanup_oai(openai.Completion.create(
        model=model_name,
        prompt=prompt,
        temperature=0,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    ))


def call_openai_chat(prompt, model_name="gpt-3.5-turbo"):
    return cleanup_oai(openai.ChatCompletion.create(
        model=model_name,
        messages=[
            {"role": 'system', "content": "you are a good person"},
            {"role": "user", "content": prompt}
        ]
    ))


def check_free(task):
    doc_ref = db.collection('coffin').document(task)
    doc = doc_ref.get()
    if doc.exists:
        return False
    return True


def mark_task_start(task):
    doc_ref = db.collection('coffin').document(task)
    doc_ref.set({
        'status': 'started',
        'date': firestore.SERVER_TIMESTAMP
    })


def mark_task_done(task):
    doc_ref = db.collection('coffin').document(task)
    doc_ref.set({
        'status': 'done',
        'date': firestore.SERVER_TIMESTAMP
    })


def task_name(model_name, main_track):
    return f'{model_name}_{main_track}'

