from bs4 import BeautifulSoup
from selenium import webdriver
import time

# Initialize WebDriver and parameter
driver = webdriver.Chrome()  # Ensure you have the appropriate WebDriver installed
content = []

##########################################
############# setup input ################
##########################################

page = 122758
page_end = 122761
scroll_time_setting = 2
input_file = "scraped_content.html"
output_file = "testing.html"

##########################################
############# setup input ################
##########################################

# While loop the process for multiple pages

while True:
    # Open the URL of the webpage without suffix
    url = "https://tw.linovelib.com/novel/73/{}.html".format(page)
    driver.get(url)

    # Automatically scroll the page
    scroll_pause_time = scroll_time_setting  # Pause between each scroll
    screen_height = driver.execute_script("return window.screen.height;")  # Browser window height
    i = 1
    while True:
        # Scroll down
        driver.execute_script(f"window.scrollTo(0, {screen_height * i});")
        i += 1
        time.sleep(scroll_pause_time)

        # Check if reaching the end of the page
        scroll_height = driver.execute_script("return document.body.scrollHeight;")
        if screen_height * i > scroll_height:
            break

    # Fetch the data using BeautifulSoup after all data is loaded
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    # Filter out unwanted paragraphs
    unwanted_texts = ["翻上頁", "呼出功能", "翻下頁", "上一頁", "目錄", "書頁", "下一頁", "背景", "字體", "章評", "插圖"]
    paragraphs = soup.select("p")
    filtered_paragraphs = [p for p in paragraphs if not any(text in p.get_text() for text in unwanted_texts)]
    
    # Append the title and filtered paragraphs only if the number of words in filtered paragraphs is greater than or equal to the number of words in heading
    title = soup.select_one("title").get_text()
    heading = soup.select_one("h1").get_text() if soup.select_one("h1") else "No Heading"
    heading2 = soup.select_one("h3").get_text() if soup.select_one("h1") else "No Heading"

    if len(filtered_paragraphs) > len(heading2):
        page_content = f"<h1>{heading}</h1>\n<p>Web Page: {page}</p>\n"
        page_content += "\n".join([str(paragraph) for paragraph in filtered_paragraphs])

        content.append(f"<h2>{title}</h2>\n{page_content}\n<hr>")

    # Check for suffixes dynamically
    suffix = "_2"
    suffix_url = f"https://tw.linovelib.com/novel/73/{page}{suffix}.html"
    driver.get(suffix_url)

    # Automatically scroll the page
    scroll_pause_time = scroll_time_setting  # Pause between each scroll
    screen_height = driver.execute_script("return window.screen.height;")  # Browser window height
    i = 1
    while True:
        # Scroll down
        driver.execute_script(f"window.scrollTo(0, {screen_height * i});")
        i += 1
        time.sleep(scroll_pause_time)

        # Check if reaching the end of the page
        scroll_height = driver.execute_script("return document.body.scrollHeight;")
        if screen_height * i > scroll_height:
            break

    # Fetch the data using BeautifulSoup after all data is loaded
    suffix_soup = BeautifulSoup(driver.page_source, "html.parser")
    atitle = suffix_soup.select_one('h1#atitle')

    # Determine the maximum number of suffix pages if atitle is present
    if atitle:
        total_suffix_pages = int(atitle.get_text().split('（')[1].split('/')[1].split('）')[0])
        for i in range(2, total_suffix_pages + 1):
            suffix = f"_{i}"
            suffix_url = f"https://tw.linovelib.com/novel/73/{page}{suffix}.html"
            driver.get(suffix_url)

            # Automatically scroll the page
            scroll_pause_time = scroll_time_setting  # Pause between each scroll
            screen_height = driver.execute_script("return window.screen.height;")  # Browser window height
            j = 1
            while True:
                # Scroll down
                driver.execute_script(f"window.scrollTo(0, {screen_height * j});")
                j += 1
                time.sleep(scroll_pause_time)

                # Check if reaching the end of the page
                scroll_height = driver.execute_script("return document.body.scrollHeight;")
                if screen_height * j > scroll_height:
                    break
            
            # Fetch the data using BeautifulSoup after all data is loaded
            soup = BeautifulSoup(driver.page_source, "html.parser")
            
            # Filter out unwanted paragraphs
            paragraphs = soup.select("p")
            filtered_paragraphs = [p for p in paragraphs if not any(text in p.get_text() for text in unwanted_texts)]
            
            # Append the title and filtered paragraphs only if the number of words in filtered paragraphs is greater than or equal to the number of words in heading
            title = soup.select_one("title").get_text()
            heading = soup.select_one("h1").get_text() if soup.select_one("h1") else "No Heading"

            if len(filtered_paragraphs) > len(heading):
                page_content = f"<h1>{heading}</h1>\n<p>Web Page: {page}</p>\n"
                page_content += "\n".join([str(paragraph) for paragraph in filtered_paragraphs])
                page_content += '\n<a href="#top">Back to top</a>\n<hr>'
            
                content.append(f"<h2>{title}</h2>\n{page_content}\n<hr>")


    # While loop the process for multiple pages
    page += 1
    # It will traverse for only 5 pages as you are after if want more page just comment the below if block
    if page > page_end:
        break

# Close the WebDriver session
driver.quit()

# Save the content to an HTML file
html_content = "<html>\n<head>\n<meta charset='UTF-8'>\n<title>Web Scraped Content</title>\n</head>\n<body>\n"
html_content += "\n".join(content)
html_content += "\n</body>\n</html>"

with open(input_file, "w", encoding="utf-8") as file:
    file.write(html_content)
       
############ making table of content and format ############
############ making table of content and format ############

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

print("Table of Contents has been added and saved to {}".format(output_file))