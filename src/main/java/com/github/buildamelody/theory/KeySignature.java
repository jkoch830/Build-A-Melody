package com.github.buildamelody.theory;

/**
 * Key signatures
 */
public enum KeySignature {
    C(new String[]{"C", "D", "E", "F", "G", "A", "B"}, "C"),
    G(new String[]{"G", "A", "B", "C", "D", "E", "F#"}, "G"),
    D(new String[]{"D", "E", "F#", "G", "A", "B", "C#"}, "D"),
    A(new String[]{"A", "B", "C#", "D", "E", "F#", "G#"}, "A"),
    E(new String[]{"E", "F#", "G#", "A", "B", "C#", "D#"}, "E"),
    B(new String[]{"B", "C#", "D#", "E", "F#", "G#", "A#"}, "B"),
    F_SHARP(new String[]{"F#", "G#", "A#", "B", "C#", "D#", "E#"}, "F#"),
    C_SHARP(new String[]{"C#", "D#", "E#", "F#", "G#", "A#", "B#"}, "C#"),
    F(new String[]{"F", "G", "A", "Bb", "C", "D", "E"}, "F"),
    B_FLAT(new String[]{"Bb", "C", "D", "Eb", "F", "G", "A"}, "Bb"),
    E_FLAT(new String[]{"Eb", "F", "G", "Ab", "Bb", "C", "D"}, "Eb"),
    A_FLAT(new String[]{"Ab", "Bb", "C", "Db", "Eb", "F", "G"}, "Ab"),
    D_FLAT(new String[]{"Db", "Eb", "F", "Gb", "Ab", "Bb", "C"}, "Db"),
    G_FLAT(new String[]{"Gb", "Ab", "Bb", "Cb", "Db", "Eb", "F"}, "Gb"),
    C_FLAT(new String[]{"Cb", "Db", "Eb", "Fb", "Gb", "Ab", "Bb"}, "Cb"),
    a(new String[]{"A", "B", "C", "D", "E", "F", "G"}, "a"),
    e(new String[]{"E", "F#", "G", "A", "B", "C", "D"}, "e"),
    b(new String[]{"B", "C#", "D", "E", "F#", "G", "A"}, "b"),
    f_SHARP(new String[]{"F#", "G#", "A", "B", "C#", "D", "E"}, "f#"),
    c_SHARP(new String[]{"C#", "D#", "E", "F#", "G#", "A", "B"}, "c#"),
    g_SHARP(new String[]{"G#", "A#", "B", "C#", "D#", "E", "F#"}, "g#"),
    d_SHARP(new String[]{"D#", "E#", "F#", "G#", "A#", "B", "C#"}, "d#"),
    a_SHARP(new String[]{"A#", "B#", "C#", "D#", "E#", "F#", "G#"}, "a#"),
    d(new String[]{"D", "E", "F", "G", "A", "Bb", "C"}, "d"),
    g(new String[]{"G", "A", "Bb", "C", "D", "Eb", "F"}, "g"),
    c(new String[]{"C", "D", "Eb", "F", "G", "Ab", "Bb"}, "c"),
    f(new String[]{"F", "G", "Ab", "Bb", "C", "Db", "Eb"}, "f"),
    b_FLAT(new String[]{"Bb", "C", "Db", "Eb", "F", "Gb", "Ab"}, "bb"),
    e_FLAT(new String[]{"Eb", "F", "Gb", "Ab", "Bb", "Cb", "Db"}, "eb"),
    a_FLAT(new String[]{"Ab", "Bb", "Cb", "Db", "Eb", "Fb", "Gb"}, "ab");
    


    private final String[] scale;
    private final String name;

    KeySignature(String[] scale, String name) {
        this.scale = scale;
        this.name = name;
    }

    /**
     * Retrieves the scale of the key signature
     * @return A string array containing all notes in the scale
     */
    public String[] getScale() {
        return this.scale;
    }

    /**
     * Retrieves the name of the key signature
     * @return The name of the key signature
     */
    public String getName() {
        return this.name;
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
