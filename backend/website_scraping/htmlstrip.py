# Script to strip given text from HTML tags
# Use case: Content from webpages recovered may have stray HTML tags, like <b> or <i>

from html.parser import HTMLParser

# Simple class to encapsulate the stripping of HTML tags.
class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()  # Call the parent constructor
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)

# Module to strip tags using the MLStripper class
def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

# Example usage
if __name__ == "__main__":
    sample_html = "<html><body><h1>Title</h1><p>This is a <b>bold</b> paragraph.</p></body></html>"
    print(strip_tags(sample_html))
