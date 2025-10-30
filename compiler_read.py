import re
import sys
import os
from typing import Any, Dict, List, Optional, Tuple

PROGRAM_RE = re.compile(r"<program\b[^>]*>(.*?)</program>", re.DOTALL)
CONFIG_RE = re.compile(r"<config\b[^>]*>(.*?)</config>", re.DOTALL)
DATA_RE = re.compile(r"<data\b[^>]*>(.*?)</data>", re.DOTALL)

def _coerce_value(raw: str) -> Any:
    s = raw.strip()
    # Quoted string
    if (len(s) >= 2) and ((s[0] == s[-1] == '"') or (s[0] == s[-1] == "'")):
        return s[1:-1]
    # Int or float
    try:
        if "." in s or "e" in s.lower():
            return float(s)
        return int(s)
    except ValueError:
        return s

def _parse_config_text(cfg_text: str) -> Dict[str, Any]:
    """
    Parse semicolon-separated assignments, e.g.:
    prog.name="addition";prog.id=0;prog.pvm_version=1
    """
    out: Dict[str, Any] = {}
    for part in cfg_text.split(";"):
        part = part.strip()
        if not part:
            continue
        if "=" not in part:
            # key without value -> store as True
            key = part.strip()
            out[key.replace(".", "_")] = True
            continue
        key, val = part.split("=", 1)
        key = key.strip()
        val = val.strip()
        out[key.replace(".", "_")] = _coerce_value(val)
    return out

class config():
    def __init__(self, **kwargs):
        # Defaults
        self.prog_name: str = ""
        self.prog_id: int = 0
        self.pvm_version: Optional[int] = None
        # Store all parsed fields dynamically
        for k, v in kwargs.items():
            setattr(self, k, v)

    def to_dict(self) -> Dict[str, Any]:
        return dict(self.__dict__)

def parse_program_text(text: str) -> Dict[str, Any]:
    """
    Parse the first <program>...</program> block in text.
    Returns:
        {
          'config': config(),       # populated config object
          'data': str,              # concatenated program text
          'data_sections': [str],   # raw sections inside <data> tags (if any)
          'raw': {
             'config_text': str or '',
             'program_block': str
          }
        }
    """
    m_prog = PROGRAM_RE.search(text)
    if not m_prog:
        raise ValueError("No <program>...</program> section found.")

    program_block = m_prog.group(1)

    # Extract <config>...</config>
    cfg_text = ""
    m_cfg = CONFIG_RE.search(program_block)
    if m_cfg:
        cfg_text = m_cfg.group(1).strip()

    cfg_map = _parse_config_text(cfg_text) if cfg_text else {}
    cfg_obj = config(**cfg_map)

    # Extract <data>...</data> sections; fallback to remainder after </config>
    data_sections: List[str] = [s.strip() for s in DATA_RE.findall(program_block)]
    if not data_sections:
        # Remove the <config>...</config> part, whatever remains is data
        if m_cfg:
            # keep everything before/after config tags as data
            start, end = m_cfg.span()
            before = program_block[:start]
            after = program_block[end:]
            fallback = (before + after).strip()
        else:
            fallback = program_block.strip()
        if fallback:
            data_sections = [fallback]

    data_text = "\n".join(s for s in data_sections if s)

    return {
        "config": cfg_obj,
        "data": data_text,
        "data_sections": data_sections,
        "raw": {
            "config_text": cfg_text,
            "program_block": program_block,
        },
    }

def read_program_file(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    return parse_program_text(text)

if __name__ == "__main__":
    # Support:
    # - No args: default to ./compiler.py if present, else read stdin
    # - "-" arg: read stdin
    # - File path: read that file
    if len(sys.argv) < 2:
        default_path = "compiler.py"
        if os.path.exists(default_path):
            result = read_program_file(default_path)
        else:
            data = sys.stdin.read()
            if not data.strip():
                print("Usage: python compiler_read.py <file>|-")
                sys.exit(1)
            result = parse_program_text(data)
    else:
        arg = sys.argv[1]
        if arg == "-":
            data = sys.stdin.read()
            if not data.strip():
                print("Usage: python compiler_read.py <file>|-")
                sys.exit(1)
            result = parse_program_text(data)
        else:
            result = read_program_file(arg)

    # Minimal, impersonal output
    print("config:", result["config"].to_dict())
    print("data:", result["data"])
