import pytest
from src.preprocessing.chunking import parse_html, chunk_html


def test_parse_html():
    # testing out basic paragraph returns

    test_html = """
    <!DOCTYPE html>
<head>
  <title>Dungeon Synth: A Guide</title>
      <meta name="viewport" content="target-densitydpi=device-dpi,user-scalable=1,minimum-scale=1,maximum-scale=2.5,initial-scale=1,width=device-width">
          <meta charset="UTF-8">
          <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
      <meta name="description" content="A Guide to Dungeon Synth">
</head>
<div class="col">
        <div class="card m-3">
          <div class="card-header text-center">
            <h4>Mortiis</h4>
          </div>
          <div class=num>
            <p>Crypt of the Wizard</p>
          </div>
        </div>
      </div>
            <div class="col">
        <div class="card m-3">
          <div class="card-header text-center">
            <h4>Old Sorcery</h4>
          </div>
          <div class=card-body>
            <p class="lead">Realms of Magickal Sorrow</p>
            <p class="lead">Strange and Eternal</p>
          </div>
        </div>
      </div>
    """

    test_paragraphs = parse_html(test_html)

    assert test_paragraphs == ["Crypt of the Wizard"]
    assert isinstance(test_paragraphs, list)
    assert isinstance(test_paragraphs[0], str)
