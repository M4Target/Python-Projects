from bs4 import BeautifulSoup

input_file = "scraped_content.html"
output_file = "第三部 領主的養女Ⅳ.html"

# Read the HTML content from the file
with open(input_file, "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

# Create a new style tag for CSS
style_tag = soup.new_tag("style")
style_tag.string = '''
      body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
          Oxygen-Sans, Ubuntu, Cantarell, "Helvetica Neue", sans-serif;
        line-height: 1.6;
        padding: 20px;
        max-width: 800px;
        margin: auto;
      }

      h1 {
        font-size: 2em;
        font-weight: bold;
        margin-top: 20px;
      }

      p {
        margin-top: 10px;
        font-size: 1.5em;
        text-align: justify;
      }

      h1:first-of-type {
        margin-top: 0;
      }
'''

# Append the style tag to the head
soup.head.append(style_tag)

# Create a new div for the Table of Contents
toc_div = soup.new_tag("div", id="table-of-contents")
toc_div.append(soup.new_tag("h2"))
toc_div.h2.string = "Table of Contents"
toc_list = soup.new_tag("ul")

# Find all <h1> tags and create anchor links
for index, h1 in enumerate(soup.find_all("h1"), start=1):
    # Create an id for each <h1> tag
    h1_id = f"section-{index}"
    h1['id'] = h1_id

    # Create a list item for the ToC
    toc_item = soup.new_tag("li")
    toc_link = soup.new_tag("a", href=f"#{h1_id}")
    toc_link.string = h1.get_text()
    toc_item.append(toc_link)
    toc_list.append(toc_item)

# Append the list to the ToC div
toc_div.append(toc_list)

# Insert the ToC at the beginning of the body
soup.body.insert(0, toc_div)

# Save the modified HTML content to a new file
with open(output_file, "w", encoding="utf-8") as file:
    file.write(str(soup))

print("Table of Contents has been added and saved to scraped_content_with_toc.html")