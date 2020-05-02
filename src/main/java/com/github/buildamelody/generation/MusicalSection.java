package com.github.buildamelody.generation;

import org.jfugue.theory.ChordProgression;

import java.util.Map;

/**
 * A section of the full piece with its own selected generation parameters.
 * These parameters include its own chord progression, note length allocation,
 * degree of harmony, length, and repetition.
 */
public class MusicalSection {

    // number of uniquely generated measures in this section
    private int numMeasures;

    // number of times the measures will be chained together
    private int repetition;

    // probability that each generated note will be harmonized with the chord
    private int harmony;

    // how many notes of each value/length
    private Map<NoteValue, Integer> noteValueAllocation;

    // this section's chord progression
    private ChordProgression chordProgression;

}
