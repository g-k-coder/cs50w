import regex

from . import util

""" 
    Challenge for those more comfortable: 

    If you’re feeling more comfortable, 
    try implementing the Markdown to HTML conversion 
    without using any external libraries, supporting 
    headings, 
    boldface text, 
    unordered lists, 
    links, and 
    paragraphs. 


    You may find using regular expressions in Python helpful.
"""

def convert_headings(string):
    """ #, ..., ###### => h1, ..., h6 """
    """ 
        <h1>...</h1> 
        ...
        <h6>...</h6>   
    """
    
    # '\s' included in regex pattern b\c #'s are not recognized as a heading 
    # if not immediately followed by whitespace character
    
    try:
        # regex.findall() creates an iterable, i.e., list
        headings = regex.findall(r'^#{1,6}\s', 
                                 string)
        
        heading = len(headings)
    # If no match return string 
    except TypeError:
        return False
    else:
        if not heading:
            return False
    
    # Heading size
    heading = len(headings[0]) - 1
    
    # Remove
    string = string.replace(headings[0][0:heading+1], '')
         
    return f"<h{heading}>{string}</h{heading}>"


def convert_links(string):
    """ [text](URL) => href=URL, anchor tag text=text """
    """ <a href="...">***</a> """
    
    try:
        links = regex.findall(r'(\[\S+\]\(\S+\)){1}', 
                              string.replace(')[', ') ['))
                
        check_if_None = len(links)
    # If no match return string 
    except TypeError:
        return False
    else:
        if not check_if_None:
            return False
    
    for link in links:
        tags = link.split('](')
        
        string = string.replace(link, 
                                f"<a href=\"{tags[1].replace(')', '')}\">{tags[0].replace('[', '')}</a>")
         
    return string


def convert_ulists(string):
    """ 
        <ul>
            <li>...</li>
            ...
            <li>...</li>
        </ul>
    """
        
    try:
        ul = regex.findall(r'^(\*|\+|\-)\s', 
                           string)
        
        li = len(ul)
    # If no match return string 
    except TypeError:
        return False
    else:
        if not li:
            return False
    
    return f"<li>{string[2:]}</li>"
    
    
#? DONE
def convert_bold(string):
    """ **|__text**|__ => b = **|__, boldface text=text """

    try:
        boldface_txt = regex.findall(r'\*{2}\S+\*{2}|\_{2}\S+\_{2}', 
                                     string)
        
        check_if_None = len(boldface_txt)
    # If no match return string 
    except TypeError:
        return False
    else:
        if not check_if_None:
            return False


    for match in boldface_txt:
        
        string = string.replace(match,
                       # slicing [2:-2] removes tags 
                       f"<b>{match[2:-2]}</b>")

    """  
        ---- <b>some text</b> ----
    """
    
    return string


def convert_to_html(title):
    # Get entries markdown content and convert it into a list
    html_content = ""
    content = util.get_entry(title).split('\n')
    
    for line in content:
        headings = convert_headings(line)
        if headings:
            line = headings
        
        links = convert_links(line)
        if links:
            line = links
        
        ul = convert_ulists(line)
        if ul:
            line = f"<ul>{ul}</ul>"    
            
        html_content += line
        
    
    return html_content

    