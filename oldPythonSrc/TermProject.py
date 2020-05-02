from tkinter import *
import random, copy, pyaudio, wave, os
from threading import *
from pydub import AudioSegment


##Classes
#a note has a pitch, octave, and length
class Note(object):
    def __init__(self, pitch, octave, length):
        self.pitch = pitch
        self.octave = octave
        self.length = length
        self.longRadius = 6
        self.shortRadius = 4
        self.stemLength = 35
        self.x = None
        self.y = None
    
    def __repr__(self):
        return "[%s, %d, %.4f]" % (self.pitch, self.octave, self.length)
        
    def __eq__(self, other):
        return (isinstance(other, Note) and self.pitch == other.pitch and \
                self.octave == other.octave and \
                self.length == other.length and \
                self.x == other.x and self.y == other.y)
    
    def noteData(self):
        return [self.pitch, self.octave, self.length]

    def play(self):
        letter = self.pitch
        octave = self.octave
        file = "PianoKeys/" + str(letter) + str(octave) + ".wav"
        play(file)
    
    def drawWholeNote(self, canvas, x, y):
        canvas.create_oval(x - self.longRadius, y - self.shortRadius, 
                    x + self.longRadius, y + self.shortRadius, width = 2)
        canvas.create_oval(x - self.longRadius + 2, y - self.shortRadius, 
                    x + self.longRadius - 2, y + self.shortRadius, width = 2)
    
    def drawHalfNote(self, canvas, x, y, stemUp):
        canvas.create_oval(x - self.longRadius, y - self.shortRadius, 
                        x + self.longRadius, y + self.shortRadius, width = 1)  
        if stemUp == True and self.octave < 5 and not (self.pitch == "B" and \
                                            self.octave == 4):     #stem is up
            canvas.create_line(x + self.longRadius, y, x + self.longRadius, 
                                y - self.stemLength, width=1)
        else:               #stem is down
            canvas.create_line(x - self.longRadius, y, x - self.longRadius, 
                                y + self.stemLength, width=1)
            
    def drawQuarterNote(self, canvas, x, y, stemUp):
        canvas.create_oval(x - self.longRadius, y - self.shortRadius, 
                        x + self.longRadius, y + self.shortRadius, fill="black")  
        if stemUp == True and self.octave < 5 and not (self.pitch == "B" and \
                                            self.octave == 4):     #stem is up
            canvas.create_line(x + self.longRadius, y, x + self.longRadius, 
                                y - self.stemLength, width=1)
        else:               #stem is down
            canvas.create_line(x - self.longRadius, y, x - self.longRadius, 
                                y + self.stemLength, width=1)
            
    def drawEighthNote(self, canvas, x, y, stemUp):
        canvas.create_oval(x - self.longRadius, y - self.shortRadius, 
                        x + self.longRadius, y + self.shortRadius, fill="black")
        if  stemUp == True and self.octave < 5 and not (self.pitch == "B" and \
                                            self.octave == 4):     #stem is up
            canvas.create_line(x + self.longRadius, y, x + self.longRadius, 
                                y - self.stemLength, width=1)
            canvas.create_arc(x + self.longRadius - 6, y - self.stemLength, 
                        x + self.longRadius + 6, y - self.stemLength + 18, 
                                            extent=90, style=ARC, width=1)
        else:      #stem is down
            canvas.create_line(x - self.longRadius, y, x - self.longRadius, 
                                y + self.stemLength, width=1)
            canvas.create_arc(x - self.longRadius - 6, y + self.stemLength - 18, 
                                x - self.longRadius + 6, y + self.stemLength, 
                                extent=90, style=ARC, width = 1, start=180)
    
    def drawSixteenthNote(self, canvas, x, y, stemUp):
        canvas.create_oval(x - self.longRadius, y - self.shortRadius, 
                        x + self.longRadius, y + self.shortRadius, fill="black")
        
        if stemUp == True and self.octave < 5 and not (self.pitch == "B" and \
                                            self.octave == 4):     #stem is up
            canvas.create_line(x + self.longRadius, y, x + self.longRadius, 
                                y - self.stemLength, width=1)
            canvas.create_arc(x + self.longRadius - 6, y - self.stemLength, 
                            x + self.longRadius + 6, y - self.stemLength + 18, 
                                            extent=90, style=ARC, width=1)
            canvas.create_arc(x + self.longRadius - 6, y - self.stemLength + 8, 
                            x + self.longRadius + 6, y - self.stemLength + 26, 
                                extent=90, style=ARC, width=1)
        else:               #stem is down
            canvas.create_line(x - self.longRadius, y, x - self.longRadius, 
                                y + self.stemLength, width=1)
            canvas.create_arc(x - self.longRadius - 6, y + self.stemLength - 18, 
                                x - self.longRadius + 6, y + self.stemLength, 
                                extent=90, style=ARC, width = 1, start=180)
            canvas.create_arc(x - self.longRadius - 6, y + self.stemLength - 26,
                            x - self.longRadius + 6, y + self.stemLength - 8, 
                            extent=90, style=ARC, width = 1, start=180)
    
    def drawWholeRest(self, canvas, x, y):
        icon = PhotoImage(file="Images/wholeRest.png")
        rest = Label(image = icon)
        rest.image = icon
        rest.pack
        canvas.create_image(x + 120, y - 7, image=icon)
        
    def drawHalfRest(self, canvas, x, y):
        icon = PhotoImage(file="Images/halfRest.png")
        rest = Label(image = icon)
        rest.image = icon
        rest.pack
        canvas.create_image(x, y - 3, image=icon)
    
    def drawQuarterRest(self, canvas, x, y):
        icon = PhotoImage(file="Images/quarterRest.png")        
        rest = Label(image = icon)
        rest.image = icon
        rest.pack
        canvas.create_image(x, y, image=icon)
        
    def drawEighthRest(self, canvas, x, y):
        icon = PhotoImage(file="Images/eighthRest.png")        
        rest = Label(image = icon)
        rest.image = icon
        rest.pack
        canvas.create_image(x, y + 3, image=icon)
        
    def drawSixteenthRest(self, canvas, x, y):
        icon = PhotoImage(file="Images/sixteenthRest.png")        
        rest = Label(image = icon)
        rest.image = icon
        rest.pack
        canvas.create_image(x, y + 7, image=icon)

    def draw(self, canvas, x, y, stemUp=True):
        if self.length == 1:        #whole
            if self.pitch == "0" and self.octave == 0:
                self.drawWholeRest(canvas, x, y)
            else:
                self.drawWholeNote(canvas, x, y)
        elif self.length == 1/2:      #half
            if self.pitch == "0" and self.octave == 0:
                self.drawHalfRest(canvas, x, y)
            else:
                self.drawHalfNote(canvas, x, y, stemUp)
        elif self.length == 1/4:      #quarter
            if self.pitch == "0" and self.octave == 0:
                self.drawQuarterRest(canvas, x, y)
            else:
                self.drawQuarterNote(canvas, x, y, stemUp)
        elif self.length == 1/8:      #eighth
            if self.pitch == "0" and self.octave == 0:
                self.drawEighthRest(canvas, x, y)
            else:
                self.drawEighthNote(canvas, x, y, stemUp)
            
        elif self.length == 1/16:     #sixteenth
            if self.pitch == "0" and self.octave == 0:
                self.drawSixteenthRest(canvas, x, y)
            else:
                self.drawSixteenthNote(canvas, x, y, stemUp)

    def moveNoteUpTreble(self, keySignature):
        if self.pitch[0] != "C" or self.octave != 6:
            index = getElementLocation(keySignature, self.pitch)
            newIndex = index + 1
            if newIndex == 7:
                newIndex = 0
            newLetter = keySignature[newIndex]
            if newLetter[0] == "C":
                self.pitch = newLetter
                self.octave += 1
            else:
                self.pitch = newLetter
        
    def moveNoteDownTreble(self, keySignature):
        if self.pitch[0] != "A" or self.octave != 3:
            index = getElementLocation(keySignature, self.pitch)
            newIndex = index - 1
            if newIndex == -1:
                newIndex = 6
            newLetter = keySignature[newIndex]
            if newLetter[0] == "B":
                self.pitch = newLetter
                self.octave -= 1
            else:
                self.pitch = newLetter
                
    def moveNoteUpBass(self, keySignature):
        if self.pitch[0] != "F" or self.octave != 4:
            index = getElementLocation(keySignature, self.pitch)
            newIndex = index + 1
            if newIndex == 7:
                newIndex = 0
            newLetter = keySignature[newIndex]
            if newLetter[0] == "C":
                self.pitch = newLetter
                self.octave += 1
            else:
                self.pitch = newLetter
    
    def moveNoteDownBass(self, keySignature):
        if self.pitch[0] != "C" or self.octave != 2:
            index = getElementLocation(keySignature, self.pitch)
            newIndex = index - 1
            if newIndex == -1:
                newIndex = 6
            newLetter = keySignature[newIndex]
            if newLetter[0] == "B":
                self.pitch = newLetter
                self.octave -= 1
            else:
                self.pitch = newLetter

#a measure has notes
class Measure(object):
    def __init__(self, notes):
        self.notes = []
        
    def __repr__(self):
        string = ""
        for note in self.notes:
            string += str(note)
        return "[%s]" % string

    #x is beginning at barline and y is 'E' line
    def trebleDraw(self, canvas, x, y): 
        noteLocationDict = {
        ("A", 3): 20,
        ("B", 3): 15,
        ("C", 4): 10,
        ("D", 4): 5,
        ("E", 4): 0,
        ("F", 4): -5,
        ("G", 4): -10,
        ("A", 4): -15,
        ("B", 4): -20,
        ("C", 5): -25,
        ("D", 5): -30,
        ("E", 5): -35,
        ("F", 5): -40,
        ("G", 5): -45,
        ("A", 5): -50,
        ("B", 5): -55,
        ("C", 6): -60
                        }
        xSpacer = 0
        for i in range(len(self.notes)):
            note = self.notes[i]
            pitch = note.pitch[0]
            octave = note.octave
            if pitch == "0" and octave == 0:
                length = note.length
                yVal = y + -20
                note.x = x + xSpacer
                note.y = yVal
                note.draw(canvas, x + xSpacer, yVal)
            else:
                length = note.length
                yVal = y + noteLocationDict[(pitch, octave)]
                note.draw(canvas, x + xSpacer, yVal)
                note.x = x + xSpacer
                note.y = yVal
                #accounts for ledger lines
                if yVal == y + -50:
                    canvas.create_line(x + xSpacer - 10, yVal, x + xSpacer + 10, 
                                                                        yVal)
                elif yVal == y + -55:
                    canvas.create_line(x + xSpacer - 10, yVal + 5, 
                                        x + xSpacer + 10, yVal + 5)
                elif yVal == y + -60:
                    canvas.create_line(x + xSpacer - 10, yVal, x + xSpacer + 10, 
                                                                        yVal)
                    canvas.create_line(x + xSpacer - 10, yVal + 10, 
                                                x + xSpacer + 10, yVal + 10)
                elif yVal == y + 10:
                    canvas.create_line(x + xSpacer - 10, yVal, x + xSpacer + 10, 
                                                                        yVal)
                elif yVal == y + 15:
                    canvas.create_line(x + xSpacer - 10, yVal - 5, 
                                        x + xSpacer + 10, yVal - 5)
                elif yVal == y + 20:
                    canvas.create_line(x + xSpacer - 10, yVal, x + xSpacer + 10, 
                                                                        yVal)
                    canvas.create_line(x + xSpacer - 10, yVal - 10, 
                                                x + xSpacer + 10, yVal - 10)
            xSpacer += 240 * length

    #x is beginning at barline and y is 'G' line
    def bassDraw(self, canvas, x, y):
        noteLocationDict = {
        ("C", 2): 20,
        ("D", 2): 15,
        ("E", 2): 10,
        ("F", 2): 5,
        ("G", 2): 0,
        ("A", 2): -5,
        ("B", 2): -10,
        ("C", 3): -15,
        ("D", 3): -20,
        ("E", 3): -25,
        ("F", 3): -30,
        ("G", 3): -35,
        ("A", 3): -40,
        ("B", 3): -45,
        ("C", 4): -50,
        ("D", 4): -55,
        ("E", 4): -60,
        ("F", 4): -65
                        }
        xSpacer = 0
        tracker = 0
        for i in range(len(self.notes)):
            note = self.notes[i]
            pitch = note.pitch[0]
            octave = note.octave
            if pitch == "0" and octave == 0:
                length = note.length
                yVal = y + -20
                note.x = x + xSpacer
                note.y = yVal
                note.draw(canvas, x + xSpacer, yVal)
            else:
                length = note.length
                yVal = y + noteLocationDict[(pitch, octave)]
                note.draw(canvas, x + xSpacer, yVal, False)
                note.x = x + xSpacer
                note.y = yVal
                #accounts for ledger lines
                if yVal == y + 10:
                    canvas.create_line(x + xSpacer - 10, yVal, x + xSpacer + 10, 
                                                                        yVal)
                elif yVal == y + 15:
                    canvas.create_line(x + xSpacer - 10, yVal - 5, 
                                            x + xSpacer + 10, yVal - 5)
                elif yVal == y + 20:
                    canvas.create_line(x + xSpacer - 10, yVal, x + xSpacer + 10, 
                                                                        yVal)
                    canvas.create_line(x + xSpacer - 10, yVal - 10, 
                                                x + xSpacer + 10, yVal - 10)
                elif yVal == y + -50:
                    canvas.create_line(x + xSpacer - 10, yVal, x + xSpacer + 10, 
                                                                        yVal)
                elif yVal == y + -55:
                    canvas.create_line(x + xSpacer - 10, yVal + 5,
                                            x + xSpacer + 10, yVal + 5)
                elif yVal == y + -60:
                    canvas.create_line(x + xSpacer - 10, yVal, x + xSpacer + 10, 
                                                                        yVal)
                    canvas.create_line(x + xSpacer - 10, yVal + 10, 
                                                x + xSpacer + 10, yVal + 10)
                elif yVal == y + -65:
                    canvas.create_line(x + xSpacer - 10, yVal + 5, 
                                                    x + xSpacer + 10, yVal + 5)
                    canvas.create_line(x + xSpacer - 10, yVal + 15, 
                                                    x + xSpacer + 10, yVal + 15)
            xSpacer += 240 * length
    
#a page takes in 8 measures and draws it
class Page(object):
    def __init__(self, rightHandMeasures, leftHandMeasures, width, height):
        self.rightHandMeasures = rightHandMeasures
        self.leftHandMeasures = leftHandMeasures
        self.width = width
        self.height = height
        
    def getNoteMeasureIndexRightHand(self, target):
        currentMeasureIndex = -1
        for measure in self.rightHandMeasures:
            currentMeasureIndex += 1
            currentNoteIndex = -1
            for note in measure.notes:
                currentNoteIndex += 1
                if note == target:
                    return(currentMeasureIndex, currentNoteIndex)
    
    def getNoteMeasureIndexLeftHand(self, target):
        currentMeasureIndex = -1
        for measure in self.leftHandMeasures:
            currentMeasureIndex += 1
            currentNoteIndex = -1
            for note in measure.notes:
                currentNoteIndex += 1
                if note == target:
                    return(currentMeasureIndex, currentNoteIndex)
                
    def drawFiveLines(self, canvas, y):
        spacing = 10
        sideMargin = 50
        for i in range(5):
            canvas.create_line(sideMargin, y + spacing * i, 
                        self.width - sideMargin, y + spacing * i)
    
    def drawGrandStaff(self, canvas, y, keySignature, timeSignature):
        sideMargin = 50
        self.drawFiveLines(canvas, y)
        self.drawFiveLines(canvas, y + 80)
        canvas.create_line(sideMargin, y, sideMargin, y + 120)
        canvas.create_line(self.width - sideMargin, y, 
                        self.width - sideMargin, y + 120)
        #clefs
        icon1 = PhotoImage(file="Images/trebleClef.png")
        icon2 = PhotoImage(file="Images/bassClef.png")
        #code from 
        #http://effbot.org/pyfaq/why-do-my-tkinter-images-not-appear.htm
        treble = Label(image = icon1)
        treble.image = icon1
        treble.pack
        bass = Label(image = icon2)
        bass.image = icon2
        bass.pack
        canvas.create_image(72, y + 22, image=icon1)
        canvas.create_image(75, y + 100, image=icon2)
        drawKeySignature(canvas, y, keySignature, timeSignature)
        
    
    def drawSheetMusic(self, canvas, keySignature, timeSignature):
        spacing = self.height / 4.5
        for i in range(4):
            self.drawGrandStaff(canvas, 50 + spacing * i, keySignature, 
                                                        timeSignature)
                                                        
            
    def drawRightHand(self, canvas):
        measureSpacer = 260
        #clef buffer accounts for space margin + room for clef, key, 
        #time signature
        clefBuffer = 220
        counter = -1
        multiplier = -1
        #draws each measure in right hand
        for measure in self.rightHandMeasures:
            counter += 1
            #goes to next staff every two measures
            if counter % 2 == 0:  
                multiplier += 1
                counter = 0
            measure.trebleDraw(canvas, clefBuffer + measureSpacer * counter, 
                            90 + multiplier * (self.height / 4.5))
            #Treble: 90 is space margin + 4 lines down (10 each)
            if counter % 2 == 1:    #draws measure lines
                canvas.create_line(460, 170 + multiplier * (self.height / 4.5), 
                            460, 90 + multiplier * (self.height / 4.5) - 40)
                
    def drawLeftHand(self, canvas):
        measureSpacer = 260
        clefBuffer = 220
        counter = -1
        multiplier = -1
        #draws each measure in left hand
        for measure in self.leftHandMeasures:
            counter += 1
            if counter % 2 == 0:
                multiplier += 1
                counter = 0
            measure.bassDraw(canvas, clefBuffer + measureSpacer * counter,
                            170 + multiplier * (self.height / 4.5))
            #Bass: 170 is 90 + space margin
            
        

    def draw(self, canvas, keySignature, timeSignature):
        self.drawSheetMusic(canvas, keySignature, timeSignature)
        self.drawRightHand(canvas)
        self.drawLeftHand(canvas)

