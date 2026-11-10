from lark.exceptions import UnexpectedInput

import analyzer


def get_error(text):
    try:
        analyzer._PARSER.parse(text)
    except UnexpectedInput as exc:
        return exc
    raise AssertionError(f"{text!r} was expected to fail")


def test_describe_expected():
    assert analyzer._describe_expected({"DIGIT"}) == "digit"
    assert analyzer._describe_expected({"COMMA", "RPAR"}) == "',' or ')'"
    assert analyzer._describe_expected({"$END"}) == "end of string"


def test_is_valid():
    assert analyzer._is_valid("abc=12")
    assert analyzer._is_valid("abc=(def=34),xyz=00")
    assert not analyzer._is_valid("abc=1")
    assert not analyzer._is_valid("abc=12,")


def test_format_error_wrong_char():
    message = analyzer.format_error(get_error("abc=(def=1x"), "abc=(def=1x")
    assert "position 10" in message
    assert "Expected: digit" in message
    assert "Got:      'x'" in message


def test_format_error_end_of_string():
    message = analyzer.format_error(get_error("abc=12,"), "abc=12,")
    assert "position 7" in message
    assert "Expected: 3-letter name" in message
    assert "Got:      end of string" in message


def test_format_error_could_end_here():
    message = analyzer.format_error(get_error("abc=12x"), "abc=12x")
    assert "Expected: end of string or ','" in message


def test_describe_rules():
    rules = analyzer._describe_rules(get_error("abc=(def=1x").state)
    assert rules == ["<param> ::= <name> '=' <digit> • <digit>"]


def test_check():
    assert analyzer.check("abc=12") == (True, analyzer.OK_MESSAGE)
    assert analyzer.check("") == (False, analyzer.EMPTY_MESSAGE)
    ok, message = analyzer.check("ab=12")
    assert not ok and "position 0" in message


if __name__ == "__main__":
    tests = [f for name, f in sorted(globals().items()) if name.startswith("test_")]
    failed = 0
    for test in tests:
        try:
            test()
            print(f"[PASS] {test.__name__}")
        except AssertionError as exc:
            failed += 1
            print(f"[FAIL] {test.__name__}: {exc}")
    print(f"\nFailed: {failed} of {len(tests)}")
