package com.github.buildamelody.theory;

/**
 * Key signatures
 */
public enum KeySignature {
    C(new String[]{"C", "D", "E", "F", "G", "A", "B"}),
    G(new String[]{"G", "A", "B", "C", "D", "E", "F#"}),
    D(new String[]{"D", "E", "F#", "G", "A", "B", "C#"}),
    A(new String[]{"A", "B", "C#", "D", "E", "F#", "G#"}),
    E(new String[]{"E", "F#", "G#", "A", "B", "C#", "D#"}),
    B(new String[]{"B", "C#", "D#", "E", "F#", "G#", "A#"}),
    F_SHARP(new String[]{"F#", "G#", "A#", "B", "C#", "D#", "E#"}),
    C_SHARP(new String[]{"C#", "D#", "E#", "F#", "G#", "A#", "B#"}),
    F(new String[]{"F", "G", "A", "Bb", "C", "D", "E"}),
    B_FLAT(new String[]{"Bb", "C", "D", "Eb", "F", "G", "A"}),
    E_FLAT(new String[]{"Eb", "F", "G", "Ab", "Bb", "C", "D"}),
    A_FLAT(new String[]{"Ab", "Bb", "C", "Db", "Eb", "F", "G"}),
    D_FLAT(new String[]{"Db", "Eb", "F", "Gb", "Ab", "Bb", "C"}),
    G_FLAT(new String[]{"Gb", "Ab", "Bb", "Cb", "Db", "Eb", "F"}),
    C_FLAT(new String[]{"Cb", "Db", "Eb", "Fb", "Gb", "Ab", "Bb"}),
    a(new String[]{"A", "B", "C", "D", "E", "F", "G"}),
    e(new String[]{"E", "F#", "G", "A", "B", "C", "D"}),
    b(new String[]{"B", "C#", "D", "E", "F#", "G", "A"}),
    f_SHARP(new String[]{"F#", "G#", "A", "B", "C#", "D", "E"}),
    c_SHARP(new String[]{"C#", "D#", "E", "F#", "G#", "A", "B"}),
    g_SHARP(new String[]{"G#", "A#", "B", "C#", "D#", "E", "F#"}),
    d_SHARP(new String[]{"D#", "E#", "F#", "G#", "A#", "B", "C#"}),
    a_SHARP(new String[]{"A#", "B#", "C#", "D#", "E#", "F#", "G#"}),
    d(new String[]{"D", "E", "F", "G", "A", "Bb", "C"}),
    g(new String[]{"G", "A", "Bb", "C", "D", "Eb", "F"}),
    c(new String[]{"C", "D", "Eb", "F", "G", "Ab", "Bb"}),
    f(new String[]{"F", "G", "Ab", "Bb", "C", "Db", "Eb"}),
    b_FLAT(new String[]{"Bb", "C", "Db", "Eb", "F", "Gb", "Ab"}),
    e_FLAT(new String[]{"Eb", "F", "Gb", "Ab", "Bb", "Cb", "Db"}),
    a_FLAT(new String[]{"Ab", "Bb", "Cb", "Db", "Eb", "Fb", "Gb"});
    


    private final String[] scale;

    KeySignature(String[] scale) {
        this.scale = scale;
    }

    /**
     * Retrieves the scale of the key signature
     * @return A string array containing all notes in the scale
     */
    public String[] getScale() {
        return this.scale;
    }

    /**
     * Retrieves a specific note in the key signature's scale
     * @param n The index of the note
     * @return The note at index n in the scale
     */
    public String getNote(int n) {
        return this.scale[n % 7];
    }
}
