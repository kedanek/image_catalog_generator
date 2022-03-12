import sys
import os

def flatten(t):
    return [item for sublist in t for item in sublist]

def getChildren(path):
  # Base Case / File
  if (os.path.isfile(path)):
    return [path]
  
  # Recursive Case / Directory
  children = os.listdir(path)
  return flatten(list(map(lambda c: getChildren(path + '/' + c), children)))

assetsRootPath = sys.argv[1]
children = getChildren(assetsRootPath)
for c in children:
  print(c)


