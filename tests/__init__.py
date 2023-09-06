from os.path import abspath, join, dirname
import sys

git_repo_path = abspath(join(dirname(__file__), "..\src"))



print(git_repo_path)


print(sys.path.insert(0,git_repo_path))

