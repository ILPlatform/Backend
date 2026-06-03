#!/usr/bin/env python3

import os
import sys
from pathlib import Path

from dotenv import load_dotenv


FUNCTIONS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(FUNCTIONS_DIR))
os.chdir(FUNCTIONS_DIR)

load_dotenv(FUNCTIONS_DIR / ".env")
load_dotenv(FUNCTIONS_DIR / "config.env")

from FunctionsCurriculum.DailyClasses.DailyTeacherClassesEmail import main


if __name__ == "__main__":
    main()
