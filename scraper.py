import re
import time
import requests
from bs4 import BeautifulSoup


VERIFY = False # verify SSL certificates, change to True ASAP, just for testing

# song name to search
#song_name = "Over the Rainbow" # non-standard format
#song_name = "regen enno bunger" # long test
#song_name = "enno bunger konfetti" # long test
#song_name = "Ode to Joy" # short test
#song_name = "Pirates of the Caribbean" # will load a tab instead of chords
#song_name = "Bridged By a Lightwave" # fast, medium length
#song_name = "hotel california" # long test

def get_chords(song_name):
    print(f'Searching for "{song_name}"')

    song_name = song_name.lower().replace(" ", "+")


    # go to freetar.de
    # alternates are: (in case the server goes down)
    # https://freetar.habedieeh.re
    # https://tabs.adast.dk
    base_url = "https://freetar.de"
    url = f"{base_url}/search?search_term={song_name}"
    page = requests.get(url, verify=VERIFY)

    soup = BeautifulSoup(page.content, "html.parser")

    song_links = []
    song_classes = soup.find_all(class_="song")

    for song in song_classes:
        song_links.append(song.findChild("a").unwrap())

    print(f'Found "{base_url + song_links[0].get("href")}", visiting...') # choose first song


    # go to first song
    song_soup = BeautifulSoup(requests.get(base_url + song_links[0].get("href"), verify=VERIFY).content, "html.parser")
    print("\n\n")


    # get the html 'div' element containing the chord and lyric data
    song_text_list = song_soup.find(name="div", class_="tab font-monospace") #.find_all("br")



    # for getting chords and whitespace
    # whitespace is used for timing

    for br in song_text_list.find_all("br"):
        br.replace_with("\n")

    song_text = song_text_list.text

    # remove those pesky completely empty lines
    song_text = '\n'.join(x for x in song_text.split('\n\n') if x != '\n')

    def is_chord_line(line):
        '''
        Detect if a line represents chords or other text.
        This is known by whether at least half of the text
        in the line is whitespace.
        '''
        s = '\xa0' # a space

        if line.count(s) >= (len(line) - line.count(s)): # change to < for lyrics only
            return True
        elif line.count(s) == 0 and len(line) < 5: # only one chord on the line
            return True
        else:
            return False


    song_text_lines = song_text.split('\n')

    #print(song_text_lines)
    song_chords = ''

    for i in range(len(song_text_lines)):
        line = song_text_lines[i]
        if is_chord_line(line):
            if i != len(song_text_lines) - 1:
                # not the last line,
                # add additional spaces for correct timing as
                # chord is not at the end of the line
                song_chords += line + (len(song_text_lines[i+1]) - len(line)) * ' ' + '\n'
            else:
                # last line, meaning additional outro chords
                song_chords += line + '\n'


    #song_chords = '\n'.join(x for x in song_text.split('\n') if is_chord_line(x))



    #song_chords = ''.join('\n'.join(song_text.split('[Verse')[1:]).split("\n")[1::2])

    #print('\n' * 10 + song_chords)


    char_list = list(song_chords)
    chords_list = []

    for i in range(len(char_list)):
        char = char_list[i]

        if ((i != 0 and char != '/' and char_list[i-1] != '/' and char_list[i-2] != '/' and char_list[i-3] != '/') or (i == 0 and char != '/')) and char != '\n' and char != 'x':
            # is not a newline character
            # it must be a chord or a space
            # spaces are kept for time reference
            if char == 'm' or char == '#' or char == 'b':
                # minor, sharp, or flat
                chords_list[-1] += char
            elif char.isdigit():
                # 7th not supported yet
                #print("7ths and such are not supported yet, sorry")
                print(end="")
            elif any([char == l for l in "acdefghijklnopqrstuvwxyz!@$%^&*()-_=+HIJKLMNOPQRSTUVWXYZ<>,.;:'\"?\\"]): # tries to get rid of maj, add, sus
                # not supported yet
                print(end="")
            elif char == "\xa0m":
                print(end="")
            else:
                chords_list.append(char)
        #time.sleep(0.5)



    #for chord in chords_list:
    #    if chord != '\xa0' and chord != ' ':
    #        #if chord != ' ':
    #        # it is not a space:
    #        print("\n"*20 + chord)
    #    time.sleep(0.2) # wait a little in between if there is a space
    return chords_list
