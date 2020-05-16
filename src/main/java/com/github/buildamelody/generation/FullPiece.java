package com.github.buildamelody.generation;

import com.github.buildamelody.theory.KeySignature;
import org.jfugue.theory.Key;
import org.jfugue.theory.TimeSignature;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Stream;

public class FullPiece {

    private static final String DEF_STRUCTURE = "ABC";
    private static final TimeSignature DEF_TIME_SIGNATURE = new TimeSignature(4, 4);
    private static final KeySignature DEF_KEY_SIGNATURE = KeySignature.C;
    private static final int DEF_TEMPO = 90;

    // Time signature of full piece
    private TimeSignature timeSignature;

    // Key signature of full piece
    private KeySignature keySignature;

    // Specifies number and order or musical sections
    private String structure;

    // Tempo of full piece
    private int tempo;

    private final Map<Character, MusicalSection> generatedMusicalSections;

    // The GUI listener
    private InputListener inputListener;

    public FullPiece() {
        timeSignature = DEF_TIME_SIGNATURE;
        keySignature = DEF_KEY_SIGNATURE;
        structure = DEF_STRUCTURE;
        tempo = DEF_TEMPO;
        generatedMusicalSections = new HashMap<>();
        for (char section : structure.toCharArray()) {
            generatedMusicalSections.put(section,
                    new MusicalSection(keySignature, timeSignature));
        }
    }


    /* *********************************************************** */
    /* *****************BEGIN SET AND GET METHODS***************** */
    /* *********************************************************** */

    public TimeSignature getTimeSignature() {
        return timeSignature;
    }

    public KeySignature getKeySignature() {
        return keySignature;
    }

    public String getStructure() {
        return structure;
    }

    public int getTempo() {
        return tempo;
    }

    /**
     * Sets the key signature of the full piece. Changing this will erase all
     * generated sections
     * @param keySignature The new key signature
     */
    public void setKeySignature(KeySignature keySignature) {
        this.keySignature = keySignature;
        generatedMusicalSections.replaceAll((s, v) ->
                new MusicalSection(keySignature, timeSignature));
        notifyKeySignatureSet(keySignature);
    }

    /**
     * Sets the time signature of the full piece. Changing this will erase all
     * generated sections
     * @param timeSignature The new time signature
     */
    public void setTimeSignature(TimeSignature timeSignature) {
        this.timeSignature = timeSignature;
        generatedMusicalSections.replaceAll((s, v) ->
                new MusicalSection(keySignature, timeSignature));
        notifyTimeSignatureSet(timeSignature);
    }

    /**
     * Sets the structure of the full piece. Changing this will erase sections
     * that aren't present in the new structure.
     * @param structure The new structure
     */
    public void setStructure(String structure) {
        // Removes sections that aren't present in new structure
        Set<Character> sections = new HashSet<>();
        for (char section : structure.toCharArray()) { sections.add(section); }
        generatedMusicalSections.entrySet().removeIf(entry -> !sections.contains(entry.getKey()));

        // Adds new sections
        for (char section : sections) {
            generatedMusicalSections.putIfAbsent(section,
                    new MusicalSection(keySignature, timeSignature));
        }
        notifyStructureSet(structure);
        System.out.println("Structures et to: " + structure);
    }

    public void setTempo(int tempo) {
        this.tempo = tempo;
        notifyTempoSet(tempo);
    }

    public void setInputListener(InputListener inputListener) {
        this.inputListener = inputListener;
    }

    /* *********************************************************** */
    /* ******************END SET AND GET METHODS****************** */
    /* *********************************************************** */

    /* *********************************************************** */
    /* ********************BEGIN NOTIFY METHODS******************* */
    /* *********************************************************** */

    private void notifyKeySignatureSet(KeySignature keySignature) {
        this.inputListener.onKeySignatureSet(keySignature);
    }

    private void notifyTimeSignatureSet(TimeSignature timeSignature) {
        this.inputListener.onTimeSignatureSet(timeSignature);
    }

    private void notifyStructureSet(String structure) {
        this.inputListener.onStructureSet(structure);
    }

    private void notifyTempoSet(int tempo) {
        this.inputListener.onTempoSet(tempo);
    }

    /* *********************************************************** */
    /* *********************END NOTIFY METHODS******************** */
    /* *********************************************************** */

}
