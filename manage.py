#!/usr/bin/env python

import os
import sys
from jophiel import settings
project_path = os.path.dirname(os.path.abspath(__file__))
project_dir = project_path.split(os.sep)[-1]

for module in ("jophiel","jophiel/web"):
    sys.path.insert(0,os.path.join(project_path,module))
    
from django.core.management import execute_manager
if __name__ == "__main__":
    execute_manager(settings)
