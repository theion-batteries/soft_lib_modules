from os.path import abspath, join, dirname
import sys

import pytest


git_repo_path = abspath(join(dirname(__file__), "."))
print("git_repo_path", git_repo_path)
sys.path.insert(0, git_repo_path)


import sys


print(sys.path)