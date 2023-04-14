import pytest
from src.pycrust import transpile_python_to_rust


def test_transpile_python_to_rust():
    py_code = "print('Hello, world!')"
    api_key = "my-api-key"
    rust_file = "output.rs"
    transpile_python_to_rust(py_code, api_key, rust_file)
    with open(rust_file, "r") as f:
        rust_code = f.read()
    assert "println!(\"Hello, world!\");" in rust_code
