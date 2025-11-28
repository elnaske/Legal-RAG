import json
from bs4 import BeautifulSoup
from langchain_text_splitters import RecursiveCharacterTextSplitter

def parse_html(raw_html):
    soup = BeautifulSoup(raw_html, "html.parser")

    # Extract Meta-info
    # - Parties
    # - Court
    # - Paragraph
    # - Dates? (API may be better)

    # Text
    divs = soup.find_all("div", class_="num")
    paragraphs = [div.find('p').get_text(strip=True) for div in divs if div.find('p')]

    return paragraphs

def chunk_html(path):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=20,
        length_function=len,
        is_separator_regex=False,
    )

    texts_all = []
    with open(path, 'r') as f:
        opinion = json.load(f)

    if opinion['html']:
        paragraphs = parse_html(opinion['html'])

        texts = text_splitter.create_documents(paragraphs)
        texts_all = [t.page_content for t in texts]
    
    # Should return metadata as well (e.g. paragraph number)
    return texts_all