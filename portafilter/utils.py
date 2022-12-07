from typing import Any, Union, Dict
from os import getenv
from portafilter.translator import TransCollection


def env(key: str, default_value: Any = None) -> Any:
    """Get the variable from the environment

    Arguments:
        key (str) -- The specific key

    Keyword Arguments:
        default_value (Any) -- The default value (default None)
    """
    return getenv(key, default_value)


def trans(key: str, attributes: Union[Dict, None] = None) -> str:
    """Translate a key.

    Arguments:
        key (str) -- The key path to translate
    
    Keyword Arguments:
        attributes (Union[Dict, None]) -- The string attributes to replace (default None)
    
    Returns:
        str
    """
    return TransCollection.get_instance().get(key=key, attributes=attributes)
