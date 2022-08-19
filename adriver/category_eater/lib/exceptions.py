# coding: utf-8
from __future__ import unicode_literals, absolute_import


class CategoryException(Exception):
    pass


class ValidationError(CategoryException):
    pass


class InvalidRequest(CategoryException):
    pass


class Forbidden(CategoryException):
    pass
