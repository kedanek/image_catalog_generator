from typing import List
from string import Template
import json

class TemplateBuilder:
  def __init__(self, paths: List[str]):
    self.paths = paths

  def build(self) -> str:
    item_templates = list(map(
      lambda path: self.build_list_item_template(path),
      self.paths
    ))

    body_template = ''.join(item_templates)

    return self.__build_top_template() + body_template + self.__build_script_template(self.paths) + self.__build_bottom_template()

  def build_list_item_template(self, path: str):
    t = Template("""
      <div
        class="item"
        data-visible="1"
        data-path="$path"
      >
        <div class="item__img" style="background-image: url('$path')"></div>
        <span class="item__path">$path</span>
      </div>
    """)
    return t.substitute(path=path)

  def __build_top_template(self) -> str:
    return """
      <!DOCTYPE html>
      <html lang="en">
      <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style type="text/css">
          html {
            background-image: url('./background.png');
          }
          .console {
            width: 100vw;
            height: 60px;
            display: flex;
            justify-content: center;
            align-items: center;
          }
          .console__input {
            width: 240px;
            padding: 6px;
          }
          .item {
            overflow: hidden; 
            float: left; 
            display: flex; 
            justify-content: center; 
            align-items: center;
            height: 150px;
            width: 300px;
          }
          .item[data-visible="0"] {
            display: none;
          }
          .item__img {
            height: 150px;
            width: 150px;
            background-size: contain;
            background-position: center;
            background-repeat: no-repeat;
          }
          .item__path {
            display: block;
            width: 300px;
          }
        </style>
        <title>Catalog</title>
      </head>
      <body>
        <div class="console">
          <input
            id="filter-input"
            class="console__input"
            type="text"
            placeholder="Filter"
          >
        </div>
    """

  def __build_script_template(self, paths: List[str]) -> str:
    script_file = open("script.js", "r")
    script_template = "<script>" + script_file.read() + "</script>"
    script_file.close()
    return script_template.replace("$paths", json.dumps(paths))

  def __build_bottom_template(self) -> str:
    return """
      </body>
      </html>
    """