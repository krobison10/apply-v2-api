from ..config import *
import re


class Validate:
    @staticmethod
    def number(number, name: str = "value"):
        try:
            number = int(number)
        except ValueError:
            JSONError.throw_json_error(f"The {name} must be numeric")

        if number < 0:
            JSONError.throw_json_error(f"The {name} must be a positive number")

        return number

    @staticmethod
    def email(email: str):
        pattern = r"/^(?!(?:(?:\x22?\x5C[\x00-\x7E]\x22?)|(?:\x22?[^\x5C\x22]\x22?)){255,})(?!(?:(?:\x22?\x5C[\x00-\x7E]\x22?)|(?:\x22?[^\x5C\x22]\x22?)){65,}@)(?:(?:[\x21\x23-\x27\x2A\x2B\x2D\x2F-\x39\x3D\x3F\x5E-\x7E]+)|(?:\x22(?:[\x01-\x08\x0B\x0C\x0E-\x1F\x21\x23-\x5B\x5D-\x7F]|(?:\x5C[\x00-\x7F]))*\x22))(?:\.(?:(?:[\x21\x23-\x27\x2A\x2B\x2D\x2F-\x39\x3D\x3F\x5E-\x7E]+)|(?:\x22(?:[\x01-\x08\x0B\x0C\x0E-\x1F\x21\x23-\x5B\x5D-\x7F]|(?:\x5C[\x00-\x7F]))*\x22)))*@(?:(?:(?!.*[^.]{64,})(?:(?:(?:xn--)?[a-z0-9]+(?:-[a-z0-9]+)*\.){1,126}){1,}(?:(?:[a-z][a-z0-9]*)|(?:(?:xn--)[a-z0-9]+))(?:-[a-z0-9]+)*)|(?:\[(?:(?:IPv6:(?:(?:[a-f0-9]{1,4}(?::[a-f0-9]{1,4}){7})|(?:(?!(?:.*[a-f0-9][:\]]){7,})(?:[a-f0-9]{1,4}(?::[a-f0-9]{1,4}){0,5})?::(?:[a-f0-9]{1,4}(?::[a-f0-9]{1,4}){0,5})?)))|(?:(?:IPv6:(?:(?:[a-f0-9]{1,4}(?::[a-f0-9]{1,4}){5}:)|(?:(?!(?:.*[a-f0-9]:){5,})(?:[a-f0-9]{1,4}(?::[a-f0-9]{1,4}){0,3})?::(?:[a-f0-9]{1,4}(?::[a-f0-9]{1,4}){0,3}:)?)))?(?:(?:25[0-5])|(?:2[0-4][0-9])|(?:1[0-9]{2})|(?:[1-9]?[0-9]))(?:\.(?:(?:25[0-5])|(?:2[0-4][0-9])|(?:1[0-9]{2})|(?:[1-9]?[0-9]))){3}))\]))$/iD"
        if not re.fullmatch(pattern, email):
            JSONError.throw_json_error(
                "Invalid email: contains 1 or more invalid characters"
            )
        return email

    @staticmethod
    def max_length(str: str, length: int = 50, name: str = "value"):
        if len(str) > length:
            JSONError.throw_json_error(f"Max length for {name} is {length} characters")
        return str

    @staticmethod
    def required_fields(object: object, dependencies: list):
        """
        Verifies that specified fields are defined and truthy on the given object.

        Parameters:
            object (Any): The object to check attributes for.
            dependencies (list[str]): A list of attribute names to verify on the object.

        Raises:
            ValueError: If any specified attribute is not defined or is falsy.
        """

        for dependency in dependencies:
            if not hasattr(object, dependency) or not getattr(object, dependency):
                raise ValueError(f"Field '{dependency}' needs to be defined")

    @staticmethod
    def not_null(dependencies: list):
        for dependency in dependencies:
            if not dependency:
                raise ValueError(f"Field is null")
