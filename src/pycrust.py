import openai
import re
import os
import argparse


def transpile_python_to_rust(py_code, api_key, rust_file):
    openai.api_key = api_key
    engine_id = 'text-davinci-002'
    prompt = f"Transpile the following Python code into Rust:\n\n{py_code}\n\nRust code:"
    response = openai.Completion.create(
        engine=engine_id,
        prompt=prompt,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.5,
    )
    rust_code = response.choices[0].text
    # Replace numpy with ndarray
    rust_code = re.sub(r"numpy", "ndarray", rust_code)
    with open(rust_file, "w") as f:
        f.write(rust_code)
    missing_libs = []
    for import_stmt in re.findall(r"use (.+);", rust_code):
        if import_stmt not in ["std", "core"]:
            missing_libs.append(import_stmt)
    with open("missing_libs.txt", "w") as f:
        f.write("\n".join(missing_libs))
    if missing_libs:
        print("Some Rust libraries are missing. Please download them using `cargo`.")


def main():
    parser = argparse.ArgumentParser(
        description='Transpile Python code to Rust')
    parser.add_argument('input_file', type=str,
                        help='path to input Python file')
    parser.add_argument('--api_key', type=str, help='OpenAI API key')
    args = parser.parse_args()
    if args.api_key is None:
        try:
            with open('.openai', 'r') as f:
                args.api_key = f.read().strip()
        except FileNotFoundError:
            args.api_key = os.environ.get('OPENAI_API_KEY')
        if args.api_key is None:
            print(
                'Please set the OPENAI_API_KEY environment variable or provide it using the --api_key flag.')
            exit(1)
    rust_file = os.path.splitext(args.input_file)[0] + '.rs'
    with open(args.input_file, 'r') as f:
        py_code = f.read()
    transpile_python_to_rust(py_code, args.api_key, rust_file)


if __name__ == '__main__':
    main()
