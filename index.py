import sys
import os
from typing import List

# Return True if the fiile/directory name starts with '.', False otherwise.
def isHidden(name: str) -> bool:
  return name.startswith('.')

# Flatten a 2D array into 1D
def flatten(t: str) -> List[str]:
  return [item for sublist in t for item in sublist]

# Return True if the extension of the provided filename is included in the provided extension list, False otherwise.
def hasTargetExtension(filename: str, extensions: List[str]) -> bool:
  return any(filename.endswith(ext) for ext in extensions)

# Return the current path if it is a file, otherwise, i.e. if it is a directory, recursively call this function on its children.
def getChildren(path, extensions: List[str]) -> List[str]:
  # Base Case / File
  if (os.path.isfile(path)):
    return [path] if hasTargetExtension(path, extensions) else []
  
  # Recursive Case / Directory
  children = os.listdir(path)
  return flatten(list(map(
    lambda c: [] if isHidden(c) else getChildren(path + '/' + c, extensions),
    children
  )))

assetsRootPath = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
defaultImgExtensions = "gif,jpeg,jpg,png,webp"
extensions = sys.argv[2] if len(sys.argv) > 2 else defaultImgExtensions

children = getChildren(assetsRootPath, extensions.split(','))
for c in children:
  print(c)


