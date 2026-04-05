"""
tools.py — 14 tools for the Advanced Cohere + LangGraph Agent
==============================================================
Tools included:
  Math        : add, subtract, multiply, divide, power, square_root,
                evaluate_expression (full expression evaluator)
  Date/Time   : get_current_datetime, days_between
  Conversion  : convert_units
  File I/O    : read_file, write_file, list_directory
  Web Search  : web_search (live via Tavily, or stub)
"""

import os
import math
import datetime
from pathlib import Path

from langchain.tools import tool


# ══════════════════════════════════════════════════════════════════════════════
#  1. CALCULATOR TOOLS
# ══════════════════════════════════════════════════════════════════════════════

@tool
def add(a: float, b: float) -> float:
    """Add two numbers together. Example: add(3, 4) → 7"""
    return a + b


@tool
def subtract(a: float, b: float) -> float:
    """Subtract b from a. Example: subtract(10, 3) → 7"""
    return a - b


@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers. Example: multiply(6, 7) → 42"""
    return a * b


@tool
def divide(a: float, b: float) -> str:
    """
    Divide a by b.
    Returns an error string if b is zero.
    Example: divide(10, 2) → 5.0
    """
    if b == 0:
        return "Error: Cannot divide by zero."
    return str(a / b)


@tool
def power(base: float, exponent: float) -> float:
    """
    Raise base to the power of exponent.
    Example: power(2, 10) → 1024.0
    """
    return base ** exponent


@tool
def square_root(n: float) -> str:
    """
    Return the square root of n.
    Returns an error string for negative input.
    Example: square_root(144) → 12.0
    """
    if n < 0:
        return "Error: Cannot take the square root of a negative number."
    return str(math.sqrt(n))


@tool
def evaluate_expression(expression: str) -> str:
    """
    Safely evaluate a mathematical expression string.

    Supported functions & constants:
      sqrt(x)   — square root
      sin(x)    — sine  (x in radians)
      cos(x)    — cosine
      tan(x)    — tangent
      log(x)    — natural logarithm
      log10(x)  — base-10 logarithm
      abs(x)    — absolute value
      round(x)  — round to nearest integer
      pi        — π ≈ 3.14159…
      e         — Euler's number ≈ 2.71828…

    Operators: +  -  *  /  **  //  %

    Examples:
      "2 * (3 + 4) ** 2"          → 98
      "sin(pi / 2)"               → 1.0
      "log(e)"                    → 1.0
      "round(sqrt(2) * 100) / 100" → 1.41
    """
    safe_globals = {
        "__builtins__": {},          # block all built-ins for safety
        "sqrt":  math.sqrt,
        "sin":   math.sin,
        "cos":   math.cos,
        "tan":   math.tan,
        "log":   math.log,
        "log10": math.log10,
        "pi":    math.pi,
        "e":     math.e,
        "abs":   abs,
        "round": round,
        "pow":   pow,
    }
    try:
        result = eval(expression, safe_globals)   # noqa: S307
        return str(result)
    except ZeroDivisionError:
        return "Error: Division by zero in expression."
    except Exception as exc:
        return f"Error evaluating '{expression}': {exc}"


# ══════════════════════════════════════════════════════════════════════════════
#  2. DATE / TIME TOOLS
# ══════════════════════════════════════════════════════════════════════════════

@tool
def get_current_datetime() -> str:
    """
    Return the current local date and time in ISO 8601 format.
    Example output: "2024-08-15T14:32:07"
    """
    return datetime.datetime.now().isoformat(timespec="seconds")


@tool
def days_between(date1: str, date2: str) -> str:
    """
    Calculate the number of days between two dates.
    Both dates must be in YYYY-MM-DD format.
    Example: days_between("2024-01-01", "2024-12-31") → "365"
    """
    try:
        d1 = datetime.date.fromisoformat(date1)
        d2 = datetime.date.fromisoformat(date2)
        return str(abs((d2 - d1).days))
    except ValueError as exc:
        return f"Error: {exc}. Use YYYY-MM-DD format."


# ══════════════════════════════════════════════════════════════════════════════
#  3. UNIT CONVERTER
# ══════════════════════════════════════════════════════════════════════════════

@tool
def convert_units(value: float, from_unit: str, to_unit: str) -> str:
    """
    Convert a value between common units.

    Supported categories and units:
      Temperature : celsius, fahrenheit, kelvin
      Length      : meters, feet, inches, kilometers, miles, centimeters
      Weight      : kg, lbs, grams, ounces

    Examples:
      convert_units(100, "celsius", "fahrenheit") → "212.0 fahrenheit"
      convert_units(5, "kilometers", "miles")     → "3.10686 miles"
      convert_units(70, "kg", "lbs")              → "154.324 lbs"
    """
    f, t = from_unit.strip().lower(), to_unit.strip().lower()

    # ── Temperature (special-cased because non-linear) ─────────────────────
    temp_map = {
        ("celsius",    "fahrenheit"): lambda v: v * 9 / 5 + 32,
        ("fahrenheit", "celsius"):    lambda v: (v - 32) * 5 / 9,
        ("celsius",    "kelvin"):     lambda v: v + 273.15,
        ("kelvin",     "celsius"):    lambda v: v - 273.15,
        ("fahrenheit", "kelvin"):     lambda v: (v - 32) * 5 / 9 + 273.15,
        ("kelvin",     "fahrenheit"): lambda v: (v - 273.15) * 9 / 5 + 32,
    }
    if (f, t) in temp_map:
        result = temp_map[(f, t)](value)
        return f"{result:.4g} {t}"

    # ── Linear conversions (multiply by factor) ────────────────────────────
    # All factors are relative to a SI base unit per category.
    # Length base: meters | Weight base: kilograms
    to_base = {
        # Length → meters
        "meters": 1, "centimeters": 0.01, "kilometers": 1000,
        "feet": 0.3048, "inches": 0.0254, "miles": 1609.34,
        # Weight → kg
        "kg": 1, "grams": 0.001, "lbs": 0.453592, "ounces": 0.0283495,
    }

    if f not in to_base or t not in to_base:
        return (
            f"Unsupported unit pair: '{from_unit}' → '{to_unit}'. "
            "Supported: meters, centimeters, kilometers, feet, inches, miles, "
            "kg, grams, lbs, ounces, celsius, fahrenheit, kelvin."
        )

    # Check same category (both length or both weight)
    length_units = {"meters", "centimeters", "kilometers", "feet", "inches", "miles"}
    weight_units = {"kg", "grams", "lbs", "ounces"}
    if (f in length_units) != (t in length_units):
        return f"Error: Cannot convert between different categories ('{from_unit}' and '{to_unit}')."

    result = value * to_base[f] / to_base[t]
    return f"{result:.6g} {t}"


# ══════════════════════════════════════════════════════════════════════════════
#  4. FILE I/O TOOLS
# ══════════════════════════════════════════════════════════════════════════════

@tool
def read_file(filepath: str) -> str:
    """
    Read and return the full contents of a text file.
    Example: read_file("notes.txt")
    """
    try:
        return Path(filepath).read_text(encoding="utf-8")
    except FileNotFoundError:
        return f"Error: File '{filepath}' not found."
    except Exception as exc:
        return f"Error reading '{filepath}': {exc}"


@tool
def write_file(filepath: str, content: str) -> str:
    """
    Write (or overwrite) content to a text file.
    Creates the file and any missing parent directories automatically.
    Example: write_file("output/result.txt", "Hello, world!")
    """
    try:
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return f"✅ Wrote {len(content)} characters to '{filepath}'."
    except Exception as exc:
        return f"Error writing '{filepath}': {exc}"


@tool
def list_directory(path: str = ".") -> str:
    """
    List all files and subdirectories in the given path.
    Defaults to the current working directory.
    Example: list_directory("./data")
    """
    try:
        entries = sorted(Path(path).iterdir(), key=lambda p: (p.is_file(), p.name))
        if not entries:
            return f"('{path}' is empty)"
        lines = [f"{'📄' if e.is_file() else '📁'}  {e.name}" for e in entries]
        return f"Contents of '{path}':\n" + "\n".join(lines)
    except FileNotFoundError:
        return f"Error: Path '{path}' not found."
    except Exception as exc:
        return f"Error listing '{path}': {exc}"


# ══════════════════════════════════════════════════════════════════════════════
#  5. WEB SEARCH
# ══════════════════════════════════════════════════════════════════════════════

@tool
def web_search(query: str) -> str:
    """
    Search the web for up-to-date information.

    Live mode  : set TAVILY_API_KEY in your .env and install tavily-python.
    Stub mode  : returns a helpful message explaining how to enable live search.

    Example: web_search("latest Python 3.13 features")
    """
    api_key = os.getenv("TAVILY_API_KEY", "").strip()

    # ── Live search via Tavily ─────────────────────────────────────────────
    if api_key:
        try:
            from tavily import TavilyClient          # pip install tavily-python
            client = TavilyClient(api_key=api_key)
            response = client.search(query, max_results=5)
            results = response.get("results", [])
            if not results:
                return "No results found for your query."
            lines = []
            for i, r in enumerate(results, 1):
                title   = r.get("title", "No title")
                url     = r.get("url", "")
                snippet = r.get("content", "")[:300].replace("\n", " ")
                lines.append(f"{i}. **{title}**\n   {url}\n   {snippet}…")
            return "\n\n".join(lines)
        except ImportError:
            return (
                "⚠️  TAVILY_API_KEY is set but 'tavily-python' is not installed.\n"
                "Run: pip install tavily-python"
            )
        except Exception as exc:
            return f"Search error: {exc}"

    # ── Stub: no API key configured ────────────────────────────────────────
    return (
        f"🔍 Web search is not yet configured.\n\n"
        f"Your query was: \"{query}\"\n\n"
        "To enable live web search:\n"
        "  1. Sign up (free) at https://tavily.com\n"
        "  2. Add to your .env file:  TAVILY_API_KEY=tvly-...\n"
        "  3. Install the client:     pip install tavily-python\n\n"
        "Restart the agent and web_search will use real results automatically."
    )


# ══════════════════════════════════════════════════════════════════════════════
#  TOOL REGISTRY  (import this in agent.py)
# ══════════════════════════════════════════════════════════════════════════════

ALL_TOOLS = [
    # Calculator
    add,
    subtract,
    multiply,
    divide,
    power,
    square_root,
    evaluate_expression,
    # Date / Time
    get_current_datetime,
    days_between,
    # Unit Conversion
    convert_units,
    # File I/O
    read_file,
    write_file,
    list_directory,
    # Web Search
    web_search,
]