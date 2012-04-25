#!/usr/bin/env python

import os
import sys
import importlib

import settings

from django.core.management import execute_manager


if __name__ == "__main__":
    execute_manager(settings)
