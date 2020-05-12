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
        System.out.println(noteValueSelection);
        while (measures.size() < numMeasures) { // keep generating measures
            List<Note> currMeasure = new ArrayList<>();
            Chord currChord = chordProgression.get(progressionCounter);
            while (!isMeasureFull(currMeasure)) {
                String pitch = generatePitch(currChord, currMeasure.isEmpty());

                // Note length
                NoteValue noteValue = noteValueSelection.get(
                        new Random().nextInt(noteValueSelection.size()));
                double numBeats = noteValue.getLength() * timeSignature.getDurationForBeat();
                if (numBeats < 1) {
                    int groupSize = 1 / numBeats;
                    for (int i = 0; i < )
                }
            }
        }
    }

    private String generatePitch(Chord currChord, boolean firstNote) {
        List<String> chordNotes = Arrays.asList(currChord.getChordNotes(keySignature));
        int randomInt = new Random().nextInt(RANDOM_UPPER_LIMIT);
        if ((firstNote && firstNoteHarmonized) || randomInt < harmony) { // harmonized
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
        List<NoteValue> selection = new ArrayList<>();
        double weightedSum = 0;
        for (Map.Entry<NoteValue, Integer> entry : noteValueAllocation.entrySet()) {
            double noteValueLength = entry.getKey().getLength();
            int weight = entry.getValue();
            weightedSum += noteValueLength * weight * timeSignature.getDurationForBeat();
        }
        int totalBeats = timeSignature.getBeatsPerMeasure() * numMeasures;
        double totalNotes = (totalBeats / weightedSum) * 100;
        System.out.println(totalNotes);
        for (Map.Entry<NoteValue, Integer> entry : noteValueAllocation.entrySet()) {
            long numOccurrences = Math.round((entry.getValue() / 100.0) * totalNotes);
            for (long i = 0; i < numOccurrences; i++) {
                selection.add(entry.getKey());
            }
        }
        return refineNoteValueSelection(selection);
    }

    private List<NoteValue> refineNoteValueSelection(List<NoteValue> selection) {
        int size = selection.size();
        for (int i = size - 1; i >= 0; i--) {
            NoteValue value = selection.get(i);
            double numBeats = value.getLength() * timeSignature.getDurationForBeat();
            if (numBeats < 1) {
                while (getFrequency(selection, value) % (1 / numBeats) != 0) {
                    selection.add(value);
                }
            }
        }
        return selection;
    }

    private static int getFrequency(List<NoteValue> selection, NoteValue query) {
        int count = 0;
        for (NoteValue value : selection) {
            if (value == query) { count++; }
        }
        return count;
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
