package com.github.buildamelody.theory;

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
