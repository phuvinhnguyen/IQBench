from IQBench.judge import LLMJudge
from FlowDesign.litellm import LLMInference
import argparse
import json

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Run IQBench evaluation with specified LLM model.')
    
    # Required arguments
    parser.add_argument('--input_file', type=str, required=True,
                      help='Path to the input JSON file containing VLM\'s answer')
    parser.add_argument('--output_file', type=str, required=True,
                      help='Path to save the output JSON file with answers')
    
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
    agent = LLMJudge(bot)
    
    # Load and process data
    try:
        with open(args.input_file) as rf:
            need_to_run_data = []
            run_successfully_data = []
            data = json.load(rf)[:args.num_samples]
            for item in data:
                if 'judge_think' not in item or item['judge_think'] == '':
                    item['judge_think'] = ''
                    item['judge_evidence'] = ''
                    item['judge_answer'] = ''
                    item['judge_model'] = ''
                    need_to_run_data.append(item)
                else:
                    run_successfully_data.append(item)
        
        # Prepare inputs and get outputs
        inputs = {k: [i[k] for i in need_to_run_data] for k in need_to_run_data[0].keys()}
        outputs = agent(inputs)
        print('Cost:', agent.bot.cost)
        
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
        raise e

if __name__ == "__main__":
    main()