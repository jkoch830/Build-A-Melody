package com.github.buildamelody.generation;

import com.github.buildamelody.theory.Chord;
import com.github.buildamelody.theory.KeySignature;
import com.github.buildamelody.theory.NoteValue;
import org.jfugue.pattern.Pattern;

import org.jfugue.theory.ChordProgression;
import org.jfugue.theory.Note;
import org.jfugue.theory.TimeSignature;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

/**
 * A section of the full piece with its own selected generation parameters.
 * These parameters include its own chord progression, note length allocation,
 * degree of harmony, length, and repetition.
 */
public class MusicalSection {
    private final static int DEFAULT_NUM_MEASURES = 4;
    private final static int DEFAULT_REPETITION = 1;
    private final static int DEFAULT_HARMONY = 50;
    public static final int RANDOM_UPPER_LIMIT = 100;


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
    private List<Chord> chordProgression ;

    // this section's left hand pattern
    private List<Integer> leftHandPatternIntervals;

    // choices of octaves for right hand
    private List<Integer> octaveChoices;

    // determines if first note of every measure is harmonized automatically
    private boolean firstNoteHarmonized;

    private KeySignature keySignature;

    private TimeSignature timeSignature;

    private Pattern generatedMusic;

    /**
     * Constructor for section
     * @param timeSignature The time signature
     */
    public MusicalSection(KeySignature keySignature, TimeSignature timeSignature) {
        this.keySignature = keySignature;
        this.timeSignature = timeSignature;
    }


    /* *********************************************************** */
    /* ******************BEGIN GENERATION METHODS***************** */
    /* *********************************************************** */

    /**
     * Main method for generating the music
     */
    public void generate() {
        List<List<Note>> measures = new ArrayList<>(numMeasures);
        List<NoteValue> noteValueSelection = getNoteValueSelection();
        int progressionCounter = 0;
        while (measures.size() < numMeasures) { // keep generating measures
            List<Note> currMeasure = new ArrayList<>();
            Chord currChord = chordProgression.get(progressionCounter);
            while (!isMeasureFull(currMeasure)) {
                String pitch, value;

                // Generates pitch
                if (firstNoteHarmonized && currMeasure.isEmpty()) { // first note
                    String[] chordNotes = currChord.getChordNotes(keySignature);
                    pitch = chordNotes[new Random().nextInt(Chord.CHORD_LENGTH)];
                } else {
                    pitch = generatePitch(currChord);
                }

                // generates length

            }
        }
    }

    private String generatePitch(Chord currChord) {
        List<String> chordNotes = Arrays.asList(currChord.getChordNotes(keySignature));
        int randomInt = new Random().nextInt(RANDOM_UPPER_LIMIT);
        if (randomInt < harmony) { // harmonized
            return chordNotes.get(new Random().nextInt(Chord.CHORD_LENGTH));
        } else { // selects note that isn't harmonized
            List<String> pitchChoices = new ArrayList<>();
            for (String pitch : keySignature.getScale()) {
                if (!chordNotes.contains(pitch)) { pitchChoices.add(pitch); }
            }
            return pitchChoices.get(new Random().nextInt(pitchChoices.size()));
        }
    }


    private boolean isMeasureFull(List<Note> measure) {
        final double THRESHOLD = .001;
        double totalDuration = 0;
        for (Note note : measure) {
            totalDuration += note.getDuration();
        }
        double expectedDuration = (double)timeSignature.getBeatsPerMeasure() /
                timeSignature.getDurationForBeat();
        return Math.abs(expectedDuration - totalDuration) < THRESHOLD;
    }

    private List<NoteValue> getNoteValueSelection() {
        List<NoteValue> result = new ArrayList<>();
        double ratio = 0;
        for (Map.Entry<NoteValue, Integer> entry : noteValueAllocation.entrySet()) {
            ratio += entry.getKey().getLength() * entry.getValue();
        }
        double totalNotes = numMeasures / ratio;
        for (Map.Entry<NoteValue, Integer> entry : noteValueAllocation.entrySet()) {
            int numOccurrences = (int) (entry.getValue() * totalNotes);
            for (int i = 0; i < numOccurrences; i++) {
                result.add(entry.getKey());
            }
        }
        return result;
    }
    /* *********************************************************** */
    /* *******************END GENERATION METHODS****************** */
    /* *********************************************************** */


    /* *********************************************************** */
    /* *****************BEGIN SET AND GET METHODS***************** */
    /* *********************************************************** */

    public void setNumMeasures(int numMeasures) {
        this.numMeasures = numMeasures;
    }

    public void setChordProgression(List<Chord> chordProgression) {
        this.chordProgression = chordProgression;
    }

    public void setHarmony(int harmony) {
        this.harmony = harmony;
    }

    public void setNoteValueAllocation(Map<NoteValue, Integer> noteValueAllocation) {
        this.noteValueAllocation = noteValueAllocation;
    }

    public void setRepetition(int repetition) {
        this.repetition = repetition;
    }

    public void setLeftHandPatternIntervals(List<Integer> leftHandPatternIntervals) {
        this.leftHandPatternIntervals = leftHandPatternIntervals;
    }

    public void registerListener(InputListener listener) {
        this.listeners.add(listener);
    }

    /* *********************************************************** */
    /* ******************END SET AND GET METHODS****************** */
    /* *********************************************************** */
}
