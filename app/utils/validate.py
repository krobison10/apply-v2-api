from ..config import *
import re
from email_validator import validate_email, EmailNotValidError


class Validate:
    @staticmethod
    def number(
        number, name: str = "value", required: bool = True, positive: bool = True
    ):
        if required and not number and number != 0:
            JSONError.throw_json_error(f"'{name}' is required")
        if number is None:
            return None
        try:
            number = int(number)
        except ValueError:
            JSONError.throw_json_error(f"The {name} must be numeric")

        if positive and number < 0:
            JSONError.throw_json_error(f"The {name} must be a positive number")

        return number

    @staticmethod
    def email(email: str):
        try:
            email = str(validate_email(email).email)
        except EmailNotValidError as e:
            JSONError.status_code = 422
            JSONError.throw_json_error(str(e))
        return email

    @staticmethod
    def max_length(str: str, length: int = 50, name: str = "value"):
        if len(str) > length:
            JSONError.throw_json_error(f"Max length for {name} is {length} characters")
        return str

    @staticmethod
    def required_fields(data, dependencies: list, code: int = 500):
        """
        Verifies that specified fields are defined and truthy on the given object.

        Parameters:
            object (Any): The object to check attributes for.
            dependencies (list[str]): A list of attribute names to verify on the object.

        Raises:
            ValueError: If any specified attribute is not defined or is falsy.
        """

        # Check if the input is a dictionary

        if isinstance(data, dict):
            for dependency in dependencies:
                if dependency not in data or not data[dependency]:
                    if code == 500:
                        raise ValueError(
                            f"Field '{dependency}' needs to be defined and truthy"
                        )
                    JSONError.status_code = code
                    JSONError.throw_json_error(
                        f"Field '{dependency}' needs to be defined and truthy"
                    )
        else:
            # Assume the input is an object if not a dictionary
            for dependency in dependencies:
                if not hasattr(data, dependency) or not getattr(data, dependency):
                    if code == 500:
                        raise ValueError(
                            f"Field '{dependency}' needs to be defined and truthy"
                        )
                    JSONError.status_code = code
                    JSONError.throw_json_error(
                        f"Field '{dependency}' needs to be defined and truthy"
                    )

    @staticmethod
    def not_null(dependencies: list):
        for dependency in dependencies:
            if not dependency:
                raise ValueError(f"Field is null")
