import random
from midiutil import MIDIFile
from music21 import *

song = MIDIFile(1)
track = 0

time = 0
song.addTrackName(track, time, "100% Made by a Human")

channel = 0

song.addTempo(track, time, 120)

majorKeys = ['C', 'D', 'E', 'F', 'G', 'A', 'B', 'C#', 'D#', 'F#', 'G#', 'A#']
minorKeys = ['C', 'D', 'E-', 'F', 'G', 'A-',
             'B-', 'C#', 'D#', 'F#', 'G#', 'A#']

# Randomly picks a major or minor key


def randomKey():
    if (random.randint(0, 2) == 1):
        return 'M' + random.choice(majorKeys)
    return 'm' + random.choice(minorKeys)


def generateNotesOfKey(key):
    # Major key
    if (key[0] == 'M'):
        return [note.name for note in scale.MajorScale(songKey[1:]).getPitches()]
    # Minor key
    return [note.name for note in scale.MinorScale(songKey[1:]).getPitches()]


restOptions = [0, 0, 0.5, 1, 1, 1.5, 2, 2, 3.5, 4, 4]
noteLengthOptions = [0.25, 0.5, 1, 1.25, 1.5, 2.25, 2.5, 3, 3.5, 4]
intervalOptions = ['P1', 'm3', 'M3', 'P4', 'P5', 'm6', 'M6']


def generateRest():
    if (random.randint(0, 10) == 1):
        return random.choice(restOptions)
    return 0

# 75% of the time return the prev_duration param, the rest randomly generate a new duration


def generateDuration(prev_duration):
    if (random.randint(0, 4) == 1):
        return prev_duration
    return random.choice(noteLengthOptions)

# 50% of the time return the prev_interval param, the rest randomly generate a new inteval


def generateInterval(prev_interval):
    if (prev_interval == "P1"):
        if (random.randint(0, 10) == 1):
            return prev_interval
    elif (random.randint(0, 2) == 1):
        return prev_interval
    return random.choice(intervalOptions)


songKey = randomKey()
print(songKey)
scale = generateNotesOfKey(songKey)

'''
pitch = 60           # C4 (middle C)
time = 0             # start on beat 0
duration = 1         # 1 beat long
mf.addNote(track, channel, pitch, time, duration, volume)
'''

# Options for every note to pick from

workingTime = 0  # The "write" position of the program

# Randomly pick a note in the scale, and assign as the first note for maxiumum awesomeness (I think)
firstNote = note.Note(
    random.choice(scale) + str(random.randint(3, 5)))
print("First note: " + firstNote.nameWithOctave)

noteLength = random.choice(noteLengthOptions)


# Add the first note to the midi file
song.addNote(track, channel, firstNote.pitch.midi,
             workingTime, noteLength, random.randint(50, 120))

# Randomly select a rest time
restTime = generateRest()

workingTime += (noteLength + restTime)

notesInSong = random.randint(100, 1000)

previousNote = firstNote
previousNoteDuration = noteLength
previousInterval = random.choice(intervalOptions)

for i in range(notesInSong):
    print("Generating note number " + str(i))
    intervalToUse = generateInterval(previousInterval)
    transpositionInHalfSteps = interval.Interval(
        intervalToUse).semitones
    # Make transpositionInHalfSteps negative 50% of the time
    if (random.randint(0, 1) == 1):
        transpositionInHalfSteps *= -1
    print("Transposition (Semitones): " + str(transpositionInHalfSteps))
    workingNote = previousNote.transpose(transpositionInHalfSteps)
    notePlayTime = generateDuration(previousNoteDuration)
    noteDynamic = random.randint(50, 120)
    song.addNote(track, channel, workingNote.pitch.midi,
                 workingTime, notePlayTime, noteDynamic)
    workingTime += (notePlayTime + generateRest())
    previousNoteDuration = notePlayTime
    previousInterval = intervalToUse
    print("Note: " + workingNote.nameWithOctave)
    print("\n")

with open(str(input("filename: ") + ".mid"), "wb") as output_file:
    song.writeFile(output_file)
