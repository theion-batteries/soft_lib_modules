import os
import sys

from src.module.builder import build_module_component

# from dotenv import load_dotenv



# load_dotenv()

if __name__ == "__main__":
    print(sys.modules["src.module.components.module_components"])
    dir = os.getenv("CONFIG_DIR")
    file = os.path.join(dir, "grbl_module.yaml")
    result = build_module_component(file, "cnt_motion")
