"""Execute the complete pipeline in its required order."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> None:
    """Run web scraping, cleaning, ranking, and Flask in sequence."""
    root = Path(__file__).resolve().parent
    python = sys.executable
    jupyter = root / ".venv" / "bin" / "jupyter"
    
    stages = [
        [jupyter, "nbconvert", "--execute", "--inplace", "web_scraping/scraper.ipynb"],
        [jupyter, "nbconvert", "--execute", "--inplace", "web_scraping/data_cleaning.ipynb"],
        [jupyter, "nbconvert", "--execute", "--inplace", "machine_learning/machine_learning.ipynb"],
    ]
    for command in stages:
        subprocess.run(command, cwd=root, check=True)
    subprocess.run([python, "web/web_app.py"], cwd=root, check=True)


if __name__ == "__main__":
    main()