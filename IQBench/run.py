from FlowDesign.processor import ThinkProcessor
from FlowDesign.litellm import LLMInference
import tempfile

def pil_to_tempfile_path(pil_img, suffix=".png"):
    if isinstance(pil_img, str): return pil_img
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    pil_img.save(temp_file.name)
    return temp_file.name

class AnswerQuizz(ThinkProcessor):
    modifies = ('full_answer', 'think', 'bot_answer', 'model_name')
    PROMPT = '''Given the image, answer the following question: {question}
Your answer must strictly follow this format:
<think>
Your step-by-step thinking to find the final answer of the problem
</think>
<answer>
Your final answer for the question
</answer>'''

    def __init__(self, bot: LLMInference):
        super().__init__()
        self.bot = bot

    def extract_answer(self, text):
        try:
            think, answer = text.split('<think>')[-1].split('</think>')
            answer = answer.split('<answer>')[-1].split('</answer>')[0].strip()
            return text, think.strip(), answer
        except Exception as e:
            print(e)
            return '', '', ''

    def process(self, images, questions):
        inputs = [[('user', [pil_to_tempfile_path(image), self.PROMPT.format(question=question)])] for image, question in zip(images, questions)]
        if 'gpt' not in self.bot.model:
            results = self.bot.run(inputs, batch=True)
        else:
            results = [self.bot.run(inp, batch=False) for inp in inputs]
        answers = [self.extract_answer(result['content'][0]['text']) for result in results]
        return [i[0] for i in answers], [i[1] for i in answers], [i[2] for i in answers], [self.bot.model for _ in answers]
