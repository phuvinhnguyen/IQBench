# IQBench

This package evaluate VLMs' reasoning ability on IQ tests

## Installation

This package depends on FlowDesign, which can be installed with:
```bash
pip install git+https://github.com/phuvinhnguyen/FlowDesign.git
```

After that, you can clone this repo
```bash
git clone git+https://github.com/phuvinhnguyen/IQBench.git
cd IQBench
```

## Usage
### Download data
```bash
# go to folder: IQBench/data
cd data
python process.py
```
### Get VLM's result on downloaded data
You can run this command to the output file again to handle samples that VLM was failed to run  
This command will evaluate gemini-1.5-flash on our 500 samples
```bash
# go to folder: IQBench
python -m experiments.evaluate --input_file ./data/questions_processed.json \
--output_file ./results.json \
--model_name gemini/gemini-1.5-flash \
--api_token <YOUR_TOKEN> \
--num_samples 500
```

### Get LLM's judgement on downloaded data
You can run this command to the output file again to handle samples that VLM was failed to run  
This command will evaluate gemini-1.5-flash on our 500 samples
```bash
# go to folder: IQBench
# input file is the output file from the previous step
python -m experiments.llmjudge --input_file ./results.json \
--output_file ./results_llmjudge.json \
--model_name gemini/gemini-1.5-flash \
--api_token <YOUR_TOKEN> \
--num_samples 500
```

### Output explain

#### Metadata
- **`id`**: Unique sample ID  
- **`file_name`**: Original image file name  
- **`online_link`**: URL to online image source  
- **`source`**: Source of the question (if collected)  
- **`topic`**: Topic/category of the image  
- **`author`**: Author of the sample  

####️ Image Info
- **`link`**: Renamed local image file  
- **`local_path` / `images`**: Local path to downloaded image  

#### QA Content
- **`question` / `questions`**: Question related to the image  
- **`answer`**: Ground-truth answer (label)  
- **`pattern`**: Ground-truth reasoning/explanation  

#### Status
- **`ready`**: Whether sample is ready for evaluation (`1` or `0`)  

#### VLM Output
- **`think`**: VLM's reasoning before answering  
- **`bot_answer`**: VLM's final answer  
- **`full_answer`**: Full generated response  
- **`model_name`**: Name of evaluated VLM  

#### Judge LLM
- **`judge_think`**: Judgment on VLM’s reasoning  
- **`judge_evidence`**: Supporting or refuting evidence  
- **`judge_answer`**: Final judgment (`1` = correct, `0` = incorrect)  
- **`judge_model`**: LLM used for judgment  

```json
{
    "id": 1,
    "file_name": "C1.png",
    "online_link": "https://...",
    "topic": "Mechanical Deductive Reasoning Test",
    "author": "anonymous",
    "question": "The smaller gear makes 36 revolutions by the time the larger ones make 18.\nIf the smaller gear makes 56 revolutions, how many turns will the larger one make?\nA. 24 \nB. 26 \nC. 28 \nD. 25 \n",
    "answer": "C",
    "pattern": "Explanation:\n\\[\nu = \\frac{18}{36} = 0.5\n\\]\n\\[\nn_{\\text{larger}} = u \\cdot 56 = 28\n\\]\n",
    "source": "https://...",
    "ready": 1,
    "link": "image_001.png",
    "local_path": "path/to/image_001.png",
    "images": "path/to/image_001.png",
    "questions": "The smaller gear makes 36 revolutions by the time the larger ones make 18.\nIf the smaller gear makes 56 revolutions, how many turns will the larger one make?\nA. 24 \nB. 26 \nC. 28 \nD. 25 \n",
    "bot_answer": "C. 28",
    "full_answer": "<think>\nLet $n_s$ be the number of revolutions of the smaller gear and $n_l$ be the number of revolutions of the larger gear.\nWe are given that when the smaller gear makes 36 revolutions, the larger gear makes 18 revolutions.\nThis can be written as a ratio:\n$\\frac{n_s}{n_l} = \\frac{36}{18} = 2$\nThis means that the smaller gear makes twice as many revolutions as the larger gear.\nWe can write this relationship as:\n$n_s = 2n_l$\nWe are given that the smaller gear makes 56 revolutions, so $n_s = 56$.\nWe can find the number of revolutions of the larger gear by substituting $n_s = 56$ into the equation:\n$56 = 2n_l$\n$n_l = \\frac{56}{2} = 28$\nTherefore, the larger gear will make 28 turns.\n\n</think>\n<answer>\nC. 28\n</answer>",
    "think": "Let $n_s$ be the number of revolutions of the smaller gear and $n_l$ be the number of revolutions of the larger gear.\nWe are given that when the smaller gear makes 36 revolutions, the larger gear makes 18 revolutions.\nThis can be written as a ratio:\n$\\frac{n_s}{n_l} = \\frac{36}{18} = 2$\nThis means that the smaller gear makes twice as many revolutions as the larger gear.\nWe can write this relationship as:\n$n_s = 2n_l$\nWe are given that the smaller gear makes 56 revolutions, so $n_s = 56$.\nWe can find the number of revolutions of the larger gear by substituting $n_s = 56$ into the equation:\n$56 = 2n_l$\n$n_l = \\frac{56}{2} = 28$\nTherefore, the larger gear will make 28 turns.",
    "model_name": "gemini/gemini-1.5-flash",
    "judge_think": "The VLM's reasoning and the ground truth reasoning both arrive at the same correct answer (28), but they approach the problem from slightly different perspectives.  The ground truth uses a ratio directly derived from the given data (18/36) to calculate a scaling factor (0.5), then applies that factor to the new number of revolutions (56). The VLM, on the other hand, establishes a direct relationship between the number of revolutions of the smaller and larger gears ($n_s = 2n_l$), then solves for the number of revolutions of the larger gear given the number of revolutions of the smaller gear.  Both methods are logically sound and arrive at the same correct conclusion.  The key steps \u2013 establishing the relationship between the gears' revolutions and using this relationship to find the unknown \u2013 are present in both.  There are no discrepancies in the final answer.",
    "judge_evidence": "The VLM's reasoning is logically valid.  It correctly identifies the inverse proportional relationship between the number of revolutions of the smaller and larger gears.  The equation $n_s = 2n_l$ accurately reflects this relationship, derived from the initial data. The subsequent steps of substituting $n_s = 56$ and solving for $n_l$ are mathematically sound and lead to the correct answer.  The ground truth implicitly uses the same relationship, but expresses it through a ratio and scaling factor. Both methods are equivalent and lead to the same result.",
    "judge_answer": "1",
    "judge_model": "gemini/gemini-1.5-flash"
}
```