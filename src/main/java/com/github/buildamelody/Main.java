package com.github.buildamelody;

import com.github.buildamelody.generation.MusicalSection;
import com.github.buildamelody.theory.Chord;
import com.github.buildamelody.theory.KeySignature;
import com.github.buildamelody.theory.NoteValue;
import org.jfugue.theory.TimeSignature;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Main {


    public static void main(String[] args) {
        TimeSignature timeSignature = new TimeSignature(4, 4);
        MusicalSection section = new MusicalSection(KeySignature.c, timeSignature);

        Map<NoteValue, Integer> allocation = new HashMap<>();
        allocation.put(NoteValue.QUARTER, 25);
        allocation.put(NoteValue.HALF, 50);
        allocation.put(NoteValue.EIGHTH, 25);

        List<Chord> progression = new ArrayList<>();
        progression.add(Chord.i);
        progression.add(Chord.vii);
        progression.add(Chord.v);
        progression.add(Chord.vi);

        List<Integer> leftHandPattern = new ArrayList<>(Arrays.asList(
                0, 4, 7, 4, 9, 4, 7, 4
        ));

        section.setNumMeasures(4);
        section.setHarmony(50);
        section.setRepetition(1);
        section.setOctaveChoices(new ArrayList<>(Collections.singletonList(5)));
        section.setNoteValueAllocation(allocation);
        section.setChordProgression(progression);
        section.setFirstNoteHarmonized(true);
        section.setLeftHandPatternIntervals(leftHandPattern);
        section.generate();
        section.play();

    }
}