class TitlePage(Page):
    def __init__(self, rightHandMeasures, leftHandMeasures, width, height, 
                                                        title, composer):
        super().__init__(rightHandMeasures, leftHandMeasures, width, height)
        self.title = title
        self.composer = composer
    
    def drawTitle(self, canvas):
        canvas.create_text(self.width / 2, 75, text=self.title, font="Arial 50")
    
    def drawComposer(self, canvas):
        canvas.create_text(self.width - 20, 150, text=self.composer, 
                                                font="Arial 15", anchor=E)
    
    def drawRightHand(self, canvas):
        measureSpacer = 260
        #clef buffer accounts for space margin + room for clef, key, 
        #time signature
        clefBuffer = 220
        counter = -1
        multiplier = 0
        #draws each measure in right hand
        for measure in self.rightHandMeasures:
            counter += 1
            #goes to next staff every two measures
            if counter % 2 == 0:  
                multiplier += 1
                counter = 0
            measure.trebleDraw(canvas, clefBuffer + measureSpacer * counter, 
                            90 + multiplier * (self.height / 4.5))
            #Treble: 90 is space margin + 4 lines down (10 each)
            if counter % 2 == 1:    #draws measure lines
                canvas.create_line(460, 170 + multiplier * (self.height / 4.5), 
                                460, 90 + multiplier * (self.height / 4.5) - 40)
                
    def drawLeftHand(self, canvas):
        measureSpacer = 260
        clefBuffer = 220
        counter = -1
        multiplier = 0
        #draws each measure in left hand
        for measure in self.leftHandMeasures:
            counter += 1
            if counter % 2 == 0:
                multiplier += 1
                counter = 0
            measure.bassDraw(canvas, clefBuffer + measureSpacer * counter,
                            170 + multiplier * (self.height / 4.5))
            #Bass: 170 is 90 + space margin
    
    def drawSheetMusic(self, canvas, keySignature, timeSignature):
        spacing = self.height / 4.5
        for i in range(4):
            if i == 0:
                continue
            self.drawGrandStaff(canvas, 50 + spacing * i, keySignature, 
                                                            timeSignature)
        self.drawTitle(canvas)
        self.drawComposer(canvas)
        self.drawRightHand(canvas)
        self.drawLeftHand(canvas)

##Helper Functions:
#returns a triad of the specificed key and chord numeral
def returnTriad(data, key, chordProgressionNumeral):
    result = []
    chordProgressionNumber = \
                        data.romanNumeralTranslation[chordProgressionNumeral]
    result.append(data.keySignatures[key][chordProgressionNumber])
    result.append(data.keySignatures[key][(chordProgressionNumber + 2) % 7])
    result.append(data.keySignatures[key][(chordProgressionNumber + 4) % 7])
    return result

#checks if a measure is complete based on note lengths
def isMeasureFull(measure, timeSignature):
    sum = 0
    for note in measure:
        sum += note.noteData()[2]
    return sum == timeSignature


#calculates the current sum of note lengths
def calculateLengthSum(measure):
    if type(measure) == Measure:        #checks if measure is an object or list
        if len(measure.notes) == 0:
            return 0
        sum = 0
        for note in measure.notes:
            sum += note.noteData()[2]
        return sum
    else:
        if len(measure) == 0:
            return 0
        sum = 0
        for note in measure:
            sum += note[2]
        return sum

#checks if dictionary values add up to 100
def isDictionaryFull(dict):
    sum = 0
    for key in dict:
        sum += dict[key]
    if sum == 100:
        return True
    else:
        return False
    
#checks if all parameters are selected
def isMelodyInputValid(length, leftHandPattern, chordProgression):
    return length != None and leftHandPattern != None \
                        and chordProgression != None
                        
#converts chord progressions to a string
def displayChordProgressions(lst):
    str = ""
    for numeral in lst:
        str = str + numeral + "," + " "
    return str[:-2]
    
#returns the nth spot of an element in a dictionary (or list)
def getElementLocation(dict, elem):
    counter = -1
    for key in dict:
        counter += 1
        if key == elem:
            return counter
            
#returns the nth element in a dictionary
def nthElementDict(dict, n):
    counter = -1
    for key in dict:
        counter += 1
        if counter == n:
            return dict[key]

#creates list of pages based on how many measures are given
def createPages(data, rightHandMeasures, leftHandMeasures):
    currentRightHand = []
    currentLeftHand = []
    pages = []
    for i in range(0, len(rightHandMeasures)):
        currentRightHand.append(rightHandMeasures[i])
        currentLeftHand.append(leftHandMeasures[i])
        if len(currentRightHand) == 8:
            pages.append(Page(currentRightHand, currentLeftHand, data.width, 
                                                                data.height))
            currentRightHand = []
            currentLeftHand = []
    if len(currentRightHand) > 0:
        pages.append(Page(currentRightHand, currentLeftHand, data.width, 
                                                                data.height))
    return pages
    
def createCompletedPages(data, rightHandMeasures, leftHandMeasures):
    currentRightHand = []
    currentLeftHand = []
    pages = []
    while len(pages) == 0:
        #checks if song is shorter than 6 measures
        if len(rightHandMeasures) <= 6:
            upper = len(rightHandMeasures)
        else:
            upper = 6
        for i in range(0, upper):
            currentRightHand.append(rightHandMeasures[i])
            currentLeftHand.append(leftHandMeasures[i])
            #checks if first page is full or no more measures can be placed
            if len(currentRightHand) == upper or upper == len(currentRightHand):
                pages.append(TitlePage(currentRightHand, currentLeftHand, 
                            data.width, data.height, data.title, data.composer))
        if len(rightHandMeasures) <= 6:
            return pages
    currentRightHand = []
    currentLeftHand = []
    #continues to make pages out of remaining measures every 8 measures
    for i in range(6, len(rightHandMeasures)):
        currentRightHand.append(rightHandMeasures[i])
        currentLeftHand.append(leftHandMeasures[i])
        if len(currentRightHand) == 8:
            pages.append(Page(currentRightHand, currentLeftHand, data.width, 
                                                                data.height))
            currentRightHand = []
            currentLeftHand = []
    if len(currentRightHand) > 0:     #creates a page of the remaining measures
        pages.append(Page(currentRightHand, currentLeftHand, data.width, 
                                                                data.height))
    return pages
    
        
    
#returns whether a note is in the right hand
def isNoteInRightHand(note, rightHandMeasures):
    for measure in rightHandMeasures:
        if note in measure.notes:
            return True
    return False
#checks if structure is in a valid format
def isValidStructure(structure):
    for letter in structure:
        if not (letter == "A" or letter == "B" or letter == "C"):
            return False
    return True

#checks if chord progression is in a valid format
def isValidChordProgression(chordProgression):
    try:
        for i in range(len(chordProgression)):
            if chordProgression[i] == ",":
                if chordProgression[i + 1] != " ":
                    return False
        for char in chordProgression.split(", "):
            if char not in ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'i', 
                                        'ii', 'iii', 'iv', 'v', 'vi', 'vii']:
                return False
        return True
    except:
        return False

#checks if left hand pattern is in a valid format
def isValidLeftHandPattern(data, s):
    #tries to convert it, if fails, false
    try:
        pattern = convertLeftHandPattern(s)
        if type(pattern)!= list or len(pattern) != 2 or \
                        type(pattern[0]) != list or type(pattern[1]) != float:
            return False
        #checks if length is a valid note length
        if pattern[1] not in [1/16, 1/8, 1/4, 1/2, 1/1]:
            return False
        num = pattern[1]
        #checks if number of notes given agrees with length of notes
        if int(1 / num) != len(pattern[0]):
            return False
        #checks if number is within 1-9
        for num in pattern[0]:
            if num not in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
                return False
        #adds pattern to dictionary for left hand generation (later)
        data.leftHandPatternTranslation[s] = pattern
        return True
    except:
        return False

#converts user inputted chord progression to a valid format
def convertChordProgression(s):
    list = []
    for char in s.split(", "):
        list.append(char)
    return list
    
    #I, vi, I, v

#converts a string to a valid left hand pattern format
def convertLeftHandPattern(s):
    numbers = ""
    newList = []
    counter = -1
    numerator = 0
    denominator = 0
    firstList = []
    for char in s:      #adds all numbers in first list to numbers string
        counter += 1
        if char.isdigit():
            numbers += char
        elif char == "]":
            break
    for num in numbers:         #creates a list of integers form numbers
        firstList.append(int(num))
    for i in range(counter +1, len(s)):  #converts the 2nd element to a float
        if s[i].isdigit():
            numerator = int(s[i])
            denominator = int(s[i + 2])
            break
    newList.append(firstList)
    newList.append(numerator/denominator)
    return newList
 
#returns tuple of measure and note index of next note
def nextSelect(page, note):
    if isNoteInRightHand(note, page.rightHandMeasures):
        noteMeasureIndex = page.getNoteMeasureIndexRightHand(note)
        noteIndex = noteMeasureIndex[1]
        measureIndex = noteMeasureIndex[0]
        newNoteIndex = noteIndex + 1
        newMeasureIndex = measureIndex
        if newNoteIndex == len(page.rightHandMeasures[measureIndex].notes):
            newMeasureIndex += 1
            newNoteIndex = 0
        if newMeasureIndex != len(page.rightHandMeasures):
            return (newMeasureIndex, newNoteIndex)
        else:
            return (measureIndex, noteIndex)
    else:
        noteMeasureIndex = page.getNoteMeasureIndexLeftHand(note)
        noteIndex = noteMeasureIndex[1]
        measureIndex = noteMeasureIndex[0]
        newNoteIndex = noteIndex + 1
        newMeasureIndex = measureIndex
        if newNoteIndex == len(page.leftHandMeasures[measureIndex].notes):
            newMeasureIndex += 1
            newNoteIndex = 0
        if newMeasureIndex != len(page.leftHandMeasures):
            return (newMeasureIndex, newNoteIndex)
        else:
            return (measureIndex, noteIndex)
            
#returns tuple of measure and note index of previous note
def previousSelect(page, note):
    if isNoteInRightHand(note, page.rightHandMeasures):
        noteMeasureIndex = page.getNoteMeasureIndexRightHand(note)
        noteIndex = noteMeasureIndex[1]
        measureIndex = noteMeasureIndex[0]
        newNoteIndex = noteIndex - 1
        newMeasureIndex = measureIndex
        if newNoteIndex == -1:
            newMeasureIndex -= 1
            newNoteIndex = len(page.rightHandMeasures\
                                                    [newMeasureIndex].notes) - 1
        if newMeasureIndex != -1:
            return (newMeasureIndex, newNoteIndex)
        else:
            return (measureIndex, noteIndex)
    else:
        noteMeasureIndex = page.getNoteMeasureIndexLeftHand(note)
        noteIndex = noteMeasureIndex[1]
        measureIndex = noteMeasureIndex[0]
        newNoteIndex = noteIndex - 1
        newMeasureIndex = measureIndex
        if newNoteIndex == -1:
            newMeasureIndex -= 1
            newNoteIndex = len(page.leftHandMeasures[newMeasureIndex].notes) - 1
        if newMeasureIndex != -1:
            return (newMeasureIndex, newNoteIndex)
        else:
            return (measureIndex, noteIndex)

def play(file):
    CHUNK = 1024 #measured in bytes

    wf = wave.open(file, 'rb')

    p = pyaudio.PyAudio()

    stream1 = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    stream2 = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(CHUNK)

    while len(data) > 0:
        stream1.write(data)
        stream2.write(data)
        data = wf.readframes(CHUNK)

    stream1.stop_stream()
    stream1.close()
    stream2.stop_stream()
    stream2.close()

    p.terminate()

##Generation Functions:
import math

#determines if there's a note that can fit within the current measure
def existsFittingLength(timeSignature, measureNoteLengthSum, choices):
    spaceLeft = timeSignature - measureNoteLengthSum
    for note in choices:
        if note <= spaceLeft:
            return True
    return False

#returns a length based on note allocation and makes sure it doesn't overfill
#the measure
def chooseRandomLength(data, noteAllocation, currentMeasure, timeSignature):
    measureNoteLengthSum = calculateLengthSum(currentMeasure)
    if timeSignature == 1:
        verge = 3/4
    elif timeSignature == 3/4:
        verge = 2/4
    elif timeSignature == 2/4:
        verge = 1/4
    #checks if there's choices left and that there exists a note that can fit
    #within the measure and fill it
    if len(data.lengthChoices) != 0 and existsFittingLength(timeSignature, 
                                    measureNoteLengthSum, data.lengthChoices):
        loop = True
        while loop == True:
            pick = random.choice(data.lengthChoices)
            if measureNoteLengthSum + pick <= timeSignature:
                data.lengthChoices.remove(pick)
                return pick
    else:
        lst = []
        for val in noteAllocation:
            lst.extend(int(noteAllocation[val]) * [val])
        loop = True
        while loop == True:
            tempLength = random.choice(lst)
            if measureNoteLengthSum + tempLength <= timeSignature:
                return tempLength

#makes a list of the note lengths to select from based on note allocation          
def makeChoiceList(data, noteAllocation, length):
    wholeAmount = noteAllocation[1]
    halfAmount = noteAllocation[1/2]
    quarterAmount = noteAllocation[1/4]
    eighthAmount = noteAllocation[1/8]
    sixteenthAmount = noteAllocation[1/16]
    ratio = wholeAmount + (1/2) * halfAmount + (1/4) * quarterAmount + (1/8) * \
                                        eighthAmount + (1/16) * sixteenthAmount
    totalNotes = length / ratio
    numWhole = int(wholeAmount * totalNotes)
    numHalf = int(halfAmount * totalNotes)
    numQuarter = int(quarterAmount * totalNotes)
    numEighth = int(eighthAmount * totalNotes)
    numSixteenth = int(sixteenthAmount * totalNotes)
    choices = []
    choices.extend([1] * numWhole)
    choices.extend([1/2] * numHalf)
    choices.extend([1/4] * numQuarter)
    choices.extend([1/8] * (numEighth))
    choices.extend([1/16] * (numSixteenth))
    data.lengthChoices = choices

#generates a random pitch based on the current chord progression numeral
#and harmony
def choosePitch(data, key, chordProgressionNumeral, harmony):
    randomInteger = random.randint(1, 100)
    notesInChord = returnTriad(data, key, chordProgressionNumeral)
    if 0 < randomInteger <= harmony:
        return random.choice(notesInChord)
    elif harmony < randomInteger <= 100:
        choices = copy.copy(data.keySignatures[key])
        for note in notesInChord:   #removes all chord notes before choosing
            choices.remove(note)
        return random.choice(choices)

#generates a random note with a random length depending on key, chord numeral, 
#and note allocation specification
def generateRandomNote(data, key, chordProgressionNumeral, noteAllocation, 
                    timeSignature, harmony, isFirstNote, currentMeasure=[]):
    noteData = []
    if isFirstNote == True:
        #generates a note of the current chord
        triad = returnTriad(data, key, chordProgressionNumeral)
        noteData.append(random.choice(triad))
    else:          
        #generates a random note within the scale   
        pitch = choosePitch(data, key, chordProgressionNumeral, harmony) 
        noteData.append(pitch)
    noteData.append(5)
    noteData.append(chooseRandomLength(data, noteAllocation, currentMeasure, 
                                                    timeSignature))
    return(noteData)
    
#generates a melodyLength long melody based on key, chordProgression, 
#timeSignature, and noteAllocation and directly stores it
def generateMelody(data, section):
    if section == "Melody":
        parameters = [data.key, data.timeSignature, data.chordProgression, 
                        data.noteAllocation, data.melodyLength, 
                        data.melodyRepetition, data.melodyHarmony]
    elif section == "Development":
        parameters = [data.key, data.timeSignature, 
                        data.developmentChordProgression, 
                        data.developmentNoteAllocation, data.developmentLength, 
                        data.developmentRepetition, data.developmentHarmony]
    elif section == "Section C":
        parameters = [data.key, data.timeSignature, 
                        data.sectionCChordProgression, 
                        data.sectionCNoteAllocation, data.sectionCLength, 
                        data.sectionCRepetition, data.sectionCHarmony]
    makeChoiceList(data, parameters[3], parameters[4])
    melody = []
    chordProgressionCounter = -1
    while len(melody) < parameters[4]:  #stays in loop until melody is complete
        measure = Measure([])
        chordProgressionCounter += 1
        #stays in loop until measure is full
        while isMeasureFull(measure.notes, parameters[1]) == False: 
            chordProgressionLength = len(parameters[2])
            chordProgressionNumeral = parameters[2][chordProgressionCounter % \
                                                        chordProgressionLength]
            if len(measure.notes) == 0: #checks if first note hasn't been placed
                randomNote = generateRandomNote(data, parameters[0], 
                                chordProgressionNumeral, parameters[3], 
                                parameters[1], parameters[6], True)
                notePitch = randomNote[0]
                noteOctave = randomNote[1]
                noteLength = randomNote[2]
                #creates note object
                newNote = Note(notePitch, noteOctave, noteLength)   
                measure.notes.append(newNote)         #adds note to measure
                if noteLength == 1/8:   #creates two eighth notes at once
                    nextNotePitch = choosePitch(data, parameters[0], 
                                    chordProgressionNumeral, parameters[6])
                    nextNote = Note(nextNotePitch, 5, 1/8)
                    measure.notes.append(nextNote)
                elif noteLength == 1/16:  #creates four sixteenth notes at once
                    for i in range(3):      #creates three more
                        nextNotePitch = choosePitch(data, parameters[0], 
                                        chordProgressionNumeral, parameters[6])
                        nextNote = Note(nextNotePitch, 5, 1/16)
                        measure.notes.append(nextNote)
            else:
                randomNote = generateRandomNote(data, parameters[0], 
                                chordProgressionNumeral, parameters[3], 
                                parameters[1], parameters[6], False, measure)
                notePitch = randomNote[0]
                noteOctave = randomNote[1]
                noteLength = randomNote[2]
                #creates note object
                newNote = Note(notePitch, noteOctave, noteLength)
                measure.notes.append(newNote)             #adds note to measure
                if noteLength == 1/8:
                    nextNotePitch = choosePitch(data, parameters[0], 
                                    chordProgressionNumeral, parameters[6])
                    nextNote = Note(nextNotePitch, 5, 1/8)
                    measure.notes.append(nextNote)
                elif noteLength == 1/16:  #creates four sixteenth notes at once
                    for i in range(3):      #creates three more
                        nextNotePitch = choosePitch(data, parameters[0], 
                                        chordProgressionNumeral, parameters[6])
                        nextNote = Note(nextNotePitch, 5, 1/16)
                        measure.notes.append(nextNote)
        melody.append(measure)          #adds completed measure to data.melody
    repeatedMelody = []
    counter = 0
    while counter < parameters[5]:
        melodyCopy = copy.deepcopy(melody)  #prevents aliasing
        repeatedMelody.extend(melodyCopy)
        counter += 1
    return repeatedMelody
    
