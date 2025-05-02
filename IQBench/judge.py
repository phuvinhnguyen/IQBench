from FlowDesign.processor import ThinkProcessor
from FlowDesign.litellm import LLMInference

class LLMJudge(ThinkProcessor):
    modifies = ('judge_think', 'judge_evidence', 'judge_answer', 'judge_model')

    PROMPT = '''# Given the following information:

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
<think>
Compare the VLM's reasoning to the ground truth reasoning. Is the logical structure similar? Are the key steps present? Does the reasoning correctly support the final answer? Mention any discrepancies or alignments.
</think>
<evidence>
If the VLM's reasoning is flawed or deviates from the ground truth, provide specific parts of the VLM reasoning that are incorrect, missing, or misleading. If correct, explain why the reasoning is logically valid.
</evidence>
<answer>
Return 1 if the VLM's reasoning is correct and aligns with the ground truth, otherwise return 0.
</answer>
'''

    def __init__(self, bot: LLMInference):
        super().__init__()
        self.bot = bot

    def extract_answer(self, text):
        try:
            think, evidence = text.split('<think>')[-1].split('</think>')
            evidence, answer = evidence.split('<evidence>')[-1].split('</evidence>')
            answer = answer.split('<answer>')[-1].split('</answer>')[0]
            return think.strip(), evidence.strip(), answer.strip()
        except Exception as e:
            print(e)
            return '', '', ''

    def process(self, think, bot_answer, answer, pattern, images):
        inputs = [[('user', [
            # pil_to_tempfile_path(_images),
            self.PROMPT.format(
                think=_think,
                bot_answer=_bot_answer,
                answer=_answer,
                pattern=_pattern
            )])] for _think, _bot_answer, _answer, _pattern, _images
                in zip(think, bot_answer, answer, pattern, images)]
        
        ## Handle text only does not need to separate model for batch processing
        # if 'gpt' not in self.bot.model and 'claude' not in self.bot.model:
        results = self.bot.run(inputs, batch=True)
        # else:
        #     results = [self.bot.run(inp, batch=False) for inp in inputs]
            
        answers = [self.extract_answer(result['content'][0]['text']) for result in results]
        return [i[0] for i in answers], [i[1] for i in answers], [i[2] for i in answers], [self.bot.model for _ in answers]
