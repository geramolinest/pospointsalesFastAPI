from typing import Annotated
from fastapi import Depends

from .Constants import Constants  # type: ignore
from .Config import Config #type: ignore


ConfigDep = Annotated[Config, Depends(Config)]