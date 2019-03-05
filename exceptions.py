class Error(Exception):
    """Base class for exceptions in the BookStore application."""
    pass


class NoEntriesError(Error):
    """Error when there are no arguments in the Entry widgets"""
    pass


class EmptyEntryError(Error):
    """Error when there are no arguments in the Entry widgets"""
    pass


class MultipleIdenticalEntriesError(Error):
    """Error when the database contains two or more identical books"""
    pass


class EntryExistsError(Error):
    """Error when the database already contains the book"""
    pass


class EditionExistsError(Error):
    """
    Error when the database contains book(s)
    with the same title and author
    """
    pass


class EntryNotExistsError(Error):
    """Error when the database does not contain the book"""
    pass
