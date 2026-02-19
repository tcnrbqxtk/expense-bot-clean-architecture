class ExpensesCapError(Exception):
    """
    The user has reached the maximum number of expenses allowed.
    """

    pass


class JsonError(Exception):
    """
    Bad json-file.
    """

    pass
