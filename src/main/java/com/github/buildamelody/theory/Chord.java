package com.github.buildamelody.theory;

public enum Chord {

    i(0, 2, 4),
    ii(1, 3, 5),
    iii(2, 4, 6),
    iv(3, 5, 7),
    v(4, 6, 8),
    vi(5, 7, 9),
    vii(6, 8, 10);

    public static final int CHORD_LENGTH = 3;

    private final int rootOffset;
    private final int thirdOffset;
    private final int fifthOffset;


    Chord(int root, int third, int fifth) {
        this.rootOffset = root;
        this.thirdOffset = third;
        this.fifthOffset = fifth;
    }

    /**
     * Retrieves the offset of the root of the chord
     * @return The offset of the root of the chord
     */
    public int getRootOffset() {
        return rootOffset;
    }

    /**
     * Retrieves an array containing all notes in the chord
     * @param keySignature The key signature the notes abide by
     * @return The array containing the notes of the chord
     */
    public String[] getChordNotes(KeySignature keySignature) {
        String[] chordNotes = new String[CHORD_LENGTH];
        String[] scale = keySignature.getScale();
        chordNotes[0] = scale[rootOffset % 7];
        chordNotes[1] = scale[thirdOffset % 7];
        chordNotes[2] = scale[fifthOffset % 7];
        return chordNotes;
    }

    public static Chord getChordFromNumeral(String numeral) {
        switch(numeral) {
            case "I":
            case "i":
                return i;
            case "II":
            case "ii":
                return ii;
            case "III":
            case "iii":
                return iii;
            case "IV":
            case "iv":
                return iv;
            case "V":
            case "v":
                return v;
            case "VI":
            case "vi":
                return vi;
            case "VII":
            case "vii":
                return vii;
            default:
                throw new IllegalArgumentException("Illegal numeral: " + numeral);
        }
    }
}
