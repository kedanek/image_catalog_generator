import sys
import os
from typing import List
from template_builder import TemplateBuilder

# Return True if the fiile/directory name starts with '.', False otherwise.
def is_hidden(name: str) -> bool:
  return name.startswith('.')

# Flatten a 2D array into 1D
def flatten(t: str) -> List[str]:
  return [item for sublist in t for item in sublist]

# Return True if the extension of the provided filename is included in the provided extension list, False otherwise.
def has_target_extension(filename: str, extensions: List[str]) -> bool:
  return any(filename.endswith(ext) for ext in extensions)

# Return the current path if it is a file, otherwise, i.e. if it is a directory, recursively call this function on its children.
def get_children(path, extensions: List[str]) -> List[str]:
  # Base Case / File
  if (os.path.isfile(path)):
    return [path] if has_target_extension(path, extensions) else []
  
  # Recursive Case / Directory
  children = os.listdir(path)
  return flatten(list(map(
    lambda c: [] if is_hidden(c) else get_children(path + '/' + c, extensions),
    children
  )))

root_path = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
extensions = sys.argv[2] if len(sys.argv) > 2 else "gif,jpeg,jpg,png,webp"

children = get_children(root_path, extensions.split(','))
template = TemplateBuilder(children).build()

f = open("catalog.html", "w")
f.write(template)
f.close()

