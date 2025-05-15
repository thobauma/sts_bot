from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class Relic:
    name: str
    id: str
    counter: Optional[int] = -1
    price: Optional[int] = -1