#calculates the octave of a note in a left hand pattern
def calculateLeftOctave(data, keySignature, number, position):
    baseNote = keySignature[number]
    baseOctave = data.leftHandBaseOctaves[baseNote[0]]
    baseNoteLocation = getElementLocation(data.leftHandOctaveReference, 
                                                            baseNote[0])
    nextOctave = nthElementDict(data.leftHandOctaveReference, 
                                                    baseNoteLocation + position)
    octave = baseOctave + nextOctave
    return octave
    
    
#generates the left hand based on key, chord progression, melody length, and 
#the pattern selected and directly stores it
def generateLeftHand(data, key, chordProgression, melodyLength, timeSignature, 
                                            leftHandPattern, repetition):
    completed = []
    measures = []
    notes = []
    chordProgressionCounter = -1
    keySignature = data.keySignatures[key]
    while len(completed) < melodyLength: #stays in loop until melody is complete
        measure = Measure([])
        noteNumber = -1         #keeps track of which note in pattern to place
        chordProgressionCounter += 1
        chordProgressionLength = len(chordProgression)
        chordProgressionNumeral = chordProgression[chordProgressionCounter % \
                                                        chordProgressionLength]
        number = data.romanNumeralTranslation[chordProgressionNumeral]
        #stays in loop until measure is full
        while isMeasureFull(measure.notes, timeSignature) == False:
            noteNumber += 1
            position = data.leftHandPatternTranslation[leftHandPattern][0]\
                                                                [noteNumber]
            #pitch
            pitch = keySignature[(position + number) % 7]
            #octave calculation
            octave = calculateLeftOctave(data, keySignature, number, position)
            #length
            length = data.leftHandPatternTranslation[leftHandPattern][1]
            newNote = Note(pitch, octave, length)
            notes.append(newNote)
            measure.notes.append(newNote)
        measures.append(measure)
        completed.append(measure)
    repeatedCompleted = []
    counter = 0
    while counter < repetition:
        leftHandCopy = copy.deepcopy(completed)
        repeatedCompleted.extend(leftHandCopy)
        counter += 1
    return repeatedCompleted

def makeMelody(data):
    #right hand
    melodyInfo = generateMelody(data, "Melody")
    data.melody = melodyInfo
    #left hand
    leftHandInfo = generateLeftHand(data, data.key,
                                data.chordProgression, data.melodyLength, 
                                data.timeSignature, data.leftHandPattern,
                                data.melodyRepetition)
    data.melodyLeftHand = leftHandInfo
    #creates new page
    data.melodyPages = createPages(data, data.melody, data.melodyLeftHand)
                                                            
def makeDevelopment(data):
    #right hand
    developmentInfo = generateMelody(data, "Development")
    data.development = developmentInfo
    #left hand
    leftHandInfo = generateLeftHand(data, data.key,
                            data.developmentChordProgression, 
                            data.developmentLength, 
                            data.timeSignature, 
                            data.developmentLeftHandPattern,
                            data.developmentRepetition)
    data.developmentLeftHand = leftHandInfo
    #creates new pages
    data.developmentPages = createPages(data, data.development,
                                                data.developmentLeftHand)
    
def makeSectionC(data):
    #right hand
    sectionCInfo = generateMelody(data, "Section C")
    data.sectionC = sectionCInfo
    #left hand
    leftHandInfo = generateLeftHand(data, data.key,
                            data.sectionCChordProgression, 
                            data.sectionCLength, 
                            data.timeSignature, 
                            data.sectionCLeftHandPattern,
                            data.sectionCRepetition)
    data.sectionCLeftHand = leftHandInfo
    #creates new pages
    data.sectionCPages = createPages(data, data.sectionC, data.sectionCLeftHand)

def makeFullSong(data ,complete=False):
    order = list(data.structure)
    rightHand = []
    leftHand = []
    for section in order:
        if section == "A":
            rightHand.extend(data.melody)
            leftHand.extend(data.melodyLeftHand)
        elif section == "B":
            rightHand.extend(data.development)
            leftHand.extend(data.developmentLeftHand)
        else:
            rightHand.extend(data.sectionC)
            leftHand.extend(data.sectionCLeftHand)
    #adds an ending whole note
    endingRightNote = Note(data.key, 5, data.timeSignature)
    endingLeftNote = Note(data.key, 3, data.timeSignature)
    endingRightHandMeasure = Measure([])
    endingLeftHandMeasure = Measure([])
    endingRightHandMeasure.notes.append(endingRightNote)
    endingLeftHandMeasure.notes.append(endingLeftNote)
    rightHand.append(endingRightHandMeasure)
    leftHand.append(endingLeftHandMeasure)
    if complete == False:
        data.fullSong = rightHand
        data.fullSongLeftHand = leftHand
        data.fullSongPages = createPages(data, rightHand, leftHand)
    else:
        data.completedSongPages = createCompletedPages(data, rightHand, 
                                                                    leftHand)

        
    
    
    
##Data:
#Code from  https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
def init(data):
    data.keyList = [
        ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#'], 
        ['F', 'Bb', 'Eb', 'Ab', 'Db', 'Gb', 'Cb'], 
        ['a', 'e', 'b', 'f#', 'c#', 'g#', 'd#', 'a#'], 
        ['d', 'g', 'c', 'f', 'bb', 'eb', 'ab']
    ]
    data.majorChordProgressions = [
        ['I', 'IV', 'V'],
        ['I', 'IV', 'vi', 'V'],
        ['I', 'IV', 'I', 'V'],
        ['I', 'vi', 'IV', 'V'],
        ['I', 'V', 'vi', 'IV'], 
        ['vi', 'IV', 'I', 'V']
    ]
    data.minorChordProgressions = [
        ['i', 'VII', 'VI', 'VII'],
        ['VI', 'i', 'VII', 'iv'],
        ['i', 'VII', 'V', 'VI'],
        ['i', 'VI', 'VII', 'III'],
        ['i', 'iv', 'VII', 'III'],
        ['i', 'VI', 'III', 'VII']
    ]
    data.keySignatures = {
    "C": ["C", "D", "E", "F", "G", "A", "B"],
    "G": ["G", "A", "B", "C", "D", "E", "F#"], 
    "D": ["D", "E", "F#", "G", "A", "B", "C#"],
    "A": ["A", "B", "C#", "D", "E", "F#", "G#"],
    "E": ["E", "F#", "G#", "A", "B", "C#", "D#"],
    "B": ["B", "C#", "D#", "E", "F#", "G#", "A#"],
    "F#": ["F#", "G#", "A#", "B", "C#", "D#", "E#"],
    "C#": ["C#", "D#", "E#", "F#", "G#", "A#", "B#"],
    "F": ["F", "G", "A", "Bb", "C", "D", "E"],
    "Bb": ["Bb", "C", "D", "Eb", "F", "G", "A"],
    "Eb": ["Eb", "F", "G", "Ab", "Bb", "C", "D"],
    "Ab": ["Ab", "Bb", "C", "Db", "Eb", "F", "G"],
    "Db": ["Db", "Eb", "F", "Gb", "Ab", "Bb", "C"],
    "Gb": ["Gb", "Ab", "Bb", "Cb", "Db", "Eb", "F"],
    "Cb": ["Cb", "Db", "Eb", "Fb", "Gb", "Ab", "Bb"],
    "a": ["A", "B", "C", "D", "E", "F", "G"],
    "e": ["E", "F#", "G", "A", "B", "C", "D"],
    "b": ["B", "C#", "D", "E", "F#", "G", "A"],
    "f#": ["F#", "G#", "A", "B", "C#", "D", "E"],
    "c#": ["C#", "D#", "E", "F#", "G#", "A", "B"],
    "g#": ["G#", "A#", "B", "C#", "D#", "E", "F#"],
    "d#": ["D#", "E#", "F#", "G#", "A#", "B", "C#"],
    "a#": ["A#", "B#", "C#", "D#", "E#", "F#", "G#"],
    "d": ["D", "E", "F", "G", "A", "Bb", "C"],
    "g": ["G", "A", "Bb", "C", "D", "Eb", "F"],
    "c": ["C", "D", "Eb", "F", "G", "Ab", "Bb"],
    "f": ["F", "G", "Ab", "Bb", "C", "Db", "Eb"],
    "bb": ["Bb", "C", "Db", "Eb", "F", "Gb", "Ab"],
    "eb": ["Eb", "F", "Gb", "Ab", "Bb", "Cb", "Db"],
    "ab": ["Ab", "Bb", "Cb", "Db", "Eb", "Fb", "Gb"]
}
    data.romanNumeralTranslation = {
    "I": 0,
    "II": 1,
    "III": 2,
    "IV": 3,
    "V": 4,
    "VI": 5,
    "VII": 6,
    "i": 0,
    "ii": 1,
    "iii": 2,
    "iv": 3,
    "v": 4,
    "vi": 5,
    "vii": 6
}
    data.leftHandPatternTranslation = {
    "Arpeggio": [[0, 2, 4, 7, 9, 7, 4, 2], 1/8],
    "Rainbow\nArpeggio": [[0, 4, 7, 4, 9, 4, 7, 4], 1/8],
    "Sonatina-Style": [[0, 4, 2, 4, 0, 4, 2, 4], 1/8]
}
    data.leftHandPatternSelection = ['Arpeggio', 'Rainbow\nArpeggio', 
                                                        'Sonatina-Style']
                                                        
    data.leftHandBaseOctaves = {
        "E": 2,
        "F": 2,
        "G": 2,
        "A": 2,
        "B": 2,
        "C": 3,
        "D": 3
    }
    
    data.leftHandOctaveReference = {
        "C": 0,
        "D": 0,
        "E": 0,
        "F": 0,
        "G": 0,
        "A": 0,
        "B": 0,
        "C1": 1,
        "D1": 1,
        "E1": 1,
        "F1": 1,
        "G1": 1,
        "A1": 1,
        "B1": 1,
        "C2": 2,
        "D2": 2
    }
    #screens
    data.generalQuestionsScreen = True
    data.melodyScreen = False
    data.melodyPlaybackScreen = False
    data.developmentScreen = False
    data.developmentPlaybackScreen = False
    data.sectionCScreen = False
    data.sectionCPlaybackScreen = False
    data.fullSongPlaybackScreen = False
    data.infoScreen = False
    data.completedSongScreen = False
    data.help = False
    data.save = False
    data.counter = 0
    #play
    data.metronome = 0
    data.noteNum = 0
    data.melodyCombinedHands = []
    data.developmentCombinedHands = []
    data.sectionCCombinedHands = []
    data.fullSongCombinedHands = []
    data.playMelody = False
    data.playDevelopment = False
    data.playSectionC = False
    data.playFullSong = False
    #currently selected note
    data.selected = None
    #general questions data
    data.key = 'C'
    data.keySignature = data.keySignatures[data.key]
    data.major = True
    data.structure = "ABA"
    data.enterStructure = "Enter your own"
    data.enterStructureMode = False
    data.timeSignature = 4/4
    data.tempo = 90
    data.errorMessageAllocation = False
    data.errorMessageIncomplete = False
    #melody
    data.melody = []
    data.melodyLeftHand = []
    data.melodyPages = []
    data.currentMelodyPage = 0
    #melody questions data
    data.melodyLength = None
    data.melodyRepetition = 1
    data.noteAllocation = {1: 10, 1/2: 30, 1/4: 60, 1/8: 0, 1/16: 0}
    data.leftHandPattern = None
    data.chordProgression = None
    data.enterChordProgression = "Enter your own"
    data.enterChordProgressionMode = False
    data.enterLeftHandPattern = "Enter your own"
    data.enterLeftHandPatternMode = False
    data.melodyHarmony = 50
    #development
    data.development = []
    data.developmentLeftHand = []
    data.developmentPages = []
    data.currentDevelopmentPage = 0
    data.playDevelopment = False
    #development questions data
    data.developmentLength = None
    data.developmentRepetition = 1
    data.developmentNoteAllocation = {1: 10, 1/2: 30, 1/4: 60, 1/8: 0, 1/16: 0}
    data.developmentLeftHandPattern = None
    data.developmentChordProgression = None
    data.enterDevelopmentChordProgression = "Enter your own"
    data.enterDevelopmentChordProgressionMode = False
    data.enterDevelopmentLeftHandPattern = "Enter your own"
    data.enterDevelopmentLeftHandPatternMode = False
    data.developmentHarmony = 50
    #section c
    data.sectionC = []
    data.sectionCLeftHand = []
    data.sectionCPages = []
    data.currentSectionCPage = 0
    data.playSectionC = False
    #section c questions data
    data.sectionCLength = None
    data.sectionCRepetition = 1
    data.sectionCNoteAllocation = {1: 10, 1/2: 30, 1/4: 60, 1/8: 0, 1/16: 0}
    data.sectionCLeftHandPattern = None
    data.sectionCChordProgression = None
    data.enterSectionCChordProgression = "Enter your own"
    data.enterSectionCChordProgressionMode = False
    data.enterSectionCLeftHandPattern = "Enter your own"
    data.enterSectionCLeftHandPatternMode = False
    data.sectionCHarmony = 50
    #full song
    data.fullSong = []
    data.fullSongLeftHand = []
    data.fullSongPages = []
    data.currentFullSongPage = 0
    data.playFullSong = False
    #completed song
    data.title = "Enter Title"
    data.enterTitleMode = False
    data.composer = "Enter your name"
    data.enterComposerMode = False
    data.completedSongPages = []
    data.currentCompletedSongPage = 0


##Controller:
##Mouse Pressed Helper Functions


def mousePressedChordProgression(event, data, section):
    x = event.x
    y = event.y
    spacing = (data.width - (6 * 90)) / 7
    distance = 90 + spacing
    if 150 <= y <= 190:
        for i in range(6):
            if spacing + i * distance <= x <= spacing + 90 + i * distance:
                if data.major == True:
                    if section == "Melody":
                        data.chordProgression = \
                                                data.majorChordProgressions[i]
                    elif section == "Development":
                        data.developmentChordProgression = \
                                                data.majorChordProgressions[i]
                    elif section == "Section C":
                        data.sectionCChordProgression = \
                                                data.majorChordProgressions[i]
                else:
                    if section == "Melody":
                        data.chordProgression = data.minorChordProgressions[i]
                    elif section == "Development":
                        data.developmentChordProgression = \
                                                data.minorChordProgressions[i]
                    elif section == "Section C":
                        data.sectionCChordProgression = \
                                                data.minorChordProgressions[i]

def mousePressedLength(event, data, section):
    x = event.x
    y = event.y
    if 50 <= y <= 90:
        spacing = (data.width - 8 * 40) / 9
        distance = 40 + spacing
        for i in range(8):
            if spacing + (distance * i) <= x <= distance * (i + 1):
                length = i + 1
                if section == "Melody":
                    data.melodyLength = length
                elif section == "Development":
                    data.developmentLength = 4 * length
                elif section == "Section C":
                    data.sectionCLength =  4 * length
                    
def mousePressedLeftHandPattern(event, data, section):
    x = event.x
    y = event.y
    spacing = (data.width - (3 * 110)) / 4
    distance = 110 + spacing
    if 315 <= y <= 355:
        for i in range(3):
            if spacing + i * distance <= x <= spacing + 110 + i * distance:
                pattern = data.leftHandPatternSelection[i]
                if section == "Melody":
                    data.leftHandPattern = pattern
                elif section == "Development":
                    data.developmentLeftHandPattern = pattern
                elif section == "Section C":
                    data.sectionCLeftHandPattern = pattern
            
