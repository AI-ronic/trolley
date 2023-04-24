import itertools
import utils


with open("prompt/trolley.txt", "r") as f:
    prompt = f.read()

with open("prompt/candidate.csv", "r") as f:
    candidate = f.read().split('\n')

out = []

for t1, t2 in list(itertools.permutations(candidate, 2)):
    print(f"{t1} vs {t2}")
    to_call = utils.tie_up(prompt, t1, t2)
    result = utils.call_ai21(to_call)
    print(result)
    print("-------")
    out.append([t1, t2, result])

with open("output/rekt.csv", "w") as f:
    for l in out:
        f.write(",".join(l) + "\n")
