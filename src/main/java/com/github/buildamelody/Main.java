package com.github.buildamelody;

import org.jfugue.pattern.Pattern;
import org.jfugue.player.Player;
import org.jfugue.theory.Chord;
import org.jfugue.theory.ChordProgression;
import org.jfugue.theory.Intervals;
import org.jfugue.theory.Key;
import org.jfugue.theory.Note;
import org.jfugue.theory.TimeSignature;

import java.util.Arrays;
import java.util.List;

public class Main {


    public static void main(String[] args) {
        ChordProgression cp = new ChordProgression("I iv V");
        TimeSignature ts = new TimeSignature(3, 8);
        for (Chord chord : cp.getChords()) {
            for (Note note : chord.getNotes()) {
                System.out.println(note.toStringWithoutDuration());
            }
        }
        Note note = new Note("C5i");
        System.out.println(Arrays.toString(cp.toStringArray()));

    }
}
