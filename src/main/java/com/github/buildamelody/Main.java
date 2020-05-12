package com.github.buildamelody;

import com.github.buildamelody.generation.MusicalSection;
import com.github.buildamelody.theory.Chord;
import com.github.buildamelody.theory.KeySignature;
import com.github.buildamelody.theory.NoteValue;
import org.jfugue.pattern.Pattern;
import org.jfugue.player.Player;
import org.jfugue.theory.ChordProgression;
import org.jfugue.theory.Intervals;
import org.jfugue.theory.Key;
import org.jfugue.theory.Note;
import org.jfugue.theory.TimeSignature;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Main {


    public static void main(String[] args) {
        TimeSignature timeSignature = new TimeSignature(4, 4);
        MusicalSection section = new MusicalSection(KeySignature.C, timeSignature);

        Map<NoteValue, Integer> allocation = new HashMap<>();
        allocation.put(NoteValue.QUARTER, 75);
        allocation.put(NoteValue.EIGHTH, 25);

        List<Chord> progression = new ArrayList<>();
        progression.add(Chord.i);
        progression.add(Chord.i);
        progression.add(Chord.i);
        progression.add(Chord.i);

        section.setNumMeasures(4);
        section.setHarmony(100);
        section.setRepetition(1);
        section.setNoteValueAllocation(allocation);
        section.setChordProgression(progression);
        section.generate();

    }
}