def mousePressedNoteAllocation(event, data, section):
    x = event.x
    y = event.y
    center = data.width / 2
    if center - 60 <= x <= center + 60 and 480 <= y <= 710:
        #decrease button
        if center - 60 <= x <= center - 40:
            for i in range(5):
                if 490 + i * 50 <= y <= 510 + i * 50:
                    key = 1 / (2 ** i)
                    if section == "Melody":
                        if data.noteAllocation[key] != 0:
                            data.noteAllocation[key] -= 5
                    elif section == "Development":
                        if data.developmentNoteAllocation[key] != 0:
                            data.developmentNoteAllocation[key] -= 5
                    elif section == "Section C":
                        if data.sectionCNoteAllocation[key] != 0:
                            data.sectionCNoteAllocation[key] -= 5
        #increase button
        elif center + 40 <= x <= center + 60:
            for i in range(5):
                if 490 + i * 50 <= y <= 510 + i * 50:
                    key = 1 / (2 ** i)
                    if section == "Melody":
                        if data.noteAllocation[key] != 100:
                            data.noteAllocation[key] += 5
                    elif section == "Development":
                        if data.developmentNoteAllocation[key] != 100:
                            data.developmentNoteAllocation[key] += 5
                    elif section == "Section C":
                        if data.sectionCNoteAllocation[key] != 100:
                            data.sectionCNoteAllocation[key] += 5

def mousePressedHarmony(event, data, section):
    x = event.x
    y = event.y
    if 485 <= y <= 505:
        if data.width - 85 <= x <= data.width - 65:
            if section == "Melody":
                if data.melodyHarmony != 100:
                    data.melodyHarmony += 5
            elif section == "Development":
                if data.developmentHarmony != 100:
                    data.developmentHarmony += 5
            elif section == "Section C":
                if data.sectionCHarmony != 100:
                    data.sectionCHarmony += 5
        elif data.width - 185 <= x <= data.width - 165:
            if section == "Melody":
                if data.melodyHarmony != 0:
                    data.melodyHarmony -= 5
            elif section == "Development":
                if data.developmentHarmony != 0:
                    data.developmentHarmony -= 5
            elif section == "Section C":
                if data.sectionCHarmony != 0:
                    data.sectionCHarmony -= 5
    
def mousePressedRepetition(event, data, section):
    x = event.x
    y = event.y
    if 635 <= y <= 655:
        if data.width - 85 <= x <= data.width - 65:
            if section == "Melody":
                if data.melodyRepetition != 4:
                    data.melodyRepetition += 1
            elif section == "Development":
                if data.developmentRepetition != 4:
                    data.developmentRepetition += 1
            elif section == "Section C":
                if data.sectionCRepetition != 4:
                    data.sectionCRepetition += 1
        elif data.width - 185 <= x <= data.width - 165:
            if section == "Melody":
                if data.melodyRepetition != 1:
                    data.melodyRepetition -= 1
            elif section == "Development":
                if data.developmentRepetition != 1:
                    data.developmentRepetition -= 1
            elif section == "Section C":
                if data.sectionCRepetition != 1:
                    data.sectionCRepetition -= 1
                
##Mouse Pressed:
#all mouse pressed events on general screen    
def mousePressedGeneralScreen(event, data):
    x = event.x
    y = event.y
    #keys
    rowNum = 0
    columnNum = 0
    spacing = (data.width - 8 * 40) / 9
    distance = spacing + 40
    for col in range(8):
        if spacing + (distance * col) <= x <= distance * (col + 1):
            for row in range(4):
                if 50 + (64 * row) <= y <= 90 + (64 * row):
                    rowNum = row
                    columnNum = col
                    if columnNum < len(data.keyList[rowNum]):
                        data.key = data.keyList[rowNum][columnNum]
                        data.chordProgression = None
                        if rowNum == 0 or rowNum == 1:
                            data.major = True
                        else:
                            data.major = False
    #structure
    if 355 <= y <= 395:
        spacing = (data.width - 80 * 4) / 5
        distance = 80 + spacing
        if spacing <= x <= spacing + 80:
            data.structure = "ABA"
        elif spacing + distance <= x <= spacing + distance + 80:
            data.structure = "ABAB"
        elif spacing + distance * 2 <= x <= spacing + distance * 2 + 80:
            data.structure = "ABACABA"
        elif spacing + distance * 3 <= x <= spacing + distance * 3 + 80:
            data.structure = "ABCBA"
    elif 430 <= y <= 470:
        if data.width / 2 - 60 <= x <= data.width / 2 + 60:
            data.enterStructureMode = True
    #time signature
    elif 545 <= y <= 625:
        spacing = 60
        distance = spacing + 40
        start = data.width / 2 - 20 - distance
        if start <= x <= start + 40:
            data.timeSignature = 4/4
        elif start + distance <= x <= start + distance + 40:
            data.timeSignature = 3/4
        elif start + distance * 2 <= x <= start + distance * 2 + 40:
            data.timeSignature = 2/4
    #tempo
    elif 700 <= y <= 720:
        if data.width / 2 - 70 <= x <= data.width / 2 - 50:
            if data.tempo != 30:
                data.tempo -= 30
        elif data.width / 2 + 50 <= x <= data.width / 2 + 70:
            if data.tempo != 180:
                data.tempo += 30
    #next button
    elif data.width / 2 - 40 <= x <= data.width / 2 + 40 and \
                    data.height - 75 <= y <= data.height - 25:
        data.generalQuestionsScreen = False
        data.enterStructureMode = False
        if "A" in data.structure:
            data.melodyScreen = True
        if "B" in data.structure:
            data.developmentScreen = True
        else:
            data.sectionCScreen = True

#all mouse pressed events on melody screen    
def mousePressedMelodyScreen(event, data):
    x = event.x
    y = event.y
    spacing = (data.width - (6 * 90)) / 7
    mousePressedChordProgression(event, data, "Melody")
    mousePressedLength(event, data, "Melody")
    mousePressedLeftHandPattern(event, data, "Melody")
    mousePressedNoteAllocation(event, data, "Melody")
    mousePressedHarmony(event, data, "Melody")
    mousePressedRepetition(event, data, "Melody")
    #next and back button
    if data.height - 75 <= y <= data.height - 25:
        #back button
        if data.width / 2 - 100 <= x <= data.width / 2 - 20:
            data.melodyScreen = False
            data.generalQuestionsScreen = True
            data.enterChordProgressionMode = False
            data.enterLeftHandPatternMode = False
        #next button
        elif data.width / 2 + 20 <= x <= data.width / 2 + 100:
            if isMelodyInputValid(data.melodyLength, data.leftHandPattern, 
                data.chordProgression) and \
                                        isDictionaryFull(data.noteAllocation):
                makeMelody(data)
                data.melodyScreen = False
                data.enterChordProgressionMode = False
                data.enterChordProgressionMode = False
                data.enterLeftHandPatternMode = False
                data.melodyPlaybackScreen = True
            else:
                if isMelodyInputValid(data.melodyLength, data.leftHandPattern, 
                data.chordProgression) == False:
                    data.errorMessageIncomplete = True
                if isDictionaryFull(data.noteAllocation) == False:
                    data.errorMessageAllocation = True
    #custom chord progression
    elif 190 + spacing <= y <= 230 + spacing:
        if data.width / 2 - 60 <= x <= data.width / 2 + 60:
            data.enterChordProgressionMode = True
            data.enterLeftHandPatternMode = False
    #custom left hand pattern
    elif 380 <= y <= 420:
        if data.width / 2 - 100 <= x <= data.width / 2 + 100:
            data.enterLeftHandPatternMode = True
            data.enterChordProgressionMode = False
    #checks if melody specifications are complete after every click
    if isMelodyInputValid(data.melodyLength, data.leftHandPattern, 
        data.chordProgression):
        data.errorMessageIncomplete = False
    #checks if note allocation adds to 100% after every click
    if isDictionaryFull(data.noteAllocation) == True:
            data.errorMessageAllocation = False

def mousePressedMelodyPlaybackScreen(event, data):
    x = event.x
    y = event.y
    data.selected = None
    center = 50 + (data.height / 4.5) * 2 - (data.height / 4.5 - 120) / 2
    if data.height - 75 <= y <= data.height - 25:
        #back button
        if data.width / 2 - 190 <= x <= data.width / 2 - 90:
            data.currentMelodyPage = 0
            data.playMelody = False
            data.melodyPlaybackScreen = False
            data.melodyScreen = True
        #play button
        elif data.width / 2 - 50 <= x <= data.width / 2 + 50:
            if data.playMelody == False:
                data.currentMelodyPage = 0
                data.noteNum = 0
                data.playMelody = True
                data.melodyCombinedHands = combineHands(data.melody, 
                                                            data.melodyLeftHand)
            else:
                data.playMelody = False
                data.noteNum = 0
        #next button
        elif data.width / 2 + 90 <= x <= data.width / 2 + 190:
            data.playMelody = False
            data.melodyPlaybackScreen = False
            if "B" in data.structure:
                data.developmentScreen = True
            elif "C" in data.structure:
                data.sectionCScreen = True
            else:
                data.developmentScreen = False
                data.sectionCScreen = False
                makeFullSong(data)
                data.fullSongPlaybackScreen = True

    #page turners
    elif center - 15 <= y <= center + 15 and data.playMelody == False:
        if 10 <= x <= 40 and data.currentMelodyPage != 0:
            data.currentMelodyPage -= 1
        elif data.width - 40 <= x <= data.width - 10 and \
                data.currentMelodyPage != len(data.melodyPages) - 1:
            data.currentMelodyPage += 1
    #checks for clicks in right hand
    for measure in data.melody:
        for note in measure.notes:
            if note.x != None and note.y != None:
                if note.x - 6 <= x <= note.x + 6 and \
                                                note.y - 4 <= y <= note.y + 4:
                    data.selected = note
    #checks for clicks in left hand
    for measure in data.melodyLeftHand:
        for note in measure.notes:
            if note.x != None and note.y != None:
                if note.x - 6 <= x <= note.x + 6 and \
                                                note.y - 4 <= y <= note.y + 4:
                    data.selected = note

def mousePressedDevelopmentScreen(event, data):
    x = event.x
    y = event.y
    spacing = (data.width - (6 * 90)) / 7
    mousePressedChordProgression(event, data, "Development")
    mousePressedLength(event, data, "Development")
    mousePressedLeftHandPattern(event, data, "Development")
    mousePressedNoteAllocation(event, data, "Development")
    mousePressedHarmony(event, data, "Development")
    mousePressedRepetition(event, data, "Development")
    #next and back button
    if data.height - 75 <= y <= data.height - 25:
        #back button
        if data.width / 2 - 100 <= x <= data.width / 2 - 20:
            data.developmentScreen = False
            data.enterDevelopmentLeftHandPatternMode = False
            data.enterDevelopmentChordProgressionMode = False
            if "A" in data.structure:
                data.melodyPlaybackScreen = True
            else:
                data.generalQuestionsScreen = True
        #next button
        elif data.width / 2 + 20 <= x <= data.width / 2 + 100:
            #checks if everything is complete before generating melody
            if isMelodyInputValid(data.developmentLength, 
                                        data.developmentLeftHandPattern, 
                                        data.developmentChordProgression) and\
                            isDictionaryFull(data.developmentNoteAllocation):
                makeDevelopment(data)
                data.developmentScreen = False
                data.developmentPlaybackScreen = True
                data.enterDevelopmentLeftHandPatternMode = False
                data.enterDevelopmentChordProgressionMode = False
            else:
                if isMelodyInputValid(data.developmentLength,
                                        data.developmentLeftHandPattern, 
                                    data.developmentChordProgression) == False:
                    data.errorMessageIncomplete = True
                if isDictionaryFull(data.developmentNoteAllocation) == False:
                    data.errorMessageAllocation = True
    #custom chord progression
    elif 190 + spacing <= y <= 230 + spacing:
        if data.width / 2 - 60 <= x <= data.width / 2 + 60:
            data.enterDevelopmentChordProgressionMode = True
            data.enterDevelopmentLeftHandPatternMode = False
    #custom left hand pattern
    elif 380 <= y <= 420:
        if data.width / 2 - 100 <= x <= data.width / 2 + 100:
            data.enterDevelopmentLeftHandPatternMode = True
            data.enterDevelopmentChordProgressionMode = False
    #checks if melody specifications are complete after every click
    if isMelodyInputValid(data.developmentLength, 
            data.developmentLeftHandPattern, data.developmentChordProgression):
        data.errorMessageIncomplete = False
    #checks if note allocation adds to 100% after every click
    if isDictionaryFull(data.developmentNoteAllocation) == True:
            data.errorMessageAllocation = False
        
def mousePressedDevelopmentPlaybackScreen(event, data):
    x = event.x
    y = event.y
    data.selected = None
    center = 50 + (data.height / 4.5) * 2 - (data.height / 4.5 - 120) / 2
    if data.height - 75 <= y <= data.height - 25:
        #back button
        if data.width / 2 - 190 <= x <= data.width / 2 - 90:
            data.playDevelopment = False
            data.developmentPlaybackScreen = False
            data.developmentScreen = True
            data.currentDevelopmentPage = 0
        #play button
        elif data.width / 2 - 50 <= x <= data.width / 2 + 50:
            if data.playDevelopment == False:
                data.currentDevelopmentPage = 0
                data.noteNum = 0
                data.playDevelopment = True
                data.developmentCombinedHands = combineHands(data.development, 
                                                    data.developmentLeftHand)
            else:
                data.playDevelopment = False
                data.noteNum = 0
        #next button
        elif data.width / 2 + 90 <= x <= data.width / 2 + 190:
            data.playDevelopment = False
            data.developmentPlaybackScreen = False
            #checks if user wants a 3rd section, if not, skips to full song
            if "C" in data.structure:
                data.sectionCScreen = True
            else:
                makeFullSong(data)
                data.fullSongPlaybackScreen = True
    #page turners
    elif center - 15 <= y <= center + 15 and data.playDevelopment == False:
        if 10 <= x <= 40 and data.currentDevelopmentPage != 0:
            data.currentDevelopmentPage -= 1
        elif data.width - 40 <= x <= data.width - 10 and \
                data.currentDevelopmentPage != len(data.developmentPages) - 1:
            data.currentDevelopmentPage += 1
    #checks for clicks in right hand
    for measure in data.developmentPages\
                                [data.currentDevelopmentPage].rightHandMeasures:
        for note in measure.notes:
            if note.x != None and note.y != None:
                if note.x - 6 <= x <= note.x + 6 and \
                                                note.y - 4 <= y <= note.y + 4:
                    data.selected = note
    #checks for clicks in left hand
    for measure in data.developmentPages\
                                [data.currentDevelopmentPage].leftHandMeasures:
        for note in measure.notes:
            if note.x != None and note.y != None:
                if note.x - 6 <= x <= note.x + 6 and \
                                                note.y - 4 <= y <= note.y + 4:
                    data.selected = note

def mousePressedSectionCScreen(event, data):
    x = event.x
    y = event.y
    spacing = (data.width - (6 * 90)) / 7
    mousePressedChordProgression(event, data, "Section C")
    mousePressedLength(event, data, "Section C")
    mousePressedLeftHandPattern(event, data, "Section C")
    mousePressedNoteAllocation(event, data, "Section C")
    mousePressedHarmony(event, data, "Section C")
    mousePressedRepetition(event, data, "Section C")
    #next and back button
    if data.height - 75 <= y <= data.height - 25:
        #back button
        if data.width / 2 - 100 <= x <= data.width / 2 - 20:
            data.sectionCScreen = False
            data.enterSectionCLeftHandPatternMode = False
            data.enterSectionCChordProgressionMode = False
            if "B" in data.structure:
                data.developmentPlaybackScreen = True
            if "A" in data.structure:
                data.melodyPlaybackScreen = True
            else:
                data.generalQuestionsScreen = True
        #next button
        elif data.width / 2 + 20 <= x <= data.width / 2 + 100:
            #checks if everything is complete before generating melody
            if isMelodyInputValid(data.sectionCLength, 
                data.sectionCLeftHandPattern, data.sectionCChordProgression) \
                            and isDictionaryFull(data.sectionCNoteAllocation):
                makeSectionC(data)
                data.sectionCScreen = False
                data.sectionCPlaybackScreen = True
                data.enterSectionCLeftHandPatternMode = False
                data.enterSectionCChordProgressionMode = False
            else:
                if isMelodyInputValid(data.sectionCLength, 
                                    data.sectionCLeftHandPattern, 
                                    data.sectionCChordProgression) == False:
                    data.errorMessageIncomplete = True
                if isDictionaryFull(data.sectionCNoteAllocation) == False:
                    data.errorMessageAllocation = True
    #custom chord progression
    elif 190 + spacing <= y <= 230 + spacing:
        if data.width / 2 - 60 <= x <= data.width / 2 + 60:
            data.enterSectionCChordProgressionMode = True
            data.enterSectionCLeftHandPatternMode = False
    #custom left hand pattern
    elif 380 <= y <= 420:
        if data.width / 2 - 100 <= x <= data.width / 2 + 100:
            data.enterSectionCLeftHandPatternMode = True
            data.enterSectionCChordProgressionMode = False
    #checks if melody specifications are complete after every click
    if isMelodyInputValid(data.sectionCLength, data.sectionCLeftHandPattern, 
        data.sectionCChordProgression):
        data.errorMessageIncomplete = False
    #checks if note allocation adds to 100% after every click
    if isDictionaryFull(data.sectionCNoteAllocation) == True:
            data.errorMessageAllocation = False

