from IQBench.run import AnswerQuizz
from FlowDesign.litellm import LLMInference
import argparse
import json

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Run IQBench evaluation with specified LLM model.')
    
    # Required arguments
    parser.add_argument('--input_file', type=str, required=True,
                      help='Path to the input JSON file containing questions')
    parser.add_argument('--output_file', type=str, required=True,
                      help='Path to save the output JSON file with answers')
    parser.add_argument('--cache', type=str, default=None,
                      help='path to cache file (pickle)')
    
    # Optional arguments with defaults
    parser.add_argument('--model_name', type=str, default='gemini/gemini-1.5-flash',
                      help='Name of the LLM model to use (default: gemini/gemini-1.5-flash)')
    parser.add_argument('--api_token', type=str, required=True,
                      help='API token for the LLM service')
    parser.add_argument('--num_samples', type=int, default=2,
                      help='Number of samples to process (default: 2)')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Initialize components
    bot = LLMInference(args.model_name, api_key=args.api_token)
    agent = AnswerQuizz(bot, cache=args.cache)
    
    # Load and process data
    try:
        with open(args.input_file) as rf:
            need_to_run_data = []
            run_successfully_data = []
            data = [i for i in json.load(rf) if 'Anagram' in i['topic']][:args.num_samples]
            for item in data:
                if 'full_answer' not in item or item['full_answer'] == '':
                    # not yet run
                    item['images'] = item['local_path']
                    item['questions'] = item['question']
                    item['bot_answer'] = ''
                    item['think'] = ''
                    item['full_answer'] = ''
                    item['model_name'] = ''
                    need_to_run_data.append(item)
                else:
                    run_successfully_data.append(item)
        
        # Prepare inputs and get outputs
        inputs = {k: [i[k] for i in need_to_run_data] for k in need_to_run_data[0].keys()}
        outputs = agent(inputs)
        
        # Format output
        output = [{k: v[i] for k, v in outputs.items()} 
                 for i in range(len(list(outputs.values())[0]))] + run_successfully_data
        
        # Save results
        with open(args.output_file, 'w') as wf:
            json.dump(output, wf, indent=4)
        
        print(f"Successfully processed {len(output)} samples. Results saved to {args.output_file}")
    
    except FileNotFoundError:
        print(f"Error: Input file not found at {args.input_file}")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {args.input_file}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()