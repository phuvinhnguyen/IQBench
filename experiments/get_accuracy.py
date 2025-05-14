# !!! This file is no longer needed as the vlms can parse the answer correctly

import json
import os
from FlowDesign.litellm import LLMInference
import time
from tqdm import tqdm

def create_conversation(question, answer):
    prompt = f"""You are given a question and an answer provided by another agent.

Question:
{question}

Agent's Answer:
{answer}

Your task is to revise the agent's answer and convert it into the correct final format:
- For multiple-choice questions, respond with a single uppercase letter (A, B, C, etc.).
- For numerical or calculated answers, respond with a number.

Your final answer must be enclosed in an <answer> section, like this:
<answer>
A single letter or number
</answer>

## IMPORTANT RULES
- You MUST include the <answer> section.
- You may include reasoning BEFORE the <answer> section, but not after.
- Your response MUST end with the </answer> tag.
- The content INSIDE <answer> should be only a letter or number - nothing else.
"""
    return [('user', [prompt])]

bot = LLMInference('gemini/gemini-1.5-flash', api_key='<TOKEN>')

files = [
    
]

for file in files:
    reconsider = False
    if 'o4' in os.path.basename(file) or 'gpt' in os.path.basename(file):
        reconsider = True

    with open(file) as rf:
        data = json.load(rf)

    correct = []
    failed = []
    pbar = tqdm(data)

    for i in pbar:
        try:
            if str(i['answer']).strip().lower() == i['bot_answer'].strip().lower():
                correct.append(i)
            elif reconsider:
                try:
                    response = bot(create_conversation(i['question'], i['bot_answer']))
                    answer = response['content'][0]['text'].split('<answer>')[-1].split('</answer>')[0].strip()
                except:
                    failed.append(i)
                    continue

                time.sleep(6)

                if str(i['answer']).strip().lower() == answer.lower():
                    correct.append({**i, 'modified_answer': answer})
                else:
                    failed.append({**i, 'modified_answer': answer})
            else:
                failed.append(i)
        finally:
            pbar.set_description(f"✅ {len(correct)} ❌ {len(failed)}")

    print('OK', len(correct), 'Failed', len(failed))

    alls = correct + failed
    os.makedirs('./tmp', exist_ok=True)
    with open(f'./tmp/{os.path.basename(file)}', 'w') as wf:
        json.dump(alls, wf, indent=4)
