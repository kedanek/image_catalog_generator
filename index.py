import sys
import os
from typing import List

def flatten(t):
    return [item for sublist in t for item in sublist]

# Return True if the fiile/directory name starts with '.', False otherwise.
def isHidden(name: str) -> bool:
  return name.startswith('.')

def getChildren(path) -> List[str]:
  # Base Case / File
  if (os.path.isfile(path)):
    return [path]
  
  # Recursive Case / Directory
  children = os.listdir(path)
  return flatten(list(map(
    lambda c: [] if isHidden(c) else getChildren(path + '/' + c),
    children
  )))

assetsRootPath = sys.argv[1]
children = getChildren(assetsRootPath)
for c in children:
  print(c)