def mousePressedSectionCPlaybackScreen(event, data):
    x = event.x
    y = event.y
    center = 50 + (data.height / 4.5) * 2 - (data.height / 4.5 - 120) / 2
    data.selected = None
    if data.height - 75 <= y <= data.height - 25:
        #back button
        if data.width / 2 - 190 <= x <= data.width / 2 - 90:
            data.playSectionC = False
            data.sectionCPlaybackScreen = False
            data.sectionCScreen = True
            data.currentSectionCPage = 0
        #play button
        elif data.width / 2 - 50 <= x <= data.width / 2 + 50:
            if data.playSectionC == False:
                data.currentSectionCPage = 0
                data.noteNum = 0
                data.playSectionC = True
                data.sectionCCombinedHands = combineHands(data.sectionC, 
                                                        data.sectionCLeftHand)
            else:
                data.playSectionC = False
                data.noteNum = 0
        #next button
        elif data.width / 2 + 90 <= x <= data.width / 2 + 190:
            data.playSectionC = False
            makeFullSong(data)
            data.sectionCPlaybackScreen = False
            data.fullSongPlaybackScreen = True
    #page turners
    elif center - 15 <= y <= center + 15 and data.playSectionC == False:
        if 10 <= x <= 40 and data.currentSectionCPage != 0:
            data.currentSectionCPage -= 1
        elif data.width - 40 <= x <= data.width - 10 and \
                data.currentSectionCPage != len(data.sectionCPages) - 1:
            data.currentSectionCPage += 1
    #checks for clicks in right hand
    for measure in data.sectionCPages\
                                [data.currentSectionCPage].rightHandMeasures:
        for note in measure.notes:
            if note.x != None and note.y != None:
                if note.x - 6 <= x <= note.x + 6 and \
                                                note.y - 4 <= y <= note.y + 4:
                    data.selected = note
    #checks for clicks in left hand
    for measure in data.sectionCPages\
                                [data.currentSectionCPage].leftHandMeasures:
        for note in measure.notes:
            if note.x != None and note.y != None:
                if note.x - 6 <= x <= note.x + 6 and \
                                            note.y - 4 <= y <= note.y + 4:
                    data.selected = note

def mousePressedFullSongPlaybackScreen(event, data):
    x = event.x
    y = event.y
    center = 50 + (data.height / 4.5) * 2 - (data.height / 4.5 - 120) / 2
    data.selected = None
    if data.height - 75 <= y <= data.height - 25:
        #back button
        if data.width / 2 - 190 <= x <= data.width / 2 - 90:
            data.playFullSong = False
            data.fullSongPlaybackScreen = False
            data.currentFullSongPage = 0
            #checks if a 2nd or 3rd section exists
            if "C" in data.structure:
                data.sectionCPlaybackScreen = True
            elif "B" in data.structure:
                data.developmentPlaybackScreen = True
            else:
                data.melodyPlaybackScreen = True
        #play button
        elif data.width / 2 - 50 <= x <= data.width / 2 + 50:
            if data.playFullSong == False:
                data.currentFullSongPage = 0
                data.noteNum = 0
                data.playFullSong = True
                data.fullSongCombinedHands = combineHands(data.fullSong, 
                                                        data.fullSongLeftHand)
            else:
                data.playFullSong = False
                data.noteNum = 0
        #next button
        elif data.width / 2 + 90 <= x <= data.width / 2 + 190:
            data.playFullSong = False
            data.fullSongPlaybackScreen = False
            data.infoScreen = True
    #pages
    elif center - 15 <= y <= center + 15 and data.playFullSong == False:
        #previous page
        if 10 <= x <= 40 and data.currentFullSongPage != 0:
            data.currentFullSongPage -= 1
        #next page
        elif data.width - 40 <= x <= data.width - 10 and \
                data.currentFullSongPage != len(data.fullSongPages) - 1:
            data.currentFullSongPage += 1
    #checks for clicks in right hand
    for measure in data.fullSongPages\
                                [data.currentFullSongPage].rightHandMeasures:
        for note in measure.notes:
            if note.x != None and note.y != None:
                if note.x - 6 <= x <= note.x + 6 and \
                                                note.y - 4 <= y <= note.y + 4:
                    data.selected = note
    #checks for clicks in left hand
    for measure in data.fullSongPages\
                                [data.currentFullSongPage].leftHandMeasures:
        for note in measure.notes:
            if note.x != None and note.y != None:
                if note.x - 6 <= x <= note.x + 6 and \
                                                note.y - 4 <= y <= note.y + 4:
                    data.selected = note

def mousePressedInfoScreen(event, data):
    x = event.x
    y = event.y
    data.enterTitleMode = False
    data.enterComposerMode = False
    #title
    if data.height / 2 - 120 <= y <= data.height / 2 - 70:
        if data.width / 2 - 200 <= x <= data.width / 2 + 200:
            data.enterTitleMode = True
    elif data.height / 2 + 70 <= y <= data.height / 2 + 120:
        if data.width / 2 - 200 <= x <= data.width / 2 + 200:
            data.enterComposerMode = True
    elif data.height - 75 <= y <= data.height - 25:
        #back button
        if data.width / 2 - 100 <= x <= data.width / 2 - 20:
            data.fullSongPlaybackScreen = True
            data.infoScreen = False
        #next button
        elif data.width / 2 + 20 <= x <= data.width / 2 + 100:
            makeFullSong(data, True)
            data.completedSongScreen = True
            data.infoScreen = False
            
def mousePressedCompletedSongScreen(event, data):
    x = event.x
    y = event.y
    center = 50 + (data.height / 4.5) * 2 - (data.height / 4.5 - 120) / 2
    if data.height - 75 <= y <= data.height - 25:
        #back button
        if data.width / 2 - 260 <= x <= data.width / 2 - 160:
            data.playFullSong = False
            data.completedSongPlaybackScreen = False
            data.currentCompletedSongPage = 0
            data.infoScreen = True
        #play button
        if data.width / 2 - 120 <= x <= data.width / 2 - 20:
            if data.playFullSong == False:
                data.currentCompletedSongPage = 0
                data.fullSongCombinedHands = combineHands(data.fullSong, 
                                                        data.fullSongLeftHand)
                data.playFullSong = True
                data.noteNum = 0
            else:
                data.playFullSong = False
                data.noteNum = 0
        #save button
        elif data.width / 2 + 20 <= x <= data.width / 2 + 120:
            data.playFullSong = False
            data.save = True
            data.currentCompletedSongPage = 0
            data.completedSongScreen = False
        #restart
        elif data.width / 2 + 160 <= x <= data.width / 2 + 260:
            init(data)
    #pages
    elif center - 15 <= y <= center + 15:
        #previous page
        if 10 <= x <= 40 and data.currentCompletedSongPage != 0:
            data.currentCompletedSongPage -= 1
        #next page
        elif data.width - 40 <= x <= data.width - 10 and \
                data.currentCompletedSongPage != \
                                            len(data.completedSongPages) - 1:
            data.currentCompletedSongPage += 1
            
def mousePressed(event, data):
    if data.generalQuestionsScreen == True:
        mousePressedGeneralScreen(event, data)
    elif data.melodyScreen == True:
        mousePressedMelodyScreen(event, data)
    elif data.melodyPlaybackScreen == True:
        mousePressedMelodyPlaybackScreen(event, data)
    elif data.developmentScreen == True:
        mousePressedDevelopmentScreen(event, data)
    elif data.developmentPlaybackScreen == True:
        mousePressedDevelopmentPlaybackScreen(event, data)
    elif data.sectionCScreen == True:
        mousePressedSectionCScreen(event, data)
    elif data.sectionCPlaybackScreen == True:
        mousePressedSectionCPlaybackScreen(event, data)
    elif data.fullSongPlaybackScreen == True:
        mousePressedFullSongPlaybackScreen(event, data)
    elif data.infoScreen == True:
        mousePressedInfoScreen(event, data)
    elif data.completedSongScreen == True:
        mousePressedCompletedSongScreen(event, data)

##Key Pressed:
def keyPressedCustomStructure(event, data):
    #enters keyboard input
    if event.char != chr(127) and event.char != chr(8) and \
                                                    event.keysym != "Return":
        #allows only A, B, C to be entered
        if event.char == "A" or event.char == "B" or event.char == "C":
            if data.enterStructure == "Enter your own": #allows quick editing
                data.enterStructure = ""
            data.enterStructure += event.char
    #backspaces
    elif (event.char == chr(127) or event.char == chr(8)) and \
                                                    data.enterStructure != "":
        if data.enterStructure == "Enter your own":     #allows quick editing
            data.enterStructure = ""
        data.enterStructure = data.enterStructure[:-1]
    #enters input if valid
    elif event.keysym == "Return":
        if isValidStructure(data.enterStructure):
            data.structure = data.enterStructure
            data.enterStructureMode = False

def keyPressedCustomChordProgression(event, data, section):
    if section == "Melody":
        #enters keyboard input
        if event.char != chr(127) and event.char != chr(8) and \
                                                    event.keysym != "Return":
            if event.char in ['I', 'V', 'i', 'v', ','] or \
                                                        event.keysym == "space":
                if data.enterChordProgression == "Enter your own":
                    data.enterChordProgression = ""
                data.enterChordProgression += event.char
        #backspaces
        elif (event.char == chr(127) or event.char == chr(8)) and \
                                            data.enterChordProgression != "":
            if data.enterChordProgression == "Enter your own":
                data.enterChordProgression = ""
            data.enterChordProgression = data.enterChordProgression[:-1]
        #enters input if valid
        elif event.keysym == "Return":
            if isValidChordProgression(data.enterChordProgression):
                data.chordProgression = convertChordProgression\
                                                    (data.enterChordProgression)
                data.enterChordProgressionMode = False
    elif section == "Development":
        #enters keyboard input
        if event.char != chr(127) and event.char != chr(8) and \
                                                    event.keysym != "Return":
            if event.char in ['I', 'V', 'i', 'v', ','] or \
                                                    event.keysym == "space":
                if data.enterDevelopmentChordProgression == "Enter your own":
                    data.enterDevelopmentChordProgression = ""
                data.enterDevelopmentChordProgression += event.char
        #backspaces
        elif (event.char == chr(127) or event.char == chr(8)) and \
                                    data.enterDevelopmentChordProgression != "":
            if data.enterDevelopmentChordProgression == "Enter your own":
                data.enterDevelopmentChordProgression = ""
            data.enterDevelopmentChordProgression = \
                                    data.enterDevelopmentChordProgression[:-1]
        #enters input if valid
        elif event.keysym == "Return":
            if isValidChordProgression(data.enterDevelopmentChordProgression):
                data.developmentChordProgression = convertChordProgression\
                                        (data.enterDevelopmentChordProgression)
                data.enterDevelopmentChordProgressionMode = False
    elif section == "Section C":
        #enters keyboard input
        if event.char != chr(127) and event.char != chr(8) and \
                                                    event.keysym != "Return":
            if event.char in ['I', 'V', 'i', 'v', ','] or \
                                                    event.keysym == "space":
                if data.enterSectionCChordProgression == "Enter your own":
                    data.enterSectionCChordProgression = ""
                data.enterSectionCChordProgression += event.char
        #backspaces
        elif (event.char == chr(127) or event.char == chr(8)) and \
                                    data.enterSectionCChordProgression != "":
            if data.enterSectionCChordProgression == "Enter your own":
                data.enterSectionCChordProgression = ""
            data.enterSectionCChordProgression = \
                                        data.enterSectionCChordProgression[:-1]
        #enters input if valid
        elif event.keysym == "Return":
            if isValidChordProgression(data.enterSectionCChordProgression):
                data.sectionCChordProgression = convertChordProgression\
                                        (data.enterSectionCChordProgression)
                data.enterSectionCChordProgressionMode = False
                
def keyPressedCustomLeftHandPattern(event, data, section):
    if section == "Melody":
        #enters keyboard input
        if event.char != chr(127) and event.char != chr(8) and \
                                                    event.keysym != "Return":
            if event.char.isdigit() or event.char in ('/', ',', '[', ']') or \
                                                    event.keysym == "space":
                if data.enterLeftHandPattern == "Enter your own":
                    data.enterLeftHandPattern = ""
                data.enterLeftHandPattern += event.char
        #backspaces
        elif (event.char == chr(127) or event.char == chr(8)) and \
                                            data.enterLeftHandPattern != "":
            if data.enterLeftHandPattern == "Enter your own":
                data.enterLeftHandPattern = ""
            data.enterLeftHandPattern = data.enterLeftHandPattern[:-1]
        #enters input if valid
        elif event.keysym == "Return":
            if isValidLeftHandPattern(data, data.enterLeftHandPattern):
                data.leftHandPattern = data.enterLeftHandPattern
                data.enterLeftHandPatternMode = False
    elif section == "Development":
        #enters keyboard input
        if event.char != chr(127) and event.char != chr(8) and \
                                                    event.keysym != "Return":
            if event.char.isdigit() or event.char in ('/', ',', '[', ']') or \
                                                    event.keysym == "space":
                if data.enterDevelopmentLeftHandPattern == "Enter your own":
                    data.enterDevelopmentLeftHandPattern = ""
                data.enterDevelopmentLeftHandPattern += event.char
        #backspaces
        elif (event.char == chr(127) or event.char == chr(8)) and \
                                    data.enterDevelopmentLeftHandPattern != "":
            if data.enterDevelopmentLeftHandPattern == "Enter your own":
                data.enterDevelopmentLeftHandPattern = ""
            data.enterDevelopmentLeftHandPattern = \
                                    data.enterDevelopmentLeftHandPattern[:-1]
        #enters input if valid
        elif event.keysym == "Return":
            if isValidLeftHandPattern(data, 
                                        data.enterDevelopmentLeftHandPattern):
                data.developmentLeftHandPattern = \
                                        data.enterDevelopmentLeftHandPattern
                data.enterDevelopmentLeftHandPatternMode = False
    elif section == "Section C":
        #enters keyboard input
        if event.char != chr(127) and event.char != chr(8) and \
                                                    event.keysym != "Return":
            if event.char.isdigit() or event.char in ('/', ',', '[', ']') or \
                                                        event.keysym == "space":
                if data.enterSectionCLeftHandPattern == "Enter your own":
                    data.enterSectionCLeftHandPattern = ""
                data.enterSectionCLeftHandPattern += event.char
        #backspaces
        elif (event.char == chr(127) or event.char == chr(8)) and \
                                        data.enterSectionCLeftHandPattern != "":
            if data.enterSectionCLeftHandPattern == "Enter your own":
                data.enterSectionCLeftHandPattern = ""
            data.enterSectionCLeftHandPattern = \
                                        data.enterSectionCLeftHandPattern[:-1]
        #enters input if valid
        elif event.keysym == "Return":
            if isValidLeftHandPattern(data, data.enterSectionCLeftHandPattern):
                data.sectionCLeftHandPattern = data.enterSectionCLeftHandPattern
                data.enterSectionCLeftHandPatternMode = False
                
def keyPressedCustomTitle(event, data):
    #enters keyboard input
    if event.char != chr(127) and event.char != chr(8) and \
                                                    event.keysym != "Return":
        if data.title == "Enter Title":
            data.title = ""
        data.title += event.char
    #backspaces
    elif (event.char == chr(127) or event.char == chr(8)) and data.title != "":
        if data.title == "Enter Title":
            data.title = ""
        data.title = data.title[:-1]
    #enters input if valid
    elif event.keysym == "Return":
        data.enterTitleMode = False
        
def keyPressedCustomComposer(event, data):
    #enters keyboard input
    if event.char != chr(127) and event.char != chr(8) and \
                                                    event.keysym != "Return":
        if data.composer == "Enter your name":
            data.composer = ""
        data.composer += event.char
    #backspaces
    elif (event.char == chr(127) or event.char == chr(8)) and \
                                                        data.composer != "":
        if data.composer == "Enter your name":
            data.composer = ""
        data.composer = data.composer[:-1]
    #enters input if valid
    elif event.keysym == "Return":
        data.enterComposerMode = False

def keyPressedGeneralQuestionsScreen(event, data):
    if data.enterStructureMode == True:
        keyPressedCustomStructure(event, data)
    
def keyPressedMelodyQuestionsScreen(event, data):
    if data.enterChordProgressionMode == True:
        keyPressedCustomChordProgression(event, data, "Melody")
    elif data.enterLeftHandPatternMode == True:
        keyPressedCustomLeftHandPattern(event, data, "Melody")

def keyPressedMelodyPlaybackScreen(event, data):
    if event.char == "r":
        makeMelody(data)
        data.selected = None
    elif event.keysym == "Up" and data.selected != None:
        if isNoteInRightHand(data.selected, 
                data.melodyPages[data.currentMelodyPage].rightHandMeasures):
            data.selected.moveNoteUpTreble(data.keySignatures[data.key])
        else:
            data.selected.moveNoteUpBass(data.keySignatures[data.key])
    elif event.keysym == "Down" and data.selected != None:
        if isNoteInRightHand(data.selected, 
                    data.melodyPages[data.currentMelodyPage].rightHandMeasures):
            data.selected.moveNoteDownTreble(data.keySignatures[data.key])
        else:
            data.selected.moveNoteDownBass(data.keySignatures[data.key])
    elif event.keysym == "Left" and data.selected != None:
        newIndices = previousSelect(data.melodyPages[data.currentMelodyPage], 
                                                                data.selected)
        newMeasureIndex = newIndices[0]
        newNoteIndex = newIndices[1]
        if isNoteInRightHand(data.selected, data.melodyPages\
                                    [data.currentMelodyPage].rightHandMeasures):
            data.selected = data.melodyPages[data.currentMelodyPage].\
                        rightHandMeasures[newMeasureIndex].notes[newNoteIndex]
        else:
            data.selected = data.melodyPages[data.currentMelodyPage].\
                        leftHandMeasures[newMeasureIndex].notes[newNoteIndex]
    elif event.keysym == "Right" and data.selected != None:
        newIndices = nextSelect(data.melodyPages[data.currentMelodyPage], 
                                                            data.selected)
        newMeasureIndex = newIndices[0]
        newNoteIndex = newIndices[1]
        if isNoteInRightHand(data.selected, data.melodyPages\
                                    [data.currentMelodyPage].rightHandMeasures):
            data.selected = data.melodyPages[data.currentMelodyPage].\
                        rightHandMeasures[newMeasureIndex].notes[newNoteIndex]
        else:
            data.selected = data.melodyPages[data.currentMelodyPage].\
                        leftHandMeasures[newMeasureIndex].notes[newNoteIndex]
    #deleting notes
    elif data.selected != None and (event.char == chr(127) or \
                                                        event.char == chr(8)):
        data.selected.pitch = "0"
        data.selected.octave = 0
        data.selected = None
    elif event.keysym == "space":
        if data.playMelody == False:
            data.currentMelodyPage = 0
            data.noteNum = 0
            data.playMelody = True
            data.melodyCombinedHands = combineHands(data.melody, 
                                                        data.melodyLeftHand)
        else:
            data.playMelody = False
            data.noteNum = 0

