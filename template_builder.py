from typing import List
from string import Template

class TemplateBuilder:
  def __init__(self, paths: List[str]):
    self.paths = paths

  def build(self) -> str:
    item_templates = list(map(
      lambda path: self.build_list_item_template(path),
      self.paths
    ))

    body_template = ''.join(item_templates)

    return self.__build_top_template() + body_template + self.__build_bottom_template()

  def build_list_item_template(self, path: str):
    t = Template("""
      <div class="item">
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
          .item {
            overflow: hidden; 
            float: left; 
            display: flex; 
            justify-content: center; 
            align-items: center;
            height: 150px;
            width: 300px;
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
    """

  def __build_bottom_template(self) -> str:
    return """
      </body>
      </html>
    """