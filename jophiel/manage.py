#!/usr/bin/env python

import settings

from django.core.management import execute_manager
import sys

sys.path.insert(0,"..")

if __name__ == "__main__":
    execute_manager(settings)