def keyPressedDevelopmentScreen(event, data):
    if data.enterDevelopmentChordProgressionMode == True:
        keyPressedCustomChordProgression(event, data, "Development")
    elif data.enterDevelopmentLeftHandPatternMode == True:
        keyPressedCustomLeftHandPattern(event, data, "Development")
    

def keyPressedDevelopmentPlaybackScreen(event, data):
    if event.char == "r":
        makeDevelopment(data)
        data.selected = None
    elif event.keysym == "Up" and data.selected != None:
        #checks if note is in treble or base cleff
        if isNoteInRightHand(data.selected, data.developmentPages\
                            [data.currentDevelopmentPage].rightHandMeasures):
            data.selected.moveNoteUpTreble(data.keySignatures[data.key])
        else:
            data.selected.moveNoteUpBass(data.keySignatures[data.key])
    elif event.keysym == "Down" and data.selected != None:
        #checks if note is in treble or base cleff
        if isNoteInRightHand(data.selected, data.developmentPages\
                            [data.currentDevelopmentPage].rightHandMeasures):
            data.selected.moveNoteDownTreble(data.keySignatures[data.key])
        else:
            data.selected.moveNoteDownBass(data.keySignatures[data.key])
    elif event.keysym == "Left" and data.selected != None:
        newIndices = previousSelect(data.developmentPages\
                                [data.currentDevelopmentPage], data.selected)
        newMeasureIndex = newIndices[0]
        newNoteIndex = newIndices[1]
        if isNoteInRightHand(data.selected, data.developmentPages\
                            [data.currentDevelopmentPage].rightHandMeasures):
            data.selected = data.developmentPages[data.currentDevelopmentPage].\
                        rightHandMeasures[newMeasureIndex].notes[newNoteIndex]
        else:
            data.selected = data.developmentPages[data.currentDevelopmentPage].\
                        leftHandMeasures[newMeasureIndex].notes[newNoteIndex]
    elif event.keysym == "Right" and data.selected != None:
        newIndices = nextSelect(data.developmentPages\
                                [data.currentDevelopmentPage], data.selected)
        newMeasureIndex = newIndices[0]
        newNoteIndex = newIndices[1]
        if isNoteInRightHand(data.selected, data.developmentPages\
                            [data.currentDevelopmentPage].rightHandMeasures):
            data.selected = data.developmentPages[data.currentDevelopmentPage].\
                        rightHandMeasures[newMeasureIndex].notes[newNoteIndex]
        else:
            data.selected = data.developmentPages[data.currentDevelopmentPage].\
                        leftHandMeasures[newMeasureIndex].notes[newNoteIndex]
    elif data.selected != None and (event.char == chr(127) or \
                                                        event.char == chr(8)):
        data.selected.pitch = "0"
        data.selected.octave = 0
        data.selected = None
    elif event.keysym == "space":
        if data.playDevelopment == False:
            data.currentDevelopmentPage = 0
            data.noteNum = 0
            data.playDevelopment = True
            data.developmentCombinedHands = combineHands(data.development, 
                                                data.developmentLeftHand)
        else:
            data.playDevelopment = False
            data.noteNum = 0
    
def keyPressedSectionCScreen(event, data):
    if data.enterSectionCChordProgressionMode == True:
        keyPressedCustomChordProgression(event, data, "Section C")
    elif data.enterSectionCLeftHandPatternMode == True:
        keyPressedCustomLeftHandPattern(event, data, "Section C")

def keyPressedSectionCPlaybackScreen(event, data):
    if event.char == "r":
        makeSectionC(data)
        data.selected = None
    elif event.keysym == "Up" and data.selected != None:
        if isNoteInRightHand(data.selected, data.sectionCPages\
                                [data.currentSectionCPage].rightHandMeasures):
            data.selected.moveNoteUpTreble(data.keySignatures[data.key])
        else:
            data.selected.moveNoteUpBass(data.keySignatures[data.key])
    elif event.keysym == "Down" and data.selected != None:
        if isNoteInRightHand(data.selected, data.sectionCPages\
                                [data.currentSectionCPage].rightHandMeasures):
            data.selected.moveNoteDownTreble(data.keySignatures[data.key])
        else:
            data.selected.moveNoteDownBass(data.keySignatures[data.key])
    elif event.keysym == "Left" and data.selected != None:
        newIndices = previousSelect(data.sectionCPages\
                                    [data.currentSectionCPage], data.selected)
        newMeasureIndex = newIndices[0]
        newNoteIndex = newIndices[1]
        if isNoteInRightHand(data.selected, data.sectionCPages\
                                [data.currentSectionCPage].rightHandMeasures):
            data.selected = data.sectionCPages[data.currentSectionCPage].\
                        rightHandMeasures[newMeasureIndex].notes[newNoteIndex]
        else:
            data.selected = data.sectionCPages[data.currentSectionCPage].\
                        leftHandMeasures[newMeasureIndex].notes[newNoteIndex]
    elif event.keysym == "Right" and data.selected != None:
        newIndices = nextSelect(data.sectionCPages[data.currentSectionCPage], 
                                                                data.selected)
        newMeasureIndex = newIndices[0]
        newNoteIndex = newIndices[1]
        if isNoteInRightHand(data.selected, data.sectionCPages\
                                [data.currentSectionCPage].rightHandMeasures):
            data.selected = data.sectionCPages[data.currentSectionCPage].\
                        rightHandMeasures[newMeasureIndex].notes[newNoteIndex]
        else:
            data.selected = data.sectionCPages[data.currentSectionCPage].\
                        leftHandMeasures[newMeasureIndex].notes[newNoteIndex]
    elif data.selected != None and (event.char == chr(127) or \
                                                        event.char == chr(8)):
        data.selected.pitch = "0"
        data.selected.octave = 0
        data.selected = None
    elif event.keysym == "space":
        if data.playSectionC == False:
            data.currentSectionCPage = 0
            data.noteNum = 0
            data.playSectionC = True
            data.sectionCCombinedHands = combineHands(data.sectionC, 
                                                    data.sectionCLeftHand)
        else:
            data.playSectionC = False
            data.noteNum = 0

def keyPressedFullSongPlaybackScreen(event, data):
    if event.keysym == "Up" and data.selected != None:
        if isNoteInRightHand(data.selected, data.fullSongPages\
                                [data.currentFullSongPage].rightHandMeasures):
            data.selected.moveNoteUpTreble(data.keySignatures[data.key])
        else:
            data.selected.moveNoteUpBass(data.keySignatures[data.key])
    elif event.keysym == "Down" and data.selected != None:
        if isNoteInRightHand(data.selected, data.fullSongPages\
                                [data.currentFullSongPage].rightHandMeasures):
            data.selected.moveNoteDownTreble(data.keySignatures[data.key])
        else:
            data.selected.moveNoteDownBass(data.keySignatures[data.key])
    elif event.keysym == "Left" and data.selected != None:
        newIndices = previousSelect(data.fullSongPages\
                                    [data.currentFullSongPage], data.selected)
        newMeasureIndex = newIndices[0]
        newNoteIndex = newIndices[1]
        if isNoteInRightHand(data.selected, data.fullSongPages\
                                [data.currentFullSongPage].rightHandMeasures):
            data.selected = data.fullSongPages[data.currentFullSongPage].\
                        rightHandMeasures[newMeasureIndex].notes[newNoteIndex]
        else:
            data.selected = data.fullSongPages[data.currentFullSongPage].\
                        leftHandMeasures[newMeasureIndex].notes[newNoteIndex]
    elif event.keysym == "Right" and data.selected != None:
        newIndices = nextSelect(data.fullSongPages[data.currentFullSongPage], 
                                                                data.selected)
        newMeasureIndex = newIndices[0]
        newNoteIndex = newIndices[1]
        if isNoteInRightHand(data.selected, data.fullSongPages\
                                [data.currentFullSongPage].rightHandMeasures):
            data.selected = data.fullSongPages[data.currentFullSongPage].\
                        rightHandMeasures[newMeasureIndex].notes[newNoteIndex]
        else:
            data.selected = data.fullSongPages[data.currentFullSongPage].\
                        leftHandMeasures[newMeasureIndex].notes[newNoteIndex]
    elif data.selected != None and (event.char == chr(127) or \
                                                        event.char == chr(8)):
        data.selected.pitch = "0"
        data.selected.octave = 0
        data.selected = None
    elif event.keysym == "space":
        if data.playFullSong == False:
            data.currentFullSongPage = 0
            data.noteNum = 0
            data.playFullSong = True
            data.fullSongCombinedHands = combineHands(data.fullSong, 
                                                    data.fullSongLeftHand)
        else:
            data.playFullSong = False
            data.noteNum = 0

def keyPressedInfoScreen(event, data):
    if data.enterTitleMode == True:
        keyPressedCustomTitle(event, data)
    elif data.enterComposerMode == True:
        keyPressedCustomComposer(event, data)
        
def keyPressedCompletedSongScreen(event, data):
    if event.keysym == "space":
        if data.playFullSong == False:
            data.currentCompletedSongPage = 0
            data.fullSongCombinedHands = combineHands(data.fullSong, 
                                                    data.fullSongLeftHand)
            data.playFullSong = True
            data.noteNum = 0
        else:
            data.playFullSong = False
            data.noteNum = 0

def keyPressed(event, data):
    if data.generalQuestionsScreen == True:
        keyPressedGeneralQuestionsScreen(event, data)
    elif data.melodyScreen == True:
        keyPressedMelodyQuestionsScreen(event, data)
    elif data.melodyPlaybackScreen == True:
        keyPressedMelodyPlaybackScreen(event, data)
    elif data.developmentScreen == True:
        keyPressedDevelopmentScreen(event, data)
    elif data.developmentPlaybackScreen == True:
        keyPressedDevelopmentPlaybackScreen(event, data)
    elif data.sectionCScreen == True:
        keyPressedSectionCScreen(event, data)
    elif data.sectionCPlaybackScreen == True:
        keyPressedSectionCPlaybackScreen(event, data)
    elif data.fullSongPlaybackScreen == True:
        keyPressedFullSongPlaybackScreen(event, data) 
    elif data.infoScreen == True:
        keyPressedInfoScreen(event, data)
    elif data.completedSongScreen == True:
        keyPressedCompletedSongScreen(event, data)
    if event.char == "h" and data.infoScreen != True:
        if data.help == False:
            data.help = True
        else:
            data.help = False
            
##Timer Fired:
def timerFired(data):
    if data.save == True:
        data.counter += 1
        #saves a page every second
        if data.counter % 10 == 0:
            if data.currentCompletedSongPage < len(data.completedSongPages) - 1:
                data.currentCompletedSongPage += 1
            else:
                data.completedSongScreen = True
                data.currentCompletedSongPage = 0
                data.save = False
    elif data.playMelody == True:
        playMusic(data, data.melodyCombinedHands)
        data.metronome += 1
        if data.noteNum % 128 == 0 and data.currentMelodyPage != \
                                                    len(data.melodyPages) - 1:
            data.currentMelodyPage += 1
            data.selected = None
    elif data.playDevelopment == True:
        playMusic(data, data.developmentCombinedHands)
        data.metronome += 1
        if data.noteNum % 128 == 0 and data.currentDevelopmentPage != \
                                                len(data.developmentPages) - 1:
            data.currentDevelopmentPage += 1
            data.selected = None
    elif data.playSectionC == True:
        playMusic(data, data.sectionCCombinedHands)
        data.metronome += 1
        if data.noteNum % 128 == 0 and data.currentSectionCPage != \
                                                len(data.sectionCPages) - 1:
            data.currentSectionCPage += 1
            data.selected = None
    elif data.playFullSong == True:
        playMusic(data, data.fullSongCombinedHands)
        data.metronome += 1
        if data.noteNum % 128 == 0 and data.currentFullSongPage != \
                                len(data.fullSongPages) - 1 and \
                                data.completedSongScreen == False:
            data.currentFullSongPage += 1
            data.selected = None
            
##Play Music:
#combines the right hand and left hand notes into lists of two notes
#threading from     https://docs.python.org/3/library/threading.html
#plays the music
def playMusic(data, combinedHands):
    #determines how often every sixteenth should be played
    timeUnit = int(600 / data.tempo / 4)
    if data.metronome % timeUnit == 0 and data.metronome >= 0:
        if data.noteNum != len(combinedHands):
            rightNote = combinedHands[data.noteNum][0][0]
            leftNote = combinedHands[data.noteNum][1][0]
            #checks if notes are rests
            if rightNote != None and rightNote.pitch == "0" and \
                                                        rightNote.octave == 0:
                rightNote = None
            if leftNote != None and leftNote.pitch == "0" and \
                                                        leftNote.octave == 0:
                leftNote = None
            if rightNote != None and leftNote == None:
                rightNotePitch = rightNote.pitch
                rightNoteOctave = rightNote.octave
                file = "PianoKeys/" + str(rightNotePitch) + \
                                                str(rightNoteOctave) + ".wav"
                Thread(target=play, args=(file,)).start()
            elif leftNote != None and rightNote == None:
                leftNotePitch = leftNote.pitch
                leftNoteOctave = leftNote.octave
                file = "PianoKeys/" + str(leftNotePitch) + \
                                                str(leftNoteOctave) + ".wav"
                Thread(target=play, args=(file,)).start()
            elif rightNote != None and leftNote != None:
                rightNotePitch = rightNote.pitch
                rightNoteOctave = rightNote.octave
                leftNotePitch = leftNote.pitch
                leftNoteOctave = leftNote.octave
                file1 = "PianoKeys/" + str(rightNotePitch) + \
                                                str(rightNoteOctave) + ".wav"
                file2 = "PianoKeys/" + str(leftNotePitch) + \
                                                str(leftNoteOctave) + ".wav"
                Thread(target=playMultipleFiles, args=(file1, file2)).start()
            data.noteNum += 1
        else:
            data.playMelody = False
            data.playDevelopment = False
            data.playSectionC = False
            data.playFullSong = False
            data.noteNum = 0

#combines the right hand and left hand by placing their notes in spots 
#split up by every sixteenth
def combineHands(rightHand, leftHand):
    combinedNotes = []
    for measure in rightHand:
        for note in measure.notes:
            length = note.length
            units = int(length / (1/16))
            combinedNotes.append([[note], [None]])
            for i in range(units - 1):
                combinedNotes.append([[None], [None]])
    lengthTracker = 0
    for measure in leftHand:
        for note in measure.notes:
            length = note.length
            index = int(lengthTracker / (1/16))
            combinedNotes[index][1] = [note]
            lengthTracker += length
    return combinedNotes
                
#got code from https://abhgog.gitbooks.io/pyaudio-manual/sample-project.html
def mixNotes(*args):
    if(len(args) >= 1):
        currentFile = args[0]
        for index in range(1, len(args)):
            sound1 = AudioSegment.from_wav(currentFile)
            sound2 = AudioSegment.from_wav(args[index])
            combined = sound1.overlay(sound2)
            name = str(currentFile) + str(args[index])[10:]
            combined.export(name, format='wav')
            currentFile = name
        chord = AudioSegment.from_wav(currentFile)
        chord.export(currentFile, format="wav")
    return currentFile

def play(file):
    CHUNK = 1024 #measured in bytes

    wf = wave.open(file, 'rb')

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(CHUNK)

    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()

    p.terminate()

def deleteFile(file):
    os.remove(file)

def playMultipleFiles(*files):
    newFile = mixNotes(*files)
    play(newFile)
    try:
        deleteFile(newFile)
    except:
        pass



##Draw Functions:
##Repeated Helper Functions
def drawLengthChoices(canvas, data, section):
    lengthChoices = [1, 2, 3, 4, 5, 6, 7, 8]
    spacing = (data.width - 8 * 40) / 9
    distance = 40 + spacing
    canvas.create_text(data.width / 2, 25, 
                        text=section + " Length (in measures)", font="Arial 20")
    for i in range(8):
        if section == "Melody" and lengthChoices[i] == data.melodyLength:
            color = "lavender"
        elif section == "Development" and \
                                lengthChoices[i] * 4 == data.developmentLength:
            color = "lavender"
        elif section == "Section C" and \
                                lengthChoices[i] * 4 == data.sectionCLength:
            color = "lavender"
        else:
            color = "azure"
        canvas.create_rectangle(spacing + i * distance, 50, 
            spacing + 40 + i * distance, 90, fill=color)
        if section == "Melody":
            canvas.create_text(spacing + 20 + i * distance, 70, 
                                        text=lengthChoices[i])
        elif section == "Development" or section == "Section C":
            canvas.create_text(spacing + 20 + i * distance, 70, 
                                        text=4 * lengthChoices[i])

