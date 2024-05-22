"""
main.py

Description:
A program for use with the "Chordinator", a device to help people learn guitar.

How it works:
Songs are taken as input (using ChordU JSON data or MIDI files???)
Then, each chord diagram with appropriate colors corresponding to fingers is displayed
on a display comprised of multiple neopixel strips next to the guitar neck.
Additionally, the chord name is displayed on an OLED display above the diagram.

Author: Benjamin Chase
Programmed in March-April 2024 (original March 24, 2024)
"""

# modules for music analysis/MIDI files
import pychord
import mido
#import music21
#import musicpy



# OLED display, custom module, based upon luma.oled
from display import Display


# for buttons
from gpiozero import Button


# for neopixels, uses Adafruit Blinka CircuitPython
# See https://learn.adafruit.com/neopixels-on-raspberry-pi
import board
import neopixel


fret_display_pin = board.D12
num_pixels = 40
pixel_order = neopixel.GRB
pixel_brightness = 0.05 # can adjust to lower or higher (probably between 0.01 and 1.0), higher is brighter

fret_display = neopixel.NeoPixel(
    fret_display_pin, num_pixels, brightness=pixel_brightness, auto_write=False, pixel_order=pixel_order
)

# RGB colors
RED = (255, 0, 0)
ORANGE = (252, 104, 5)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
VIOLET = (255, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# clear neopixels
fret_display.fill(BLACK)


import time


def set_fret(index, color):
    #neopixel_ids = [range(0,8), range(8,16,-1),range(16,24),range(24,32,-1),range(32,40)]
    #fret_display()
    """
    neopixel_ids = list(
        list(range(5,-1,-1))+
        list(range(12,7,-1))+
        list(range(19,14,-1))+
        list(range(26,21,-1))+
        list(range(33,28,-1))
    )
    """
    neopixel_ids = [
        5,   4,  3,  2,  1,  0,
        13, 12, 11, 10,  9,  8,
        21, 20, 19, 18, 17, 16,
        29, 28, 27, 26, 25, 24,
        37, 36, 35, 34, 33, 32
    ]
    #print(neopixel_ids)
    fret_display[neopixel_ids[index]] = color

'''
frets_list = list(range(0,32))
for i in frets_list:
    set_fret(i, BLUE)
    fret_display.show()
    time.sleep(0.25)
'''


def chord_to_positions(chord):
    """Converts chord names to finger positions on guitar."""

    with open('chord_chart.txt') as chord_chart:
        txt_data = [x.replace('\n', '') for x in chord_chart.readlines()]
        chord_names = txt_data[::5]
        chord_positions = txt_data[1::]

        for t in chord_positions[4::5]: # remove all chord names from chord data
            chord_positions.remove(t)

        chord_positions_list = [chord_positions[i:i+4] for i in range(0, len(chord_positions)-3, 4)]


        #for c in chord_positions:
        #    print(c)
    #print(notes_data)
    output_chord = []
    #for chord_num in range(len(chord_data)):
        #print()
        #print('Midi Note Number: ' + notes_data[chord_num])
    for fret in chord_positions_list[chord_names.index(chord)]:
        output_chord.append(fret)#list(fret))
    #print('  ||||||')
    return output_chord


#midi_file = mido.MidiFile("test.mid")

#midi_notes = []
#guitar_positions = []

"""
song = [
    'Bm',
    'G',
    'E',
    'Bbm',
    'B',
    'G',
    'E',
    'D',
    'Cm',
    'G',
    'Cm',
    'Ab',
    'Bm'
]

for chord in song:
    c = pychord.Chord(chord)
    print(c.components_with_pitch(root_pitch=0))
"""

def main():
    try:
        """ main function for most code """
        # chord = "C sharp major"
        with open('chord_chart.txt') as chord_chart:
            txt_data = [x.replace('\n', '') for x in chord_chart.readlines()]
            chord_names = txt_data[::5]
            for chord in chord_names:
                #time.sleep(1)
                input("Press ENTER to continue ")
                Display.write(chord)
                print("\n\n\n" + chord)
                # clear display between chords, but don't show it yet
                fret_display.fill(BLACK)

                # get chord finger positions
                fret_index = 0
                string_index = 0
                neopixel_index = 0
                not_played_strings = []
                #print(chord_to_positions(chord))

                for fret in chord_to_positions(chord):
                    print(fret)
                    #print(neopixel_index+5)
                    string_index = 0
                    for string in fret:
                        if fret_index == 0:
                            if string == "x": # not played string = red
                                set_fret(neopixel_index, RED)
                                set_fret(neopixel_index+6, RED)
                                not_played_strings.append(string_index)
                            else:
                                set_fret(neopixel_index, GREEN) # string is played, open or not open = green
                        if string_index in not_played_strings: # mark entire not played string red
                            set_fret(neopixel_index+6, RED)
                        elif string == "1": # 1 on string, index finger
                            set_fret(neopixel_index+6, ORANGE)
                        elif string == "2": # 2 on string, middle finger
                            set_fret(neopixel_index+6, YELLOW)
                        elif string == "3": # 3 on string, ring finger
                            set_fret(neopixel_index+6, BLUE)
                        elif string == "4": # 4 on string, pinky
                            set_fret(neopixel_index+6, VIOLET) # really looks more like pink
                        else: # 0 on string, turn LED off
                            if fret_index == 0:
                                set_fret(neopixel_index, GREEN) # show strings to play green
                            else:
                                set_fret(neopixel_index+6, BLACK) # no finger and not used to display open string = off
                        #fret_display.show()
                        #time.sleep(0.2)

                        string_index += 1
                        neopixel_index += 1

                    fret_index += 1
                fret_display.show()

        """
        for i, track in enumerate(midi_file.tracks):
            #print(f'Track {i}: {track.name}')
            for msg in track:
                if 'note_on' in str(msg):
                    if msg.time > 1:
                        #print(str(x) + '   ' + str(msg) + "\n")
                        #x += 1
                        print()
                        print(f'{msg.time / 1000} Seconds')
                        for fret in note_to_chord(msg.note):
                            print(list(fret))
                            for string in range(len(list(fret))):
                                value = list(fret)[string]
                                if value == '1':
                                    # turn that neopixel on
                                    pass
                                elif value == '0':
                                    # turn that neopixel off
                                    pass
        """
        time.sleep(1)
        fret_display.fill(BLACK)
        fret_display.show()
    except KeyboardInterrupt:
        print("\n\nStopped by user...\n\n")
        time.sleep(1)
        fret_display.fill(BLACK)
        fret_display.show()


if __name__ == "__main__":
    main()
