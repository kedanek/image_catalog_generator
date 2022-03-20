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
      <html lang="en" data-mode="light">
      <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style type="text/css">
          html {
            background-size: 16px;
          }
          html[data-mode="light"] {
            background-image: url('./images/background_light.svg');
          }
          html[data-mode="light"] .dark-mode {
            display: none;
          }
          html[data-mode="dark"] {
            background-image: url('./images/background_dark.svg');
          }
          html[data-mode="dark"] .light-mode {
            display: none;
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
            position: fixed;
          }
          .console__btn-group {
            position: fixed;
            right: 30px;
          }
          .console__btn-group__btn {
            height: 45px;
            width: 45px;
            background-size: 22px;
            background-position: center;
            background-repeat: no-repeat;
            border-radius: 50%;
            border: 0;
            cursor: pointer;
          }
          .console__btn-group__btn--light-mode {
            background-image: url('./images/light_mode.svg');
            background-color: white;
          }
          .console__btn-group__btn--dark-mode {
            background-image: url('./images/dark_mode.svg');
            background-color: #333;
          }
          .item {
            overflow: hidden; 
            float: left; 
            display: flex; 
            justify-content: center; 
            align-items: center;
            height: 150px;
            width: 300px;
            margin: 10px;
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
            margin-right: 10px;
          }
          .item__path {
            display: block;
            width: 300px;
          }
          html[data-mode="light"] .item__path {
            color: black;
          }
          html[data-mode="dark"] .item__path {
            color: white;
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
          <div class="console__btn-group">
            <button
              id="light-mode-btn"
              class="console__btn-group__btn console__btn-group__btn--light-mode dark-mode"
            ></button>
            <button
              id="dark-mode-btn"
              class="console__btn-group__btn console__btn-group__btn--dark-mode light-mode"
            ></button>
          </div>
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