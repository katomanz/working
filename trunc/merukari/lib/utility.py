from bs4 import BeautifulSoup
import random

############################
###### Function       ######
############################
# Get find element by css selector
def getText_find_element_by_css_selector(browser, cssSel):
    try:
        ret = browser.find_element_by_css_selector(cssSel).text
    except:
        print("Could not find " + cssSel)
        ret = "NA"
    finally:
        return ret

# Get Html file only
def getHtmlFromItemsbox(browser, url):
    browser.get(url)
    return BeautifulSoup(browser.page_source, 'html.parser')

# Save Html file to the specified path
def saveHtmlFile(soup, path, fileName):
    # Create  characters
    with open(path + fileName, mode='w', encoding='utf-8') as fw:
        fw.write(soup.prettify())

# Create random string
def random_string(length, seq='0123456789abcdefghijklmnopqrstuvwxyz'):
    sr = random.SystemRandom()
    return ''.join([sr.choice(seq) for i in range(length)])

# Replay Escape string
def replaceEscapeHtmlString(filename):
    # Read in the file
    with open(filename, 'r') as file :
        filedata = file.read()
        
    # Replace the target string
    filedata = filedata.replace('&lt;', '<')
    filedata = filedata.replace('&gt;', '>')

    # Write the file out again
    with open(filename, 'w') as file:
        file.write(filedata)

