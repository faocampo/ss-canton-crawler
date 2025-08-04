from crawler.parser import extract_text


def test_extract_text_cleans_html():
    html = (
        "<html><body>"
        "<nav class='menu'><a href='/'>Home</a></nav>"
        "<h1>Title</h1>"
        "<p>Paragraph <a href='link'>link</a></p>"
        "<script>ignored()</script>"
        "<style>.x{}</style>"
        "<img src='img.png'/>"
        "</body></html>"
    )
    text = extract_text(html)
    assert text == "Title Paragraph link"
