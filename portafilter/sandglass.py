from typing import Optional, Union, Any
from datetime import datetime, timedelta
from enum import Enum


class InvalidDate(Exception):
    pass


class ParseSpecialKey(Enum):
    TODAY = 'today'
    YESTERDAY = 'yesterday'
    TOMORROW = 'tomorrow'


class Sandglass:

    def __init__(self, date: Union[str, datetime], date_format: Optional[str] = None):
        """The init method

        Arguments:
            date (Union[str, datetime]) -- The date.

        Keyword Arguments:
            date_format (str) -- The date format (default None)

        Raises:
            InvalidDate -- The invalid date exception.
        """
        self._datetime = self._parse(date, date_format)

    def _parse(self, date: Union[str, datetime], date_format: Optional[str] = None) -> datetime:
        """Parse the date

        Arguments:
            date (Union[str, datetime]) -- The date.

        Keyword Arguments:
            date_format (str) -- The date format (default None)

        Returns:
            datetime

        Raises:
            InvalidDate -- The invalid date exception.
        """
        if isinstance(date, datetime):
            return date

        try:
            if date_format:
                return datetime.strptime(date, date_format)

            else:

                if self.is_parse_special_key(date):
                    special_key = ParseSpecialKey(date)

                    if hasattr(Sandglass, str(special_key.value)):

                        return getattr(Sandglass, str(special_key.value))().get_datetime()

                    else:
                        raise NotImplementedError

                return datetime.strptime(date, '%Y-%m-%d')

        except Exception as e:
            raise InvalidDate

    def start_of_day(self):
        """Set the date to the start of the day

        Returns:
            Self
        """
        self._datetime = self._parse(self.get_datetime().strftime('%Y-%m-%d 00:00:00'), '%Y-%m-%d %H:%M:%S')
        return self

    def end_of_day(self):
        """Set the date to the end of the day

        Returns:
            Self
        """
        self._datetime = self._parse(self.get_datetime().strftime('%Y-%m-%d 23:59:59'), '%Y-%m-%d %H:%M:%S')
        return self

    def add_day(self, value: int = 1):
        """Add N days

        Arguments:
            value (int) -- The number of days to add (default 1)

        Returns:
            Self
        """
        self._datetime += timedelta(days=value)
        return self

    def sub_day(self, value: int = 1):
        """Sub N days

        Arguments:
            value (int) -- The number of days to sub (default 1)

        Returns:
            Self
        """
        self._datetime -= timedelta(days=value)
        return self

    @staticmethod
    def now():
        """Get the now datetime

        Returns:
            Sandglass
        """
        return Sandglass(datetime.now())

    @staticmethod
    def today():
        """Get the today datetime

        Returns:
            Sandglass
        """
        return Sandglass.now()

    @staticmethod
    def yesterday():
        """Get the yesterday datetime

        Returns:
            Sandglass
        """
        return Sandglass.now().add_day(-1)

    @staticmethod
    def tomorrow():
        """Get the yesterday datetime

        Returns:
            Sandglass
        """
        return Sandglass.now().add_day(1)

    @staticmethod
    def _validate_operator_type(other: Any) -> None:
        """Validate the operator variable type.

        Arguments:
            other (Any)

        Raises:
            Exception
        """
        if not isinstance(other, Sandglass):
            raise Exception('The other variable must be an instance of Sandglass.')

    def get_datetime(self) -> datetime:
        """Get the datetime instance

        Returns:
            datetime
        """
        return self._datetime

    def __lt__(self, other: Any) -> bool:
        """The lt operator.

        Arguments:
            other (Any)

        Returns:
            bool

        Raises:
            Exception
        """
        self._validate_operator_type(other)

        return self.get_datetime() < other.get_datetime()

    def __le__(self, other: Any):
        """The le operator.

        Arguments:
            other (Any)

        Returns:
            bool

        Raises:
            Exception
        """
        self._validate_operator_type(other)

        return self.get_datetime() <= other.get_datetime()

    def __eq__(self, other: Any):
        """The eq operator.

        Arguments:
            other (Any)

        Returns:
            bool

        Raises:
            Exception
        """
        self._validate_operator_type(other)

        return self.get_datetime() == other.get_datetime()

    def __ne__(self, other: Any):
        """The ne operator.

        Arguments:
            other (Any)

        Returns:
            bool

        Raises:
            Exception
        """
        self._validate_operator_type(other)

        return self.get_datetime() != other.get_datetime()

    def __ge__(self, other: Any):
        """The ge operator.

        Arguments:
            other (Any)

        Returns:
            bool

        Raises:
            Exception
        """
        self._validate_operator_type(other)

        return self.get_datetime() >= other.get_datetime()

    def __gt__(self, other: Any):
        """The gt operator.

        Arguments:
            other (Any)

        Returns:
            bool

        Raises:
            Exception
        """
        self._validate_operator_type(other)

        return self.get_datetime() > other.get_datetime()

    def is_past(self) -> bool:
        """The is past check.

        Returns:
            bool
        """
        return self <= Sandglass.now()

    def is_future(self) -> bool:
        """The is future check.

        Returns:
            bool
        """
        return self > Sandglass.now()

    def to_string(self, date_format: Optional[str] = None) -> str:
        """Get the stringify datetime.

        Keyword Arguments:
            date_format (str) -- The date format (default None)

        Returns:
            str
        """
        return str(self.get_datetime()) if not date_format else self.get_datetime().strftime(date_format)

    @staticmethod
    def is_parse_special_key(date: str) -> bool:
        """Check the existence of the parsing special key.

        Arguments:
            date (str)

        Returns:
            bool
        """
        try:
            ParseSpecialKey(date)

            return True

        except ValueError as e:
            return False