def drawChordProgressionChoices(canvas, data, section):
    canvas.create_text(data.width / 2, 125, text="Chord Progression", 
                                                    font="Arial 20")
    spacing = (data.width - (6 * 90)) / 7
    distance = 90 + spacing
    #shows recommended major progressions if selected key is major
    if data.major == True:
        for i in range(6):
            if section == "Melody" and \
                        data.chordProgression == data.majorChordProgressions[i]:
                color = "lavender"
            elif section == "Development" and data.developmentChordProgression \
                                            == data.majorChordProgressions[i]:
                color = "lavender"
            elif section == "Section C" and data.sectionCChordProgression == \
                                                data.majorChordProgressions[i]:
                color = "lavender"
            else:
                color = "azure"
                
            canvas.create_rectangle(spacing + i * distance, 150, 
                spacing + 90 + i * distance, 190, fill=color)
            canvas.create_text(spacing + 45 + i * distance, 170, 
                text=displayChordProgressions(data.majorChordProgressions[i]), 
                                                    font="Arial 13")
    #shows recommended minor progressions if selected key is minor
    else:
        for i in range(6):
            if section == "Melody" and data.chordProgression == \
                                                data.minorChordProgressions[i]:
                color = "lavender"
            elif section == "Development" and data.developmentChordProgression \
                                            == data.minorChordProgressions[i]:
                color = "lavender"
            elif section == "Section C" and data.sectionCChordProgression \
                                            == data.minorChordProgressions[i]:
                color = "lavender"
            else:
                color = "azure"
            canvas.create_rectangle(spacing + i * distance, 150, 
                spacing + 90 + i * distance, 190, fill=color)
            canvas.create_text(spacing + 45 + i * distance, 170, 
                text=displayChordProgressions(data.minorChordProgressions[i]), 
                                                            font="Arial 13")
    #custom
    if section == "Melody":
        if data.chordProgression == \
                            convertChordProgression(data.enterChordProgression):
            color = "lavender"
        else:
            color = "azure"
        progression = data.enterChordProgression
    elif section == "Development":
        if data.developmentChordProgression == \
                convertChordProgression(data.enterDevelopmentChordProgression):
            color = "lavender"
        else:
            color = "azure"
        progression = data.enterDevelopmentChordProgression
    elif section == "Section C":
        if data.sectionCChordProgression == \
                    convertChordProgression(data.enterSectionCChordProgression):
            color = "lavender"
        else:
            color = "azure"
        progression = data.enterSectionCChordProgression
    canvas.create_rectangle(data.width / 2 - 60, 190 + spacing, 
                                data.width / 2 + 60, 230 + spacing, fill=color)
    canvas.create_text(data.width / 2, 210 + spacing, text=progression, 
                                                                font="Arial 13")
    if data.enterChordProgressionMode == True or \
                        data.enterDevelopmentChordProgressionMode == True or \
                        data.enterSectionCChordProgressionMode == True:
        canvas.create_text(data.width / 2 + 150, 210 + spacing, 
                                text="Press 'Enter' when done", font="Arial 15")
        canvas.create_text(data.width / 2 - 170, 210 + spacing, 
                text="Press 'h' for help inserting\ncustom left hand pattern", 
                                                        font="Arial 15")
#draws left hand pattern choices
def drawLeftHandPatternChoices(canvas, data, section):
    canvas.create_text(data.width / 2, 290, text="Left Hand Pattern", 
                                                        font="Arial 20")
    spacing = (data.width - (3 * 110)) / 4
    distance = 110 + spacing
    for i in range(3):
        if section == "Melody" and data.leftHandPattern == \
                                            data.leftHandPatternSelection[i]:
            color = "lavender"
        elif section == "Development" and data.developmentLeftHandPattern == \
                                            data.leftHandPatternSelection[i]:
            color = "lavender"
        elif section == "Section C" and data.sectionCLeftHandPattern == \
                                        data.leftHandPatternSelection[i]:
            color = "lavender"
        else:
            color = "azure"
        canvas.create_rectangle(spacing + i * distance, 315, 
            spacing + 110 + i * distance, 355, fill=color)
        canvas.create_text(spacing + 55 + i * distance, 335,
            text=data.leftHandPatternSelection[i])
    #custom
    if section == "Melody":
        if data.leftHandPattern == data.enterLeftHandPattern:
            color = "lavender"
        else:
            color = "azure"
        pattern = data.enterLeftHandPattern
    elif section == "Development":
        if data.developmentLeftHandPattern == \
                                        data.enterDevelopmentLeftHandPattern:
            color = "lavender"
        else:
            color = "azure"
        pattern = data.enterDevelopmentLeftHandPattern
    elif section == "Section C":
        if data.sectionCLeftHandPattern == data.enterSectionCLeftHandPattern:
            color = "lavender"
        else:
            color = "azure"
        pattern = data.enterSectionCLeftHandPattern
    canvas.create_rectangle(data.width / 2 - 100, 380, data.width / 2 + 100, 
                                                            420, fill=color)
    canvas.create_text(data.width / 2, 400, text=pattern, font="Arial 13")
    if data.enterLeftHandPatternMode == True or \
                        data.enterDevelopmentLeftHandPatternMode == True or \
                        data.enterSectionCLeftHandPatternMode == True:
        canvas.create_text(data.width / 2 + 190, 400, 
                                text="Press 'Enter' when done", font="Arial 15")
        canvas.create_text(data.width / 2 - 200, 400, 
        text="Press 'h' for help inserting\ncustom left hand pattern", 
                                                                font="Arial 15")
            
#draws note allocation choices
def drawNoteAllocation(canvas, data, section):
    canvas.create_text(25, 450, text="Note Allocation (not exact)",
                                            font="Arial 20", anchor=W)
    canvas.create_text(25, 500, text="Percentage of Whole notes:", 
                                            font="Arial 16", anchor=W)
    canvas.create_text(25, 550, text="Percentage of Half notes:", 
                                            font="Arial 16", anchor=W)
    canvas.create_text(25, 600, text="Percentage of Quarter notes:", 
                                            font="Arial 16", anchor=W)
    canvas.create_text(25, 650, text="Percentage of Eighth note pairs:", 
                                            font="Arial 16", anchor=W)
    canvas.create_text(25, 700, text="Percentage of Sixteenth note quartets:", 
                                            font="Arial 16", anchor=W)
    spacing = 50
    center = data.width / 2
    for i in range(5):
        #main box
        canvas.create_rectangle(center - 20, 480 + i * spacing, center + 20, 
                                                            520 + i * spacing)
        key = 1 / (2 ** i)
        #increase box
        canvas.create_rectangle(center + 40, 480 + i * spacing + 10, 
                            center + 60, 520 + i * spacing - 10, fill="azure")
        canvas.create_text(center + 50, 503 + i * spacing, 
                                                text="^", font="Arial 20")
        #decrease box
        canvas.create_rectangle(center - 60, 480 + i * spacing + 10, 
                            center - 40, 520 + i * spacing - 10, fill="azure")
        canvas.create_text(center - 50, 499 + i * spacing, text="v", 
                                                            font="Arial 19")
                
        #text
        if section == "Melody":
            canvas.create_text(center, 500 + i * spacing, 
                                text=str(data.noteAllocation[key]))
        elif section == "Development":
            canvas.create_text(center, 500 + i * spacing, 
                                text=str(data.developmentNoteAllocation[key]))
        elif section == "Section C":
            canvas.create_text(center, 500 + i * spacing, 
                                text=str(data.sectionCNoteAllocation[key]))

            
def drawHarmony(canvas, data, section):
    canvas.create_text(data.width - 125, 450, text="Harmony", font="Arial 20")
    canvas.create_rectangle(data.width - 145, 475, data.width - 105, 515)
    #increase box
    canvas.create_rectangle(data.width - 85, 485, data.width - 65, 505, 
                                                                fill="azure")
    canvas.create_text(data.width - 75, 498, text="^", font="Arial 20")
    #decrease box
    canvas.create_rectangle(data.width - 185, 485, data.width - 165, 505, 
                                                                fill="azure")
    canvas.create_text(data.width - 175, 495, text="v", font="Arial 19")
    #text
    if section == "Melody":
        canvas.create_text(data.width - 125, 495, text=data.melodyHarmony)
    elif section == "Development":
        canvas.create_text(data.width - 125, 495, text=data.developmentHarmony)
    elif section == "Section C":
        canvas.create_text(data.width - 125, 495, text=data.sectionCHarmony)
        
def drawRepetition(canvas, data, section):
    canvas.create_text(data.width - 125, 600, text=section + " Repetition", 
                                                                font="Arial 20")
    canvas.create_rectangle(data.width - 105, 625, data.width - 145, 665)
    #increase box
    canvas.create_rectangle(data.width - 85, 635, data.width - 65, 655, 
                                                                fill="azure")
    canvas.create_text(data.width - 75, 648, text="^", font="Arial 20")
    #decreasee box
    canvas.create_rectangle(data.width - 185, 635, data.width - 165, 655, 
                                                                fill="azure")
    canvas.create_text(data.width - 175, 644, text="v", font="Arial 19")
    if section == "Melody":
        canvas.create_text(data.width - 125, 645, text=data.melodyRepetition)
    elif section == "Development":
        canvas.create_text(data.width - 125, 645, 
                                                text=data.developmentRepetition)
    elif section == "Section C":
        canvas.create_text(data.width - 125, 645, text=data.sectionCRepetition)

def drawSharp(canvas, x, y):
    canvas.create_line(x - 2, y - 9, x - 2, y + 9, width=2)
    canvas.create_line(x + 2, y - 9, x + 2, y + 9, width=2)
    canvas.create_line(x - 9, y - 3.6, x + 9, y - 4.6, width=2)
    canvas.create_line(x - 9, y + 4.6, x + 9, y + 3.6, width=2) 


def drawFlat(canvas, x, y):
    #canvas.create_text(x, y, text="b", font="system 15")
    icon1 = PhotoImage(file="Images/flat.png")
    flat = Label(image = icon1)
    flat.image = icon1
    flat.pack
    canvas.create_image(x, y - 5, image=icon1)

def drawTimeSignature(canvas, x, y, timeSignature):
    bottomNumber = 4
    topNumber = int(bottomNumber * timeSignature)
    canvas.create_text(x, y + 10, text=topNumber, font="msserif 26")
    canvas.create_text(x, y + 30, text=bottomNumber, font="msserif 26")
    canvas.create_text(x, y + 90, text=topNumber, font="msserif 26")
    canvas.create_text(x, y + 110, text=bottomNumber, font="msserif 26")

#y is F line on treble clef
def drawKeySignature(canvas, y, keySignature, timeSignature):
    x = 110
    if "F#" in keySignature:
        drawSharp(canvas, 105, y)
        drawSharp(canvas, 105, y + 90)
        x += 13
        if "C#" in keySignature:
            drawSharp(canvas, 115, y + 15)
            drawSharp(canvas, 115, y + 105)
            x += 13
        if "G#" in keySignature:
            drawSharp(canvas, 125, y - 5)
            drawSharp(canvas, 125, y + 85)
            x += 13
        if "D#" in keySignature:
            drawSharp(canvas, 135, y + 10)
            drawSharp(canvas, 135, y + 100)
            x += 13
        if "A#" in keySignature:
            drawSharp(canvas, 145, y + 25)
            drawSharp(canvas, 145, y + 115)
            x += 10
        if "E#" in keySignature:
            drawSharp(canvas, 155, y + 5)
            drawSharp(canvas, 155, y + 95)
            x += 10
        if "B#" in keySignature:
            drawSharp(canvas, 165, y + 20)
            drawSharp(canvas, 165, y + 110)
            x += 10
    elif "Bb" in keySignature:
        drawFlat(canvas, 105, y + 20)
        drawFlat(canvas, 105, y + 110)
        x += 13
        if "Eb" in keySignature:
            drawFlat(canvas, 116, y + 5)
            drawFlat(canvas, 116, y + 95)
            x += 13
        if "Ab" in keySignature:
            drawFlat(canvas, 127, y + 25)
            drawFlat(canvas, 127, y + 115)
            x += 13
        if "Db" in keySignature:
            drawFlat(canvas, 138, y + 10)
            drawFlat(canvas, 138, y + 100)
            x += 13
        if "Gb" in keySignature:
            drawFlat(canvas, 149, y + 30)
            drawFlat(canvas, 149, y + 120)
            x += 12
        if "Cb" in keySignature:
            drawFlat(canvas, 160, y + 15)
            drawFlat(canvas, 160, y + 105)
            x += 11
        if "Fb" in keySignature:
            drawFlat(canvas, 171, y + 35)
            drawFlat(canvas, 171, y + 125)
            x += 10
    drawTimeSignature(canvas, x, y, timeSignature)
    
def drawQuestionsBackButton(canvas, data):
    canvas.create_rectangle(data.width / 2 - 100, data.height - 75, 
                            data.width / 2 - 20, data.height - 25, fill="azure")
    canvas.create_text(data.width / 2 - 60, data.height - 50, text="Back", 
                                                                font="Arial 30")
    
def drawQuestionsNextButton(canvas, data):
    canvas.create_rectangle(data.width / 2 + 20, data.height - 75, 
                        data.width / 2 + 100, data.height - 25, fill="azure")
    canvas.create_text(data.width / 2 + 60, data.height - 50, text="Next", 
                                                            font="Arial 30")
    
def drawPreviousPageButton(canvas, data):
    center = 50 + (data.height / 4.5) * 2 - (data.height / 4.5 - 120) / 2
    canvas.create_rectangle(10, center - 15, 40, center + 15, fill="azure")
    canvas.create_text(25, center, text="<", font="Arial 15")
    canvas.create_text(25, center + 30, text="Previous\n  Page", 
                                                            font="Arial 10")

def drawNextPageButton(canvas, data):
    center = 50 + (data.height / 4.5) * 2 - (data.height / 4.5 - 120) / 2
    canvas.create_rectangle(data.width - 40, center - 15, data.width - 10, 
                                                    center + 15, fill="azure")
    canvas.create_text(data.width - 25, center, text=">", font="Arial 15")
    canvas.create_text(data.width - 25, center + 30, text="Next\nPage", 
                                                            font="Arial 10")

def drawErrorMessageAllocation(canvas, data):
    canvas.create_text(data.width / 2, 440, 
            text="Note allocation percentages", fill="red")
    canvas.create_text(data.width / 2, 460, 
            text="must sum to 100%", fill="red")
            
def drawErrorMessageIncomplete(canvas, data):
    canvas.create_text(data.width / 2, 735, 
        text="You must select a specification for each category", fill="red")
    
            

##General Questions Screen:
def drawKeyChoices(canvas, data):
    canvas.create_text(data.width / 2, 20, text="Key:", font="Arial 20")
    majorKeys1 = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#']
    majorKeys2 = ['F', 'Bb', 'Eb', 'Ab', 'Db', 'Gb', 'Cb']
    minorKeys1 = ['a', 'e', 'b', 'f#', 'c#', 'g#', 'd#', 'a#']
    minorKeys2 = ['d', 'g', 'c', 'f', 'bb', 'eb', 'ab']
    #major keys
    spacing = (data.width - 8 * 40) / 9
    distance = 40 + spacing
    canvas.create_text(spacing, 40, text="Major keys:", anchor=W)
    for i in range(8):
        if data.key == majorKeys1[i]:
            color = "lavender"
        else:
            color = "azure"
        canvas.create_rectangle(spacing + i * distance, 50, 
            spacing + 40 + i * distance, 90, fill=color)
        canvas.create_text(spacing + 20 + i * distance, 70, text=majorKeys1[i])
    for i in range(7):
        if data.key == majorKeys2[i]:
            color = "lavender"
        else:
            color = "azure"
        canvas.create_rectangle(spacing + i * distance, 114, 
            spacing + 40 + i * distance, 154, fill=color)
        canvas.create_text(spacing + 20 + i * distance, 134, text=majorKeys2[i])
    #minor keys
    canvas.create_text(spacing, 168, text="Minor keys:", anchor=W)
    for i in range(8):
        if data.key == minorKeys1[i]:
            color = "lavender"
        else:
            color = "azure"
        canvas.create_rectangle(spacing + i * distance, 178, 
            spacing + 40 + i * distance, 218, fill=color)
        canvas.create_text(spacing + 20 + i * distance, 198, text=minorKeys1[i])
    for i in range(7):
        if data.key == minorKeys2[i]:
            color = "lavender"
        else:
            color = "azure"
        canvas.create_rectangle(spacing + i * distance, 242, 
            spacing + 40 + i * distance, 282, fill=color)
        canvas.create_text(spacing + 20 + i * distance, 262, text=minorKeys2[i])

#draws structure choices
def drawStructureChoices(canvas, data):
    canvas.create_text(data.width / 2, 325, text="Structure:", font="Arial 20")
    structures = ['ABA', 'ABAB', 'ABACABA', 'ABCBA']
    spacing = (data.width - 80 * 4) / 5
    distance = 80 + spacing
    for i in range(4):
        if data.structure == structures[i]:
            color = "lavender"
        else:
            color = "azure"
        canvas.create_rectangle(spacing + i * distance, 355, 
            spacing + 80 + i * distance, 395, fill=color)
        canvas.create_text(spacing + 40 + i * distance, 375, text=structures[i])
    #custom
    if data.structure == data.enterStructure:
        color = "lavender"
    else:
        color = "azure"
    canvas.create_rectangle(data.width / 2 - 60, 430, data.width / 2 + 60, 470, 
                                                                    fill=color)
    canvas.create_text(data.width / 2, 450, text=data.enterStructure, 
                                                                font="Arial 15")
    if data.enterStructureMode == True:
        canvas.create_text(data.width / 2 + 150, 450, 
                    text="Press 'Enter' when done\nMust contain only A, B, C's", 
                    font="Arial 15", anchor=W)

