from FlowDesign.processor import ThinkProcessor
from FlowDesign.litellm import LLMInference
import tempfile, re, os, pickle
from tqdm import tqdm
import litellm
from datetime import datetime
# litellm._turn_on_debug()

def pil_to_tempfile_path(pil_img, suffix=".png"):
    if isinstance(pil_img, str): return pil_img
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    pil_img.save(temp_file.name)
    return temp_file.name

class AnswerQuizz(ThinkProcessor):
    modifies = ('full_answer', 'think', 'bot_answer', 'model_name')

    PROMPT = '''Given the image, answer the following question: {question}
Your answer must strictly follow this format:
<reason>
Your step-by-step answer showing your process solving the problem
</reason>
<answer>
Your final answer
- For multiple choice, answer with a letter (A, B, C, etc.).
- For numerical or computed answers, answer with a number.
</answer>

**IMPORTANT**
- your answer must include <answer> section
- your answer must start with <answer> and end with </answer>'''

    def __init__(self, bot: LLMInference, cache=None):
        super().__init__()
        self.cache = cache

        self.bot = bot
        self.unbatch = ['o1', 'o3', 'gpt', 'claude']

    def extract_answer(self, text):
        try:
            try: text = text['content'][0]['text']
            except: text = ''
            think_match = re.search(r"<reason>(.*?)</reason>", text, re.DOTALL)
            answer_match = re.search(r"<answer>(.*?)</answer>", text, re.DOTALL)

            think = think_match.group(1).strip() if think_match else ''
            answer = answer_match.group(1).strip() if answer_match else ''

            return text, think, answer
        except Exception as e:
            raise e

    def process(self, images, questions):
        inputs = [[('user', [self.PROMPT.format(question=question), pil_to_tempfile_path(image)])] for image, question in zip(images, questions)]

        handle_batch = True
        for i in self.unbatch:
            if i in self.bot.model: handle_batch = False

        if handle_batch:
            results = self.bot.run(inputs, batch=True)
            cost = self.bot.cost
        else:
            filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            cost = 0
            if self.cache != None:
                with open(self.cache, 'rb') as rb:
                    results = pickle.load(rb)
            else: results = [{'error': 'not run'}] * len(inputs)
            with tqdm(inputs, desc="Running") as pbar:
                for i, (inp, res) in enumerate(zip(pbar, results)):
                    if res['error'] == None: continue

                    tmp_answer = self.bot.run(inp, batch=False)
                    results[i] = tmp_answer
                    cost += self.bot.cost
                    pbar.set_postfix({"cost": f"{cost:.4f}"})
                    with open(os.path.normpath(os.path.join(os.path.dirname(__file__), f'../tmp/{filename}.pickle')), 'wb') as wf:
                        pickle.dump(results, wf)
        answers = [self.extract_answer(result) for result in results]
        return [i[0] for i in answers], [i[1] for i in answers], [i[2] for i in answers], [self.bot.model for _ in answers]
