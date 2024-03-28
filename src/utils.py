
def separate_input_string(x: str, sep: str) -> list[str]:
    """
    Separates string based on separator token sep and returns list of strings.
    E.g. "URL1$URL" --> ["URL1", "URL2"]
    :param x: str -- Input String
    :param sep: str -- Separator Token
    :return: list[str]
    """
    return x.split(sep)
