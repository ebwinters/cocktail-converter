import sys
import os
import argparse
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def parse_args():
    parser = argparse.ArgumentParser(description="Convert cocktail recipes to markdown format")
    parser.add_argument("recipe", nargs="?", help="The recipe string or - for stdin")
    parser.add_argument("-f", "--file", help="Input file containing the recipe")
    parser.add_argument("-o", "--output", help="Output markdown file (default: recipe-name.md)")
    return parser.parse_args()

def get_recipe_text(args):
    if args.file:
        with open(args.file, 'r') as f:
            return f.read()
    elif args.recipe == '-':
        return sys.stdin.read()
    elif args.recipe:
        return args.recipe
    else:
        print("Error: Please provide a recipe via argument, file, or stdin")
        sys.exit(1)

def generate_markdown(recipe_text):
    prompt_path = os.path.join(os.path.dirname(__file__), "prompt.md")
    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt_template = f.read()
    
    prompt = f"{prompt_template}\n\n{recipe_text}"

    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that converts cocktail recipes into markdown format using a specific template."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        sys.exit(1)

def save_markdown(markdown_content, output_path=None, recipe_name=None):
    if not output_path:
        recipe_name = recipe_name.replace(" ", "-").lower()
        output_path = f"{recipe_name}.md"
    
    with open(output_path, 'w') as f:
        f.write(markdown_content)
    
    print(f"Markdown saved to {output_path}")

def main():
    args = parse_args()
    recipe_text = get_recipe_text(args)
    
    print("Converting recipe")
    markdown_content = generate_markdown(recipe_text)
    
    output_path = args.output if args.output else None
    save_markdown(markdown_content, output_path, "recipe")

if __name__ == "__main__":
    main()