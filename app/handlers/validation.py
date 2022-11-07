import string

from typing import Dict
from werkzeug.datastructures import MultiDict


class ValidationError(Exception):
    """An error thrown when the input format is invalid."""

    def __init__(self, message):
        self.message = message


class ModelParameter:
    """Superclass for parameter types"""

    def __init__(self, name):
        """
        :param name: The name of the parameter in the query string
        """
        self.name = name

    def convert_to_numerical(self, input_value: string) -> int:
        """
        :param input_value:
        :raises ValidationError: if the data format is invalid
        :return: The validated data in a format that can be passed to the model
        """
        raise NotImplementedError


class BinaryParameter(ModelParameter):
    """
    Parameter that can have two values
    """

    def __init__(self, name: string, val_one: string, val_zero: string):
        """
        :param name: The name of the parameter in the query string
        :param val_one: The value represented by 1 in the model
        :param val_zero: The value represented by 0 in the model
        """

        super().__init__(name)
        self.val_one = val_one
        self.val_zero = val_zero

    def convert_to_numerical(self, input_value: string) -> int:
        if input_value == self.val_one:
            return 1

        if input_value == self.val_zero:
            return 0

        raise ValidationError(
            "Parameter `{}` must be either '{}' or '{}'."
            .format(self.name, self.val_one, self.val_zero)
        )


class NumericParameter(ModelParameter):
    """
    Parameter that can have any integer value
    """

    def __init__(self, name: string, minimum: int, maximum: int):
        """
        :param name: The name of the parameter in the query string
        :param minimum: The minimum possible value
        :param maximum: The maximum possible value
        """

        super().__init__(name)
        self.minimum = minimum
        self.maximum = maximum

    def convert_to_numerical(self, input_value: string) -> int:
        try:
            value = int(input_value)
        except ValueError:
            raise ValidationError("Parameter `{}` must be an integer.".format(self.name))

        if self.minimum <= value <= self.maximum:
            return value

        raise ValidationError("Parameter `{}` must be between {} and {}.".format(self.name, self.minimum, self.maximum))


class NominalParameter(ModelParameter):
    """
    Parameter that can have one value out of several predefined ones
    """

    def __init__(self, name: string, values: 'list[string]'):
        """
        :param name: The name of the parameter in the query string
        :param values: The possible values for the parameter, in the order of their value in the model (starting from 0)
        """

        super().__init__(name)
        self.values = values

    def convert_to_numerical(self, input_value: string) -> int:
        if input_value not in self.values:
            raise ValidationError("Parameter `{}` must be one of the following values: {}.".format(self.name, self.values))

        return self.values.index(input_value)


def validate_model_parameters(args: 'MultiDict[str, str]', schema: 'list[ModelParameter]') -> 'Dict[string, int]':
    """
    Validates the input using a given schema.
    :param args: The input
    :param schema: The schema (list of parameters)
    :raises ValidationError: if the data format is invalid
    :return: The parameters in a format that can be used by the model.
    """

    result = {}
    for parameter in schema:
        value = args.get(parameter.name)
        if not value:
            raise ValidationError("Missing a value for the mandatory parameter `{}`.".format(parameter.name))
        result[parameter.name] = parameter.convert_to_numerical(value)

    return result
