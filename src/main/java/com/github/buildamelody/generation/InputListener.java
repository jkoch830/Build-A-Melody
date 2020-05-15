package com.github.buildamelody.generation;

import com.github.buildamelody.theory.KeySignature;
import org.jfugue.theory.TimeSignature;

/**
 * An observer interface which listens to new inputs from the user. The
 * {@link FullPiece} should call these methods to notify the GUI when to update
 * its display.
 */
public interface InputListener {

    /**
     * Called when a new time signature is selected.
     * This should clear all generated musical sections.
     * @param timeSignature The new time signature
     */
    void onTimeSignatureSet(TimeSignature timeSignature);

    /**
     * Called when a new key signature is selected.
     * This should clear all generated musical sections.
     * @param keySignature The new key signature
     */
    void onKeySignatureSet(KeySignature keySignature);

    /**
     * Called when a new structure is selected.
     * @param structure The new structure
     */
    void onStructureSet(String structure);

    /**
     * Called when a new tempo is selected.
     * @param tempo The new tempo
     */
    void onTempoSet(int tempo);

}
