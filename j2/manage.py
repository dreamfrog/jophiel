#!/usr/bin/env python

import os
import sys
import importlib
from django.core.management import execute_manager

import settings
sys.path.insert(0,"..")
if __name__ == "__main__":
    execute_manager(settings)
