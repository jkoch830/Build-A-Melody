package com.github.buildamelody.theory;

import java.util.HashMap;
import java.util.Map;

/**
 * The supported generated note durations
 */
public enum NoteValue {
    WHOLE(1, "w"),
    HALF(.5, "h"),
    QUARTER(.25, "q"),
    TRIPLET_QUARTER(1.0/6, "q*3:2"),
    EIGHTH(.125, "i"),
    TRIPLET_EIGHTH(1.0/12, "i*3:2"),
    SIXTEENTH(.0625, "s");

    private final double length;
    private final String abbreviation;

    // Reverse-lookup map for getting a day from a length
    private static final Map<Double, NoteValue> LOOKUP = new HashMap<>();

    static {
        for (NoteValue value : NoteValue.values()) {
            LOOKUP.put(value.getLength(), value);
        }
    }

    /**
     * @param length The number of beats in a 4/4 time signature
     * @param abbreviation The string notation JFugue uses
     */
    NoteValue(double length, String abbreviation) {
        this.length = length;
        this.abbreviation = abbreviation;
    }

    /**
     * Gets the length associated with the note value
     * @return The length
     */
    public double getLength() {
        return this.length;
    }

    /**
     * Gets the JFugue abbreviation associated with the note value
     * @return The JFugue abbreviation
     */
    public String getAbbreviation() {
        return this.abbreviation;
    }

    /**
     * Gets the note value associated with a particular length
     * @param length The length of the note value being retrieved
     * @returnd The note value
     */
    public static NoteValue getNoteValue(double length) {
        return LOOKUP.get(length);
    }
}
