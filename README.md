# Pinky Programming Language

A simple programming language interpreter written in Python.

This has been built purely for educational purposes so that I can better understand how compilers work.

## Overview

Pinky is a straightforward programming language implementation that includes:

- Basic arithmetic operations
- Variables and assignments
- Control flow (if statements, loops)
- Functions
- Integer, float, boolean and string data types

## Getting Started

1. Clone this repository
2. Make sure you have Python 3 installed
3. Run a Pinky script using: `make run` or `python3 pinky.py your_script.pinky`

## Project Structure

The interpreter is split into several key files:

- `pinky.py` - The main entry point that runs the interpreter
- `parser.py` - Parses tokens into an abstract syntax tree (AST)
- `tokens.py` - Defines the language's tokens and token types
- `model.py` - Contains the AST node classes and data types
- `utils.py` - Helper functions and utilities
