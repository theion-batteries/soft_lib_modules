import os
import sys
from os.path import abspath, dirname, join

from dotenv import load_dotenv

git_repo_path = abspath(join(dirname(__file__), "."))
sys.path.insert(0, git_repo_path)

load_dotenv()
config_dir = os.getenv("CONFIG_DIR")
log_dir = os.getenv("LOG_DIR")
settings_dir = os.getenv("SETTING_DIR")
instructions_dir = os.getenv("INSTRUCTION_DIR")
test_dir = os.getenv("TEST_CONFIG_DIR")
