package com.github.buildamelody.generation;

import com.github.buildamelody.theory.KeySignature;
import org.jfugue.theory.TimeSignature;

import java.util.HashMap;
import java.util.Map;

public class FullPiece {

    // Time signature of full piece
    private TimeSignature timeSignature;

    // Key signature of full piece
    private KeySignature keySignature;

    // Specifies number and order or musical sections
    private String structure;

    // Tempo of full piece
    private int tempo;

    private Map<String, MusicalSection> generatedMusicalSections = new HashMap<>();








}
