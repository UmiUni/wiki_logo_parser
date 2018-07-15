"""
@author: ni da ye
@date: 7/15/2018
"""

import os
import re
import sys
import pandas as pd


def getWikiUrl(key):
    from googlesearch import search
    query = key + " logo svg wiki"
    for url in search(query, tld="co.in", num=5, stop=1, pause=2):
        if ("wiki" in url.lower()) and ("_logo.svg" in url.lower()) and ("file:" in url.lower()):
            return url
    return None


def getSvgUrl(page_url):
    import httplib2
    from bs4 import BeautifulSoup, SoupStrainer
    
    http = httplib2.Http()
    status, response = http.request(page_url)
    links = []

    for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
        if 'href' in getattr(link, 'attrs', {}):
            links.append(link['href'])
    svgs = [link for link in links if (link.lower()[-4:] == '.svg') and ("file:" not in link.lower()) and ("upload" in link.lower())]
    if not svgs:
        return None
    print("Get SVG Link:")
    print(svgs[0] + "\n")
    return svgs[0]


def downLoadSvg(svg_url, filename):
    if svg_url[:2] == "//":
        svg_url = "https:" + svg_url
    try:
        stat = os.system("curl -O " + svg_url)
        os.rename(svg_url.split("/")[-1], filename)
        return filename
    except:
        pring("Fail to download svg from " + svg_url)
        return None


if __name__ == "__main__":
    if not os.path.exists("logos"):
        os.makedirs('logos')
    assert len(sys.argv) > 1, "Need Input Csv file"
    df = pd.read_csv(sys.argv[1])
    logo_wiki_page = []
    logo_src = []
    download_status = []
    for key in df['School Name'].tolist():
        print("=" * 50)
        print("Processing query for " + key)
        keyname = " ".join(re.findall("[a-zA-Z]+", key)).replace(" ", '_')
        path = "logos/" + keyname
        if not os.path.exists(path):
            os.makedirs(path)
        filename = path + "/" + keyname +".svg"
        page_url = getWikiUrl(key)
        if not page_url:
            logo_wiki_page.append("Missing")
            logo_src.append("Missing")
            download_status.append("Fail")
            print("Get missing wiki page!")
            continue
        logo_wiki_page.append(page_url)
        svg_url = getSvgUrl(page_url)
        if not svg_url:
            logo_src.append("Missing")
            download_status.append("Fail")
            print("Did not find svg src!")
            continue
        logo_src.append(svg_url)
        stat = downLoadSvg(svg_url, filename)
        if not stat:
            download_status.append("Fail")
        else:
            download_status.append("Success")
