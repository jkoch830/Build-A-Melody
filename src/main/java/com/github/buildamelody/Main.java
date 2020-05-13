package com.github.buildamelody;

import com.github.buildamelody.generation.MusicalSection;
import com.github.buildamelody.theory.Chord;
import com.github.buildamelody.theory.KeySignature;
import com.github.buildamelody.theory.NoteValue;
import com.google.common.collect.Lists;
import org.jfugue.pattern.Pattern;
import org.jfugue.player.Player;
import org.jfugue.theory.ChordProgression;
import org.jfugue.theory.Intervals;
import org.jfugue.theory.Key;
import org.jfugue.theory.Note;
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
        MusicalSection section = new MusicalSection(KeySignature.C, timeSignature);

        Map<NoteValue, Integer> allocation = new HashMap<>();
        allocation.put(NoteValue.QUARTER, 50);
        allocation.put(NoteValue.EIGHTH, 25);
        allocation.put(NoteValue.TRIPLET_QUARTER, 25);

        List<Chord> progression = new ArrayList<>();
        progression.add(Chord.i);
        progression.add(Chord.iv);
        progression.add(Chord.v);
        progression.add(Chord.i);

        section.setNumMeasures(4);
        section.setHarmony(25);
        section.setRepetition(1);
        section.setOctaveChoices(new ArrayList<>(Collections.singletonList(5)));
        section.setNoteValueAllocation(allocation);
        section.setChordProgression(progression);
        section.setFirstNoteHarmonized(true);
        section.generate();

    }
}
