import re

from typing import Type
from collections import defaultdict, deque


def normalize_str(value: str) -> str:
    """Normalize a string object.

    Args:
        value (str): String object.

    Returns:
        str: The normalized string object.
    """

    return value.strip()


def remove_html_content(value: str) -> str:
    """Returns a new string without HTML tags and their content.

    Args:
        value (str): String object.

    Returns:
        str: _description_
    """

    p = re.compile(r"<.*>.*<.*?>")

    return p.sub("", value)


def remove_parenthesis_content(value: str) -> str:
    """Returns a new string without parenthesis and their content.
    It will only remove valid parenthesis pairs. Time complexity is O(n) even in the worst case.

    Args:
        value (str): String object.

    Returns:
        str: The new string.
    """

    st = deque([""])
    count = 0

    for ch in value:
        if ch == "(":
            count += 1
            st.append("")
        elif ch == ")" and count > 0:
            st.pop()
            count -= 1
            continue

        st[-1] += ch

    # Fix whitespaces by prevention
    out = "".join(st)
    out = " ".join(out.split())

    return out


def create_recursive_dict(t: Type, depth: int) -> dict:
    """Returns a recursive defaultdict with a custom depth.
    For example, a dictionnary with a depth of 3 could be represented like below.

    {
      one: {
        two: {
          three: 3,
        },
    }

    Args:
        t (Type): The leaf dictionnary value type.
        depth (int): The depth.

    Returns:
        dict: The created dictionnary.
    """

    if depth <= 1:
        return defaultdict(t)

    return defaultdict(lambda: create_recursive_dict(t, depth - 1))
