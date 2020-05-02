package com.github.buildamelody.generation;

/**
 * The supported generated note durations
 */
public enum NoteValue {
    WHOLE(4, "w"),
    HALF(2, "h"),
    QUARTER(1, "q"),
    EIGHTH(.5, "i"),
    SIXTEENTH(.25, "s"),
    TRIPLET_QUARTER(2.0/3, "q*3:2"),
    TRIPLET_EIGHTH(1.0/3, "i*3:2");

    private final double length;
    private final String abbreviation;

    /**
     * @param length The number of beats in a 4/4 time signature
     * @param abbreviation The string notation JFugue uses
     */
    NoteValue(double length, String abbreviation) {
        this.length = length;
        this.abbreviation = abbreviation;
    }

    public double getLength() {
        return this.length;
    }

    public String getAbbreviation() {
        return this.abbreviation;
    }
}
