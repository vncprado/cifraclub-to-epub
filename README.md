# Cifraclub to epub

Usage:
    
    python3.7 cifraclub-to-epub.py music_list.txt

The script looks for [cifraclub.com.br](https://www.cifraclub.com.br/) urls in `music_list.txt`.  
The script uses the order from the file.
The final file will be called `<file_name>.epub`

You probably need to install `bs4` and `ebooklib`.

You can copy or send the resulting `music_list.epub` to your reader. Tested on Kindle paperwhite, that currently accepts epub, but probably would work in any epub compatible reader.
