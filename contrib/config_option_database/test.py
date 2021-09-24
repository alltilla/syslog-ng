#!/bin/env python3

import pdb
from module_loader import load_modules
from pathlib import Path

lib_dir = Path(__file__).resolve().parents[2] / "lib"
modules_dir = Path(__file__).resolve().parents[2] / "modules"

driver_db = load_modules(lib_dir, modules_dir)

# pdb.set_trace()

for ctx in driver_db.contexts:
    for driver in driver_db.get_drivers_in_context(ctx):
        print(driver)
