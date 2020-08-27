import re
from PyQt5.QtWidgets import QWidget, QGridLayout


def fit_in_range(value, min_max_range):
    if value < min(min_max_range):
        value = min(min_max_range)
    elif value > max(min_max_range):
        value = max(min_max_range)
    return value


def disable_all_widgets(element):
    children = element.children()
    for child in children:
        if isinstance(child, QWidget):
            child.setDisabled(True)
        elif isinstance(child, QGridLayout):
            disable_all_widgets(child)


def convert_to_numeric(str_value: str):
    """Convert a string to float (if there is a "." in the string) or to integer, if possible."""
    if re.match("^\d+\.\d+$", str_value):
        return float(str_value)
    elif re.match("^\d+$", str_value):
        return int(str_value)
    else:
        return str_value
