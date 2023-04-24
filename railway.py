import itertools
import utils
import pandas as pd


output_file = "./output/rekt.csv"

with open("prompt/trolley.txt", "r") as f:
    prompt = f.read()

# Load previously processed permutations, if any
try:
    prev_results = pd.read_csv(output_file, dtype=str,header=None,
       names=["choice1", "choice2", "response"])
    prev_permutations = set(frozenset(row[:2]) for _, row in prev_results.iterrows())
    # Note: Using frozenset as the permutation tuple is not hashable
except FileNotFoundError:
    prev_results = pd.DataFrame(columns=["choice1", "choice2", "response"])
    prev_permutations = set()

with open("prompt/candidate_all.csv", "r") as f:
# with open("prompt/candidate_test.csv", "r") as f:
    candidate = f.read().split('\n')


for t1, t2 in itertools.permutations(candidate, 2):
    # Check if permutation has already been processed
    print(f"{t1} vs {t2}")
    if frozenset((t1, t2)) in prev_permutations:
        continue
    
    # Process permutation
    to_call = utils.tie_up(prompt, t1, t2)
    result = utils.call_ai21(to_call)
    
    # Save result to output file
    result_row = {"choice1": t1, "choice2": t2, "response": f'{result}'}  # Surround result with double quotes
    prev_results = pd.concat([prev_results, pd.DataFrame(result_row, index=[0])], ignore_index=True) 
    prev_results.to_csv(output_file,header=False, index=False)
    print(result)
    print("-------")