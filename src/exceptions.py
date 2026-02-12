class ExpensesCapError(Exception):
    """
    Превышено максимальное количество трат.
    """

    pass


class JsonError(Exception):
    """
    Битый json-файл.
    """

    pass
