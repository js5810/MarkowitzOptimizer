import re
from typing import Optional

def extract_percent(s: str) -> Optional[float]:
    match = re.search(r'-?\d+(\.\d+)?', s)
    if match:
        return float(match.group())
    return None