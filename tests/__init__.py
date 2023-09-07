import sys
from os.path import abspath, dirname, join

git_repo_path = abspath(join(dirname(__file__), "..\src"))


print(git_repo_path)


print(sys.path.insert(0, git_repo_path))
