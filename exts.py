import os

from flask_sqlalchemy import SQLAlchemy
from enum import Enum, unique

db = SQLAlchemy()

@unique
class HttpStatusCode(Enum):
    """ Http Status Code Enum.
    Example usage:
        HttpStatusCode.OK.value  # 200
    """

    # SUCCESSFUL RESPONSES
    OK = 200

    # CLIENT ERRORS
    USER_NO_AUTH = 461
    PARAM_NULL = 462
    PARAM_TYPE = 463
    PARAM_FORMAT = 464
    AUTH_FAILED = 465
    TOO_MANY_REQUESTS = 429

    # SERVER ERRORS
    DATABASE_EMPTY = 531
    DATA_NOT_FOUND = 532
    USER_NOT_EXIST = 533
    DATA_ALREADY_EXIST = 534
    LAST_LEVEL = 535
    PDF_FAILED = 536


@unique
class UserTypeCode(Enum):
    """ User Type Code Enum.
    Example usage:
        UserTypeCode.ADMIN.value  # 8862
    """

    ADMIN = 8862
    PARENT = 7273
    STU = 6983