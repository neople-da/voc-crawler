import re

def multireplace(string, replacements: dict):
    for pattern, toReplce in replacements.items():
        string = re.sub(pattern, toReplce, string)
    return string