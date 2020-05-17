package com.github.buildamelody.generation;

import com.github.buildamelody.theory.Chord;
import com.github.buildamelody.theory.KeySignature;
import com.github.buildamelody.theory.NoteValue;
import org.jfugue.pattern.Pattern;

import org.jfugue.player.Player;
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
    private final static int DEFAULT_LEFT_BASE_OCTAVE = 3;
    private final static int SCALE_LENGTH = 7;
    private final static int RANDOM_UPPER_LIMIT = 100;


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
    private List<Integer> leftHandIntervals;

    // choices of octaves for right hand
    private List<Integer> octaveChoices;

    // determines if first note of every measure is harmonized automatically
    private boolean firstNoteHarmonized;

    private KeySignature keySignature;

    private TimeSignature timeSignature;

    private List<List<Note>> rightHandMeasures = new ArrayList<>();

    private List<List<Note>> leftHandMeasures = new ArrayList<>();

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
        generateRightHand();
        generateLeftHand();
    }

    private void generateRightHand() {
        List<List<Note>> measures = new ArrayList<>(numMeasures);
        List<NoteValue> noteValueSelection = getNoteValueSelection();
        int progressionCounter = 0;
        System.out.println(noteValueSelection);
        while (measures.size() < numMeasures) { // keep generating measures
            List<Note> currMeasure = new ArrayList<>();
            Chord currChord = chordProgression.get(progressionCounter % chordProgression.size());
            while (!isMeasureFull(currMeasure)) { // fills measure
                // Checks if a note value exists to fill the measure
                if (!selectionCanFillMeasure(currMeasure, noteValueSelection)) {
                    addRequiredNoteValues(currMeasure, noteValueSelection);
                }

                // Note length
                NoteValue noteValue = noteValueSelection.get(
                        new Random().nextInt(noteValueSelection.size()));
                double numBeats = noteValue.getLength() * timeSignature.getDurationForBeat();
                int groupSize = getGroupSize(noteValue);
                if (groupSize * numBeats > availableBeats(currMeasure)) { continue; }
                for (int i = 0; i < groupSize; i++) { // generates notes in groups
                    String pitch = generatePitch(currChord, currMeasure.isEmpty());
                    String octave = String.valueOf(octaveChoices.get(new Random().nextInt(octaveChoices.size())));
                    Note note = new Note(pitch + octave + noteValue.getAbbreviation());
                    currMeasure.add(note);
                    noteValueSelection.remove(noteValue);
                }
            }
            measures.add(currMeasure);
            progressionCounter++;
        }

        // copies generated measures specified by the repetition
        rightHandMeasures.clear();
        for (int i = 0; i < repetition; i++) {
            rightHandMeasures.addAll(measures);
        }
    }

    private void generateLeftHand() {
        Map<String, Integer> octaveOffsets = new HashMap<>() {{
            put("C", 0);
            put("D", 1);
            put("E", 2);
            put("F", 3);
            put("G", 4);
            put("A", 5);
            put("B", 6);
        }};

        double numNotes = leftHandIntervals.size();
        double numBeatsPerNote = timeSignature.getBeatsPerMeasure() / numNotes;
        double noteLength = numBeatsPerNote / timeSignature.getDurationForBeat();
        NoteValue noteValue = NoteValue.getNoteValue(noteLength);

        List<List<Note>> measures = new ArrayList<>();

        leftHandMeasures.clear();
        for (int i = 0; i < numMeasures; i++) {
            Chord chord = chordProgression.get(i % chordProgression.size());
            List<Note> currMeasure = new ArrayList<>();
            int rootOffset = chord.getRootOffset();  // offset of root in scale
            String rootPitch = chord.getChordNotes(keySignature)[0].substring(0, 1);
            for (int interval : leftHandIntervals) {
                String pitch = keySignature.getNote(rootOffset + interval);
                int octave = DEFAULT_LEFT_BASE_OCTAVE +
                        (octaveOffsets.get(rootPitch) + interval) / SCALE_LENGTH;
                currMeasure.add(new Note(pitch + octave + noteValue.getAbbreviation()));
            }
            measures.add(currMeasure);
        }

        // copies generated measures specified by the repetition
        leftHandMeasures.clear();
        for (int i = 0; i < repetition; i++) {
            leftHandMeasures.addAll(measures);
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

    /**
     * Checks if a measure is full based on the time signature and notes it
     * contains.
     * @param measure The measure
     * @return True if the measure is full, false otherwise
     */
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

    /**
     * Retrieves the available number of beats in a measure
     * @param measure The measure
     * @return The number of beats available
     */
    private int availableBeats(List<Note> measure) {
        double totalDuration = 0;
        for (Note note : measure) {
            totalDuration += note.getDuration() * timeSignature.getDurationForBeat();
        }
        assert(totalDuration % 1 == 0);
        return timeSignature.getBeatsPerMeasure() - (int) totalDuration;
    }

    /**
     * Checks if a measure can be filled with a given note value selection
     * @param measure The measure
     * @param selection The selection of note values
     * @return True if the measure can be filled, false if no note value can
     *         fill the measure
     */
    private boolean selectionCanFillMeasure(List<Note> measure,
                                            List<NoteValue> selection) {
        int numAvailableBeats = availableBeats(measure);
        for (NoteValue value : selection) {
            if (value.getLength() * timeSignature.getDurationForBeat() <= numAvailableBeats) {
                return true;
            }
        }
        return false;
    }

    /**
     * Adds note values to the selection such that filling the measure is possible
     * @param measure The measure
     * @param selection The current selection of note values
     */
    private void addRequiredNoteValues(List<Note> measure,
                                       List<NoteValue> selection) {
        int numAvailableBeats = availableBeats(measure);
        for (NoteValue noteValue : NoteValue.values()) {
            // checks if user wants any number of these note values
            if (noteValueAllocation.containsKey(noteValue)) {
                double noteValueBeats = noteValue.getLength() * timeSignature.getDurationForBeat();
                while (noteValueBeats <= numAvailableBeats) {
                    selection.add(noteValue);
                    numAvailableBeats -= noteValueBeats;
                }
            }
        }
        assert (numAvailableBeats == 0);
    }
    /**
     * Gets a list of note values based on the inputted note value allocation
     * @return The list of note values
     */
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
        for (Map.Entry<NoteValue, Integer> entry : noteValueAllocation.entrySet()) {
            long numOccurrences = Math.round((entry.getValue() / 100.0) * totalNotes);
            for (long i = 0; i < numOccurrences; i++) {
                selection.add(entry.getKey());
            }
        }
        return refineNoteValueSelection(selection);
    }

    /**
     * Refines a note value selection by ensuring all note values that have
     * duration less than 1 beat are added in groups such that the sum of the
     * note values is a whole number, and ensures that enough notes are in the
     * selection to fill all measures
     * @param selection The initial selection before being refined
     * @return The refined selection
     */
    private List<NoteValue> refineNoteValueSelection(List<NoteValue> selection) {
        int size = selection.size();
        // add's values who falls under 1 beat in groups
        for (int i = size - 1; i >= 0; i--) {
            NoteValue value = selection.get(i);
            double numBeats = value.getLength() * timeSignature.getDurationForBeat();
            if (numBeats < 1) {
                int groupSize = getGroupSize(value);
                while (getFrequency(selection, value) % groupSize != 0) {
                    selection.add(value);
                }
            }
        }

        // adds more notes to ensure there's enough beats
        int totalNumBeats = getNoteValueSelectionBeats(selection);
        int numBeatsRequired = timeSignature.getBeatsPerMeasure() * numMeasures - totalNumBeats;
        for (NoteValue noteValue : NoteValue.values()) {
            if (!noteValueAllocation.containsKey(noteValue)) { continue; }
            double numBeats = noteValue.getLength() * timeSignature.getDurationForBeat();
            while (numBeats <= numBeatsRequired && numBeatsRequired > 0) {
                selection.add(noteValue);
                numBeatsRequired -= numBeats;
            }
            if (numBeatsRequired == 0) { break; }
        }
        return selection;
    }

    /**
     * Calculates the number of beats a note value selection totals to
     * @param selection The selection of note values
     * @return The number of beats
     */
    private int getNoteValueSelectionBeats(List<NoteValue> selection) {
        double totalNumBeats = 0;
        for (NoteValue value : selection) {
            totalNumBeats += value.getLength() * timeSignature.getDurationForBeat();
        }
        assert(totalNumBeats % 1 == 0);
        return (int) totalNumBeats;
    }

    /**
     * Calculates the group size of a note value in the time signature's context
     * A group size of a note value is the number of note values (of the same
     * type) needed such that the total number of beats is divisible by 1
     * @param value The note value
     * @return The number of note values such that the total sum of beats is
     *         divisible by 1
     */
    private int getGroupSize(NoteValue value) {
        double beats = value.getLength() * timeSignature.getDurationForBeat();
        double total = beats;
        int count = 1;
        while (total % 1 != 0 ) {
            total += beats;
            count++;
        }
        return count;

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


    Pattern getRightHandPattern() {
        Pattern rightHand = new Pattern();
        for (List<Note> measure : rightHandMeasures) {
            for (Note note : measure) {
                rightHand.add(note);
            }
        }
        return rightHand;
    }

    Pattern getLeftHandPattern() {
        Pattern leftHand = new Pattern();
        for (List<Note> measure : leftHandMeasures) {
            for (Note note : measure) {
                leftHand.add(note);
            }
        }
        return leftHand;
    }

    /**
     * Plays the generated music
     */
    public void play() {
        Pattern rightHand = getRightHandPattern().setVoice(1).setInstrument(1);
        Pattern leftHand = getLeftHandPattern().setVoice(0).setInstrument(1);
        Player player = new Player();
        player.delayPlay(2000, rightHand, leftHand);
    }

    /* *********************************************************** */
    /* *****************BEGIN SET AND GET METHODS***************** */
    /* *********************************************************** */

    public void setNumMeasures(int numMeasures) {
        this.numMeasures = numMeasures;
    }

    public void setChordProgression(List<Chord> chordProgression) {
        this.chordProgression = chordProgression;
        System.out.println("New progression: " + chordProgression);
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

    public void setLeftHandIntervals(List<Integer> leftHandIntervals) {
        this.leftHandIntervals = leftHandIntervals;
    }

    public void setOctaveChoices(List<Integer> octaveChoices) {
        this.octaveChoices = octaveChoices;
    }

    public void setFirstNoteHarmonized(boolean harmonized) {
        this.firstNoteHarmonized = harmonized;
    }

    public void registerListener(InputListener listener) {
        this.listeners.add(listener);
    }

    public KeySignature getKeySignature() {
        return this.keySignature;
    }

    public int getNumMeasures() {
        return this.numMeasures;
    }

    public int getRepetition() {
        return this.repetition;
    }

    /* *********************************************************** */
    /* ******************END SET AND GET METHODS****************** */
    /* *********************************************************** */
}
