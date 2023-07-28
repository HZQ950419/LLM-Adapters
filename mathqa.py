import os
import re
import json
from datasets import load_dataset

dataset = load_dataset("math_qa")
save_path = "dataset/mathqa/test.json"

if not os.path.exists("dataset/mathqa/"):
    os.makedirs("dataset/mathqa/")


def writer(data, save_path):
    with open(save_path, "w") as f:
        json.dump(data, f, indent=4)

def answer_extract(sentence):
    sentence = sentence.replace(',', '')
    sentence = sentence.replace('one', '1').replace('two', '2').replace('three', '3').replace('four', '4')
    print(sentence)
    pred = [s for s in re.findall(r'-?\d+\.?\d*', sentence)]
    print(pred)
    if not pred:
        return float('inf')
    if "-" in sentence:
        pred_answer = ["-" + pred[0]]
    elif "/" in sentence or ":" in sentence:
        if len(pred) == 2 and float(pred[1]) != 0:
            pred_answer = [float(pred[0]) / float(pred[1])]
        else:
            pred_answer = float(pred[0])
    else:
        pred_answer = float(pred[0])
    print(pred_answer)
    return pred_answer

test_data = []
# for sample in dataset["test"]:
#     options = sample["options"].replace("a", "A").replace("b", "B").replace("c", "C").replace("d", "D").replace("e", "E").replace("f", "F")
#     test_data.append({
#         "instruction": f"{sample['Problem']} The options: {options}",
#         "input": "",
#         "output": "",
#         "answer": sample["correct"].upper(),
#     })

for sample in dataset["test"]:
    options = sample["options"].split(",")
    answer2index = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4}
    answer = answer_extract(options[answer2index[sample["correct"]]])
    # print(answer)

    test_data.append({
        "instruction": f"{sample['Problem']}, The options: {sample['options']}",
        "input": "",
        "output": "",
        "answer": str(answer),
    })

writer(test_data, save_path)

