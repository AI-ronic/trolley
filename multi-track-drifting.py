import utils
import pandas as pd
import random
import time
from tqdm import tqdm

target_model = "j2-jumbo-instruct"
n_sample = 100
output_root = "./multi-track/output/"

with open("prompt/trolley.txt", "r") as f:
    prompt = f.read()

with open("prompt/candidate_all.csv", "r") as f:
    candidate = f.read().split('\n')


assert target_model in utils.model_list, "Invalid model name"

random.shuffle(candidate)

for main_track in candidate:
    task_name = utils.task_name(target_model, main_track)
    output_file = output_root + task_name + ".csv"

    if not utils.check_free(task_name):
        continue
    utils.mark_task_start(task_name)

    print(">>>>>>> Start task: ", task_name)
    prev_results = pd.DataFrame(
        columns=["model_name", "main_track", "side_track", "response", "timestamp"])
    st = time.time()

    for side_track in tqdm(random.sample(candidate, n_sample)):

        to_call = utils.tie_up(prompt, main_track, side_track)
        if target_model == "j2-jumbo-instruct":
            result = utils.call_ai21(to_call)
        elif target_model in ["gpt-3.5-turbo", "gpt-4"]:
            result = utils.call_openai_chat(to_call)
        elif target_model == "text-davinci-003":
            result = utils.call_openai_complete(to_call)
        else:
            raise Exception("Invalid model name")

        # Save result to output file
        result_row = {"model_name": target_model, "main_track": main_track,
                      "side_track": side_track, "response": f'{result}', "timestamp": time.time()}
        prev_results = pd.concat([prev_results, pd.DataFrame(
            result_row, index=[0])], ignore_index=True)
        prev_results.to_csv(output_file, header=False, index=False)
        print(result)

    print(f"task {task_name} finished in {time.time() - st} seconds")
    utils.mark_task_end(task_name)
