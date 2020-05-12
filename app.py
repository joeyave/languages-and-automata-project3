from infix_to_postfix_regex import get_postfix_regex
from regex import Regex


def main():
    regex_str = input("input regex: ")
    regex_str = get_postfix_regex(regex_str)
    regex = Regex(regex_str)
    regex.convert_to_nfa("nfa.json")


if __name__ == "__main__":
    main()
