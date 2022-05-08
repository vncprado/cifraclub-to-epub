# Usage: python3.7 cifraclub-to-epub.py music_list.txt
# The script looks for cifraclub.com.br urls in "music_list.txt"
# The order created is the order from the file

import argparse
import requests
from bs4 import BeautifulSoup
from ebooklib import epub

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('music_list_file')

if __name__ == '__main__':
    music_list_file = arg_parser.parse_args().music_list_file

    with open(music_list_file) as file:
        musics = file.readlines()
        musics = [line.rstrip() for line in musics]

    music_dict = {}
    ord = 0
    for music in musics:
        cur_dict = {}
        raw_html = requests.get(music + "/imprimir.html#tabs=false&instrument=cavaco&footerChords=false")
        soup = BeautifulSoup(raw_html.content, features="html.parser")
        data = soup.find('div', id="folha1")
        text = data.find('pre')
        header = data.find('div', class_="cifra_header js-cifra_header")
        title = header.find('h1', class_="t1").find('a').get_text()
        artist = header.find('h2', class_="t2").find('a').get_text()
        # composer = header.find('small').get_text()
        tone = data.find('span', id="cifra_tom").get_text().split()[-1]

        cur_dict["text"] = text
        cur_dict["title"] = title
        cur_dict["artist"] = artist
        cur_dict["tone"] = tone
        cur_dict["url"] = music
        # cur_dict["composer"] = composer

        music_dict[ord] = cur_dict
        print(f"Downloaded: {title} - {artist}")
        ord += 1

    book = epub.EpubBook()
    book.set_identifier('')
    book.set_title(f'{music_list_file.split(".")[0]}'.capitalize())
    book.set_language('pt-br')
    book.add_author('Vinicius Prado da Fonseca')

    chapter_list = []
    for ord in range(len(music_dict)):
        music = music_dict[ord]

        text = music["text"]
        title = music["title"]
        artist = music["artist"]
        tone = music["tone"]
        url = music["url"]
        # composer = music["composer"]

        c = epub.EpubHtml(title=f'{title} - {artist}',
                          file_name=f'{title} - {artist}.xhtml',
                          lang='pt-br')

        content = u'<html><body>' + '<br/>' +\
            str(title) + '<br/>' +\
            str(artist) + '<br/>' +\
            "Tom: " + str(tone) + '<br/>' +\
            str(text) + '</body></html>'
        c.set_content(content)

        book.add_item(c)
        chapter_list.append(c)

    style = ''
    # style = 'body { font-family: Times, Times New Roman, serif; }'

    nav_css = epub.EpubItem(uid="style_nav",
                            file_name="style/nav.css",
                            media_type="text/css",
                            content=style)
    book.add_item(nav_css)

    book.toc = ((epub.Section('Musics'),
                tuple(chapter_list)
                 ),
                )

    book.spine = ['nav'] + chapter_list

    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    print("Saving file:", music_list_file.split(".")[0] + ".epub")
    epub.write_epub(music_list_file.split(".")[0] + ".epub", book, {})
