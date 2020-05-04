package com.github.buildamelody.generation;

import com.github.buildamelody.theory.NoteValue;
import org.jfugue.pattern.Pattern;
import org.jfugue.theory.ChordProgression;
import org.jfugue.theory.Note;
import org.jfugue.theory.TimeSignature;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * A section of the full piece with its own selected generation parameters.
 * These parameters include its own chord progression, note length allocation,
 * degree of harmony, length, and repetition.
 */
public class MusicalSection {
    private final static int DEFAULT_NUM_MEASURES = 4;
    private final static int DEFAULT_REPETITION = 1;
    private final static int DEFAULT_HARMONY = 50;


    private List<InputListener> listeners;

    // number of uniquely generated measures in this section
    private int numMeasures = DEFAULT_NUM_MEASURES;

    // number of times the measures will be chained together
    private int repetition = DEFAULT_REPETITION;

    // probability that each generated note will be harmonized with the chord
    private int harmony = DEFAULT_HARMONY;

    // how many notes of each value/length
    private Map<NoteValue, Integer> noteValueAllocation = new HashMap<>();

    // this section's chord progression
    private ChordProgression chordProgression ;

    // this section's left hand pattern
    private List<Integer> leftHandPatternIntervals;

    private TimeSignature timeSignature;

    private Pattern generatedMusic;

    public MusicalSection(TimeSignature timeSignature) {
        this.timeSignature = timeSignature;
    };

    /**
     * Main method for generating the music
     */
    public void generate() {

    }





}