#draws structure choices
def drawTimeSignatureChoices(canvas, data):
    canvas.create_text(data.width / 2, 515, text="Time Signature:", 
        font="Arial 20")
    timeSignatures = [(4, 4), (3, 4), (2, 4)]      #each choice will be 40 wide
    spacing = 60
    distance = 40 + spacing
    start = data.width / 2 - 20 - distance
    for k in range(3):
        if timeSignatures[k][0] / + timeSignatures[k][1] == data.timeSignature:
            color = "lavender"
        else:
            color = "azure"
        canvas.create_rectangle(start + distance * k, 545, 
                                start + 40 + (distance * k), 625, fill=color)
        canvas.create_text(start + (distance * k) + 20, 565, 
                                                text=str(timeSignatures[k][0]))
        canvas.create_text(start + (distance * k) + 20, 605, 
                                                text=str(timeSignatures[k][1]))

def drawTempo(canvas, data):
    canvas.create_text(data.width / 2, 660, text="Tempo:", font="Arial 20")
    #main box
    canvas.create_rectangle(data.width / 2 - 30, 690, data.width / 2 + 30, 730)
    canvas.create_text(data.width / 2, 710, text=data.tempo)
    #decrease box
    canvas.create_rectangle(data.width / 2 - 70, 700, data.width / 2 - 50, 720, 
                                                                fill="azure")
    canvas.create_text(data.width / 2 - 60, 709, text="v", font="Arial 19")
    #increase box
    canvas.create_rectangle(data.width / 2 + 50, 700, data.width / 2 + 70, 720, 
                                                                fill="azure")
    canvas.create_text(data.width / 2 + 60, 713, text="^", font="Arial 20")

def drawBackButton(canvas, data):
    canvas.create_rectangle(data.width / 2 - 190, data.height - 75, 
                        data.width / 2 - 90, data.height - 25, fill="azure")
    canvas.create_text(data.width / 2 - 140, data.height - 50, text="Back", 
                        font="Arial 30")

def drawPlayButton(canvas, data, x):
    canvas.create_rectangle(x - 50, data.height - 75, 
                        x + 50, data.height - 25, fill="azure")
    canvas.create_polygon(x - 15, data.height - 40, 
                                x - 15, data.height - 60, 
                                x + 15, data.height - 50)
                        
def drawStopButton(canvas, data, x):
    canvas.create_rectangle(x - 50, data.height - 75, 
                            x + 50, data.height - 25, fill="azure")
    canvas.create_rectangle(x  - 15, data.height - 35, 
                            x + 15, data.height - 65, fill="black")

def drawNextButton(canvas, data):
    canvas.create_rectangle(data.width / 2 + 90, data.height - 75, 
                        data.width / 2 + 190, data.height - 25, fill="azure")
    canvas.create_text(data.width / 2 + 140, data.height - 50, text="Next", 
                        font="Arial 30")
##General Questions Screen:
def drawGeneralQuestionsScreen(canvas, data):
    drawKeyChoices(canvas, data)
    drawStructureChoices(canvas, data)
    drawTimeSignatureChoices(canvas, data)
    drawTempo(canvas, data)
    #next button
    canvas.create_rectangle(data.width / 2 - 40, data.height - 75, 
                            data.width / 2 + 40, data.height - 25, fill="azure")
    canvas.create_text(data.width / 2, data.height - 50, text="Next", 
                                                    font="Arial 30")
    
    
##Melody Questions Screen:
def drawMelodyScreen(canvas, data):
    drawLengthChoices(canvas, data, "Melody")
    drawChordProgressionChoices(canvas, data, "Melody")
    drawLeftHandPatternChoices(canvas, data, "Melody")
    drawNoteAllocation(canvas, data, "Melody")
    drawHarmony(canvas, data, "Melody")
    drawRepetition(canvas, data, "Melody")
    drawQuestionsBackButton(canvas, data)
    drawQuestionsNextButton(canvas, data)
    if data.errorMessageAllocation == True:
        drawErrorMessageAllocation(canvas, data)
    if data.errorMessageIncomplete == True:
        drawErrorMessageIncomplete(canvas, data)
        
##Melody Playback Screen:
def drawMelodyPlaybackScreen(canvas, data):
    #sheet music with notes
    data.melodyPages[data.currentMelodyPage].draw(canvas, 
                            data.keySignatures[data.key], data.timeSignature)
    drawBackButton(canvas, data)
    drawNextButton(canvas, data)
    if data.playMelody == True:
        drawStopButton(canvas, data, data.width / 2)
    else:
        drawPlayButton(canvas, data, data.width / 2)
    canvas.create_text(data.width / 2, data.height - 10, 
                                text="Press 'h' for help | 'r' to regenerate")
    if data.playMelody == False:
        #next page button
        if data.currentMelodyPage != len(data.melodyPages) - 1:
            drawNextPageButton(canvas, data)
        #next page button
        if data.currentMelodyPage != 0:
            drawPreviousPageButton(canvas, data)

##Development Screen:
def drawDevelopmentScreen(canvas, data):
    drawLengthChoices(canvas, data, "Development")
    drawChordProgressionChoices(canvas, data, "Development")
    drawLeftHandPatternChoices(canvas, data, "Development")
    drawNoteAllocation(canvas, data, "Development")
    drawHarmony(canvas, data, "Development")
    drawRepetition(canvas, data, "Development")
    drawQuestionsBackButton(canvas, data)
    drawQuestionsNextButton(canvas, data)
    if data.errorMessageAllocation == True:
        drawErrorMessageAllocation(canvas, data)
    if data.errorMessageIncomplete == True:
        drawErrorMessageIncomplete(canvas, data)
##Development Playback Screen:
def drawDevelopmentPlaybackScreen(canvas, data):
    data.developmentPages[data.currentDevelopmentPage].draw(canvas, 
                            data.keySignatures[data.key], data.timeSignature)
    drawBackButton(canvas, data)
    drawNextButton(canvas, data)
    #play button
    if data.playDevelopment == True:
        drawStopButton(canvas, data, data.width / 2)
    else:
        drawPlayButton(canvas, data, data.width / 2)
    #help text
    canvas.create_text(data.width / 2, data.height - 10, 
                                text="Press 'h' for help | 'r' to regenerate")
    if data.playDevelopment == False:
        #next page button
        if data.currentDevelopmentPage != len(data.developmentPages) - 1:
            drawNextPageButton(canvas, data)
        #next page button
        if data.currentDevelopmentPage != 0:
            drawPreviousPageButton(canvas, data)
        
##Section C Questions Screen:
def drawSectionCScreen(canvas, data):
    drawLengthChoices(canvas, data, "Section C")
    drawChordProgressionChoices(canvas, data, "Section C")
    drawLeftHandPatternChoices(canvas, data, "Section C")
    drawNoteAllocation(canvas, data, "Section C")
    drawHarmony(canvas, data, "Section C")
    drawRepetition(canvas, data, "Section C")
    drawQuestionsBackButton(canvas, data)
    drawQuestionsNextButton(canvas, data)
    if data.errorMessageAllocation == True:
        drawErrorMessageAllocation(canvas, data)
    if data.errorMessageIncomplete == True:
        drawErrorMessageIncomplete(canvas, data)
        
##Section C Playback Screen:
def drawSectionCPlaybackScreen(canvas, data):
    data.sectionCPages[data.currentSectionCPage].draw(canvas, 
                            data.keySignatures[data.key], data.timeSignature)
    drawBackButton(canvas, data)
    drawNextButton(canvas, data)
    if data.playSectionC == True:
        drawStopButton(canvas, data, data.width / 2)
    else:
        drawPlayButton(canvas, data, data.width / 2)
    #help text
    canvas.create_text(data.width / 2, data.height - 10, 
                                text="Press 'h' for help | 'r' to regenerate")
    if data.playSectionC == False:
        #next page button
        if data.currentSectionCPage != len(data.sectionCPages) - 1:
            drawNextPageButton(canvas, data)
        #next page button
        if data.currentSectionCPage != 0:
            drawPreviousPageButton(canvas, data)
        
##Full Song Playback Screen:        
def drawFullSongPlaybackScreen(canvas, data):
    data.fullSongPages[data.currentFullSongPage].draw(canvas, 
                            data.keySignatures[data.key], data.timeSignature)
    drawBackButton(canvas, data)
    drawNextButton(canvas, data)
    #play button
    if data.playFullSong == True:
        drawStopButton(canvas, data, data.width / 2)
    else:
        drawPlayButton(canvas, data, data.width / 2)
    if data.playFullSong == False:
        #next page button
        if data.currentFullSongPage != len(data.fullSongPages) - 1:
            drawNextPageButton(canvas, data)
        #previous page button
        if data.currentFullSongPage != 0:
            drawPreviousPageButton(canvas, data)
    canvas.create_text(data.width / 2, data.height - 10, 
                                                    text="Press 'h' for help")
    canvas.create_text(data.width / 7, data.height - 50, 
                                            text="Full Song", font="Arial 20")
 
##Information Screen:
def drawInfoScreen(canvas, data):
    titleWidth = 1
    composerWidth = 1
    if data.enterTitleMode == True:
        titleWidth = 3
    elif data.enterComposerMode == True:
        composerWidth = 3
    #title box
    canvas.create_text(data.width / 2, data.height / 2 - 150, 
                                                text="Title", font="Arial 30")
    canvas.create_rectangle(data.width / 2 - 200, data.height / 2 - 120, 
                data.width / 2 + 200, data.height / 2 - 70, width=titleWidth)
    canvas.create_text(data.width / 2, data.height / 2 - 95, 
                                            text=data.title, font="Arial 25")
    #composer box
    canvas.create_text(data.width / 2, data.height / 2 + 40, text="Name", 
                                                            font="Arial 30")
    canvas.create_rectangle(data.width / 2 - 200, data.height / 2 + 70, 
                                data.width / 2 + 200, data.height / 2 + 120, 
                                                        width=composerWidth)
    canvas.create_text(data.width / 2, data.height / 2 + 95, text=data.composer, 
                                                            font="Arial 25")
    #next and back buttons
    drawQuestionsBackButton(canvas, data)
    drawQuestionsNextButton(canvas, data)
 
##Compelted Song Screen
def drawCompletedSongScreen(canvas, data):
    data.completedSongPages[data.currentCompletedSongPage].draw(canvas, 
                            data.keySignatures[data.key], data.timeSignature)
    if data.save == False:
        #previous button
        canvas.create_rectangle(data.width / 2 - 260, data.height - 75, 
                        data.width / 2 - 160, data.height - 25, fill="azure")
        canvas.create_text(data.width / 2 - 210, data.height - 50, text="Back", 
                                                            font="Arial 30")
        #play button
        if data.playFullSong == True:
            drawStopButton(canvas, data, data.width / 2 - 70)
        else:
            drawPlayButton(canvas, data, data.width / 2 - 70)
        #save button
        canvas.create_rectangle(data.width / 2 + 20, data.height - 75, 
                        data.width / 2 + 120, data.height - 25, fill="azure")
        canvas.create_text(data.width / 2 + 70, data.height - 50, text="Save", 
                                                                font="Arial 30")
        #restart button
        canvas.create_rectangle(data.width / 2 + 160, data.height - 75, 
                        data.width / 2 + 260, data.height - 25, fill="azure")
        canvas.create_text(data.width / 2 + 210, data.height - 50, 
                                                text="Restart", font="Arial 30")
        #next page button
        if data.currentCompletedSongPage != len(data.completedSongPages) - 1:
            drawNextPageButton(canvas, data)
        #previous page button
        if data.currentCompletedSongPage != 0:
            drawPreviousPageButton(canvas, data)
    
#saves every page by drawing each page every second and saving each to a folder
def saveSheet(canvas, data):
    data.completedSongPages[data.currentCompletedSongPage].draw(canvas, 
                            data.keySignatures[data.key], data.timeSignature)
    name = "SavedMusic/" + str(data.title) + " %d.ps" % \
                                            (data.currentCompletedSongPage + 1)
    canvas.update()
    canvas.postscript(file=name, colormode='color')

#help/info screen
def drawHelpScreen(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill="white")
    canvas.create_text(data.width / 2, 20, text="Parameters", font="Arial 20")
    canvas.create_text(15, 40, text="Key - A key is a group of pitches that form the tonal basis of a piece of music. A key can be either major, which\ntypically sounds \"Happier\", or minor, which typically sounds \"sad.\"", font="Arial 15", anchor=NW)
    canvas.create_text(15, 80, text="Chord Progression - A chord progression is a series of chords played in a sequence. \nWhether a chord is major or minor significantly contributes to the mood of a piece.", font="Arial 15", anchor=NW)
    canvas.create_text(15, 120, font="Arial 15", anchor=NW, text="Structure - The structure is the order that specific sections of the piece will be played in. \nFor example, the structure 'ABA' will play section A, then section B, then section A will be \nplayed again.")
    canvas.create_text(15, 180, font="Arial 15", anchor=NW, text="Time Signature - The time signature is composed of two numbers. The top number is how \nmany beats will be put in each measure, and the bottom number is which note is \nconsidered a beat. A 4/4 time signature means there will be 4 beats in every measure \nwhere every quarter note is considered a beat.")
    canvas.create_text(15, 260, font="Arial 15", anchor=NW, text="Length - How many unique measures the specific section will consist of.")
    canvas.create_text(15, 290, font="Arial 15", anchor=NW, text="Repetition - How many times you want the unqiue measures to be repeated in a section.")
    canvas.create_text(15, 320, font="Arial 15", anchor=NW, text="Left Hand Pattern - This is the pattern that the notes of a current chord (of the chosen \nchord progression) will be played in the left hand.")
    canvas.create_text(15, 360, font="Arial 15", anchor=NW, text="Note Allocation - The note allocation is how often of each note of different length will occur.\nFor example, selecting 50% for both quarter notes and eighth notes will result in the piece \nbeing composed of roughly 50% quarter notes and 50% eighth notes.")
    canvas.create_text(15, 420, font="Arial 15", anchor=NW, text="Harmony - The harmony of a piece is how often melody notes will be a tone of the chord \nbeing played in the left hand.")
    canvas.create_text(data.width / 2, 480, font="Arial 20", text="Playback Editing")
    canvas.create_text(15, 500, font="Arial 15", anchor=NW, text="Press a note and use the Up and Down arrow keys to edit the pitch of a note. Just click \nanywhere to place it.")
    canvas.create_text(15, 540, font="Arial 15", anchor=NW, text="You can also use the arrow keys to navigate between selected notes.")
    canvas.create_text(15, 570, font="Arial 15", anchor=NW, text="Press 'r' to generate a new melody.")
    canvas.create_text(15, 600, font="Arial 15", anchor=NW, text="Press 'delete' or 'backspace' to replace a note with a rest.")
    canvas.create_text(data.width / 2, 640, font="Arial 20", text="Custom Parameters")
    canvas.create_text(15, 660, font="Arial 15", anchor=NW, text="Structure must contain only A's, B', and C's placed adjacent. Ex: 'ABCCBA'")
    canvas.create_text(15, 680, font="Arial 15", anchor=NW, text="Chord Progression must contain only roman numerals (lowercase or uppercase) with commas AND spaces\nseparating them. Ex: 'IV, V, I, V'")
    canvas.create_text(15, 720, font="Arial 15", anchor=NW, text="Left hand pattern must be in the form [[a, b, c, d . . .], 1 / 8] where the first list contains digits 0-9 where 0 is the root\nof the chord, and 2 would be two notes above the root, and the second element is the length of each note\n(1/8 is an eighth note).")
    canvas.create_text(data.width / 2, 800, font="Arial 20", text="Press 'h' to exit help menu")

def redrawAll(canvas, data):
    if data.generalQuestionsScreen == True:
        drawGeneralQuestionsScreen(canvas, data)
    elif data.melodyScreen == True:
        drawMelodyScreen(canvas, data)
    elif data.melodyPlaybackScreen == True:
        drawMelodyPlaybackScreen(canvas, data)
    elif data.developmentScreen == True:
        drawDevelopmentScreen(canvas, data)
    elif data.developmentPlaybackScreen == True:
        drawDevelopmentPlaybackScreen(canvas, data)
    elif data.sectionCScreen == True:
        drawSectionCScreen(canvas, data)
    elif data.sectionCPlaybackScreen == True:
        drawSectionCPlaybackScreen(canvas, data)
    elif data.fullSongPlaybackScreen == True:
        drawFullSongPlaybackScreen(canvas, data)
    elif data.infoScreen == True:
        drawInfoScreen(canvas, data)
    elif data.completedSongScreen == True:
        drawCompletedSongScreen(canvas, data)
    elif data.save == True:
        saveSheet(canvas, data)
    #help
    if data.help == True:
        drawHelpScreen(canvas, data)
    elif data.help == False and data.melodyPlaybackScreen == False and \
                            data.developmentPlaybackScreen == False and \
                            data.sectionCPlaybackScreen == False and \
                            data.fullSongPlaybackScreen == False and \
                            data.save == False and data.infoScreen == False and\
                            data.completedSongScreen == False:
        canvas.create_text(data.width / 2, data.height - 5, 
                        text="Press 'h' for help", font="Arial 13", anchor=S)
    #draws outline around selected note
    if data.selected != None:
        x = data.selected.x
        y = data.selected.y
        canvas.create_oval(x - 6, y - 4, x + 6, y + 4, outline="red")
    #creates a red line that follows the current note being played
    if (data.playMelody == True or data.playDevelopment == True or\
                        data.playSectionC == True or data.playFullSong == True)\
                                        and data.completedSongScreen == False \
                                        and data.save == False:
        row = data.noteNum // 32
        space = data.height / 4.5
        canvas.create_line(220 + (data.noteNum % 32) * 15, 50 + (row % 4) * \
                                    space, 220 + (data.noteNum % 32) * 15, 
                                    170 + (row % 4) * space, fill="red")

##Run function:
def run(width=800, height=825):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    root.title("Build-A-Melody")
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run()