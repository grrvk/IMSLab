import sys

from lark import Lark
from lark.exceptions import UnexpectedCharacters, UnexpectedEOF, UnexpectedToken

GRAMMAR = r"""
start: param_list
param_list: param ("," param)*
param: NAME "=" DIGIT DIGIT
     | NAME "=" "(" param_list ")"
NAME: /[a-zA-Z]{3}/
DIGIT: /[0-9]/
"""

OK_MESSAGE = "String is valid"
EMPTY_MESSAGE = "Error: empty string"
END = "end of string"

TERMINAL_NAMES = {
    "NAME": "3-letter name",
    "DIGIT": "digit",
    "EQUAL": "'='",
    "COMMA": "','",
    "LPAR": "'('",
    "RPAR": "')'",
    "$END": END,
}

SYMBOL_NAMES = {
    "param_list": "<param-list>",
    "param": "<param>",
    "NAME": "<name>",
    "DIGIT": "<digit>",
    "EQUAL": "'='",
    "COMMA": "','",
    "LPAR": "'('",
    "RPAR": "')'",
}

_PARSER = Lark(GRAMMAR, parser="earley")


def _is_valid(text: str) -> bool:
    try:
        _PARSER.parse(text)
        return True
    except (UnexpectedCharacters, UnexpectedToken, UnexpectedEOF):
        return False


def _describe_rules(state) -> list[str]:
    lines = []
    for item in state or []:
        if not isinstance(item, tuple):
            continue
        rule, ptr = item
        symbols = [SYMBOL_NAMES.get(s.name, s.name) for s in rule.expansion]
        symbols.insert(ptr, "•")
        body = " ".join(symbols)
        if rule.origin.name.startswith("__param_list"):
            line = f"<param-list> ::= <param> {{ {body} }}"
        else:
            line = f"{SYMBOL_NAMES.get(rule.origin.name, rule.origin.name)} ::= {body}"
        if line not in lines:
            lines.append(line)
    return sorted(lines)


def _describe_expected(terminals) -> str:
    names = []
    for terminal in sorted(terminals):
        name = TERMINAL_NAMES.get(terminal, terminal)
        if name not in names:
            names.append(name)
    return " or ".join(names)


def format_error(exc, text: str) -> str:
    if isinstance(exc, UnexpectedCharacters):
        position = exc.pos_in_stream
        got = f"'{exc.char}'"
        expected = set(exc.allowed)
        if position > 0 and _is_valid(text[:position]):
            expected.add("$END")
    elif isinstance(exc, UnexpectedToken):
        expected = exc.expected
        if exc.token.type == "$END":
            position = len(text)
            got = END
        else:
            position = exc.pos_in_stream
            got = f"'{exc.token.value}'"
    elif isinstance(exc, UnexpectedEOF):
        position = len(text)
        got = END
        expected = exc.expected
    else:
        return f"Error: {exc}"

    message = (
        f"Error at position {position}\n"
        f"  Expected: {_describe_expected(expected)}\n"
        f"  Got:      {got}"
    )
    rules = _describe_rules(getattr(exc, "state", None))
    if rules:
        message += "\n  Rule:     " + "\n            ".join(rules)
    return message


def check(text: str) -> tuple[bool, str]:
    if not text:
        return False, EMPTY_MESSAGE
    try:
        _PARSER.parse(text)
    except (UnexpectedCharacters, UnexpectedToken, UnexpectedEOF) as exc:
        return False, format_error(exc, text)
    return True, OK_MESSAGE


def main() -> None:
    if len(sys.argv) > 1:
        print(check(sys.argv[1])[1])
        return
    while True:
        try:
            line = input("Enter a string (empty to quit): ")
        except EOFError:
            break
        if not line:
            break
        print(check(line)[1])


if __name__ == "__main__":
    main()