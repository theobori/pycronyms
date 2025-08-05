import re

from typing import Type, Any, Dict
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
        str: The new string.
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

    out = "".join(st)

    # Remove whitespaces by prevention
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


# See https://stackoverflow.com/a/19637185
def is_sortable(obj: Any) -> bool:
    """Returns is a Python object is sortable.

    Args:
        obj (Any): The object.

    Returns:
        bool: The answer.
    """

    cls = obj.__class__

    return cls.__lt__ != object.__lt__ or cls.__gt__ != object.__gt__


def sorted_recursive(obj: Any, *args: tuple, **kwargs: Dict[str, Any]) -> Any:
    """Recursively sort dict and list. To sort the objects, the built-in function `sorted`
    is used. You can pass argument to the `sorted` function with the parameters `*args` et `**kwargs`.

    Args:
        obj (Any): Any Python object.

    Returns:
        Any: The sorted value.
    """

    def inner(obj: Any) -> Any:
        if isinstance(obj, list):
            # It does the job, to handle every case, maybe catching exception would be the simplest solution
            for el in obj:
                if is_sortable(el) is False or isinstance(el, dict):
                    break
            else:
                obj = sorted(obj, *args, **kwargs)

            for i in range(len(obj)):
                obj[i] = inner(obj[i])

        elif isinstance(obj, dict):
            obj = dict(sorted(obj.items(), *args, **kwargs))

            for k, v in obj.items():
                obj[k] = inner(v)
        else:
            return obj

        return obj

    sorted_obj = inner(obj)

    return sorted_obj
