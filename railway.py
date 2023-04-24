import itertools
import utils
import pandas as pd


with open("prompt/trolley.txt", "r") as f:
    prompt = f.read()

with open("prompt/candidate.csv", "r") as f:
# with open("prompt/candidate_test.csv", "r") as f:
    candidate = f.read().split('\n')

out = []

for t1, t2 in list(itertools.permutations(candidate, 2)):
    print(f"{t1} vs {t2}")
    to_call = utils.tie_up(prompt, t1, t2)
    result = utils.call_ai21(to_call)
    print(result)
    print("-------")
    out.append([t1, t2, result])

out_df = pd.DataFrame(out, 
    columns=["choice1", "choice2", "response"])

out_df.to_csv("output/rekt.csv")

# with open("output/rekt.csv", "w") as f:
#     for l in out:
#         f.write(",".join(l) + "\n")
