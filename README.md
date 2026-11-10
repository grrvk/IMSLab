# Lab: syntax analyzer

Parameter-list analyzer using Lark (Earley parser).

## Install
```
pip install -r requirements.txt
```

## Run
```
python analyzer.py "abc=(def=34)"   # check a single string
python analyzer.py                   # interactive; empty line quits
python check_file.py input.txt       # check every line of a text file
```

## Tests
```
python unit_tests.py
```
Unit tests for each function of `analyzer.py`.

## Grammar
```
<param-list> ::= <param> {',' <param>}
<param>      ::= <name> '=' <digit> <digit>
               | <name> '=' '(' <param-list> ')'
<name>       ::= <letter> <letter> <letter>
```