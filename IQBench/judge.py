from FlowDesign.processor import ThinkProcessor
from FlowDesign.litellm import LLMInference
import re

class LLMJudge(ThinkProcessor):
    modifies = ('judge_think', 'judge_evidence', 'judge_answer', 'judge_model')

    PROMPT = '''# Given the following information:

## Question (You will not able to see the image as you should only compare the groud truth thinking and VLM's reasoning)
{question}

## Ground Truth Reasoning (GT Reasoning)
{pattern}

## Ground Truth Final Answer (GT Answer)
{answer}

## VLM's Reasoning (VLM Reasoning)
{think}

## VLM's Final Answer (VLM Answer)
{bot_answer}

## Task
Your task is to analyze whether the VLM's reasoning is logically sound and consistent with the ground truth reasoning, and whether it leads to the correct final answer. Base your judgment on reasoning accuracy, logical consistency, and whether the intermediate steps support the final conclusion.

Respond strictly in the following format:
<reason>
Compare the VLM's reasoning to the ground truth reasoning. Is the logical structure similar? Are the key steps present? Does the reasoning correctly support the final answer? Mention any discrepancies or alignments.
</reason>
<evidence>
If the VLM's reasoning is flawed or deviates from the ground truth, provide specific parts of the VLM reasoning that are incorrect, missing, or misleading. If correct, explain why the reasoning is logically valid.
</evidence>
<answer>
Return 1 if the VLM's reasoning is correct and aligns with the ground truth, otherwise return 0.
</answer>

**IMPORTANT**
- your answer must include <answer> section
- contents inside the <answer> section must be just 1 or 0
- your answer must start with <reason> and end with </answer>
'''

    def __init__(self, bot: LLMInference):
        super().__init__()
        self.bot = bot
        
    def extract_answer(self, text):
        try:
            try: text = text['content'][0]['text']
            except: print(text)
            think_match = re.search(r"<reason>(.*?)</reason>", text, re.DOTALL)
            evidence_match = re.search(r"<evidence>(.*?)</evidence>", text, re.DOTALL)
            answer_match = re.search(r"<answer>(.*?)</answer>", text, re.DOTALL)

            think = think_match.group(1).strip() if think_match else ''
            evidence = evidence_match.group(1).strip() if evidence_match else ''
            answer = answer_match.group(1).strip() if answer_match else ''

            return think, evidence, answer
        except:
            return '', '', ''


    def process(self, question, think, bot_answer, answer, pattern, local_path):
        inputs = [[('user', [
            # pil_to_tempfile_path(_images),
            self.PROMPT.format(
                question=_question,
                think=_think,
                bot_answer=_bot_answer,
                answer=_answer,
                pattern=_pattern
            )])] for _question, _think, _bot_answer, _answer, _pattern, _images
                in zip(question, think, bot_answer, answer, pattern, local_path)]
        
        results = self.bot.run(inputs, batch=True)
            
        answers = [self.extract_answer(result) for result in results]
        return [i[0] for i in answers], [i[1] for i in answers], [i[2] for i in answers], [self.bot.model for _ in answers]
