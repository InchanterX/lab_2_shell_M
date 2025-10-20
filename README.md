


# Project structure

 <pre>
    .
    ├── lab_calcM2
    │   ├── src/                               # Source code
    │       ├── __init__.py                    #
    |       ├── calculator.py                  # Calculate the expression in RPN
    │       ├── constants.py                   # Constants used across the project
    │       ├── facade.py                      # Gather all the parts into one class
    │       ├── main.py                        # It is a main file!
    │       ├── parser.py                      # Convert tokens to the RPN
    │       ├── tokenizer.py                   # Tokenize the entered string
    │   ├── tests/                             # Unit tests
    │       ├── test_calculator.py             # Test calculations process
    │       ├── test_facade.py                 # Test how classes work together
    │       ├── test_parser.py                 # Test conversion to the RPN
    │       ├── test_tokenizer.py              # Tests expression tokenization
    │   ├── uv.lock                            # зависимости проекта
    │   ├── .gitignore                         # git ignore files
    │   ├── .pre-commit-config.yaml            # Code-style check
    │   ├── requirements.txt                   # Dependencies
    │   ├── README.md                          # Laboratory report with a project description
</pre>

# Assumptions
1. White spaces are insignificant
2. It is prohibited to place more than two unary operations in a row
3. All "raise"s in programme use basic error classes with specific output messages
4. Float numbers can be wrote both with . or ,

# How it works?
## Set up
To use calculator you need to download it.
Then you can run it from the project root with your terminal with this command:
```
python -m src.main
```
To activate tests use:
```
python -m pytest
```

## Users input
**Main** file contains users interface that appear in the terminal. Programme suggest to enter an expression. There is several options for the user here:
1. User can enter an expression.
   1. If expression is valid, programme will return **correct** result.
   2. If expression is invalid, programme will return a error with explanation of it.
2. User can enter command exit|quit|выход|выйти and finish the programme execution.

## Abilities and restrictions
Calculator is able to work with such operations as +, -, /, *, //, %, **, brackets and unary +,-.
It works with integer and float numbers, but it leads to some basic restrictions:
- Division by zero is impossible for /, // and %.
- // and % do not work with float numbers.

## How it is implemented
### Tokenizer
First step from the expression to the result is tokenization. Eponymous class split the string via regular expressions into a list of tokens. Every token contains 3 variables: type, value and pos.
- Type describe which group of elements this token pertains. It can be NUMBER, OPERATIONS, LBRACKET, RBRACKET and UNKNOWN.
- Value contains... value of the token. It can be in any data type.
- Pos (position) save initial position and used in errors explanations on the program's low levels such as a tokenizer.

### Parser
Parser works with a result of tokenizers work. It convert the list of tokens in basic human-readable form into RPN (Reversed Poland Notation) to count it in the next part of the programme. It use stack and process tokens one by one.
- If it encounter a number, it just add it to stack.
- If it encounter an operation, it process it - check it for priorities and then add it to the stack on the right place.
- If it is a bracket it process it to make a correct order of operations. Brackets their self are not added to the stack.

### Calculator
When RPN is ready it is calculating via calculator. It just count the result. It detect unary operations and if it find any mistakes or prohibited combinations it raise a error.

### Facade
Facade gather all the classes in one for a simpler usage without need of righting and importing 3 classes every time and everywhere.

---
And here we are again in the main file with a result for our expression.

# Killer feature:
```
casino_on
```
