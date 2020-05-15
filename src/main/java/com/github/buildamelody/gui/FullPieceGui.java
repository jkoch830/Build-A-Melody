package com.github.buildamelody.gui;

import com.github.buildamelody.generation.FullPiece;
import com.github.buildamelody.generation.InputListener;
import com.github.buildamelody.theory.KeySignature;
import org.jfugue.theory.TimeSignature;

import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.JTabbedPane;
import javax.swing.JTextField;
import javax.swing.border.Border;
import java.awt.BorderLayout;
import java.awt.Dimension;

public class FullPieceGui implements InputListener {
    private static final String TITLE = "Build-a-Melody";

    private static final int DEF_WIDTH = 700;
    private static final int DEF_HEIGHT = 850;

    // The parent window
    private final JFrame frame;

    // The pane that will contain tabs corresponding to musical sections
    private final JTabbedPane tabbedPane;

    private FullPiece fullPiece;

    public FullPieceGui(FullPiece fullPiece) {
        this.fullPiece = fullPiece;
        this.fullPiece.setInputListener(this);

        frame = new JFrame(TITLE);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setPreferredSize(new Dimension(DEF_WIDTH, DEF_HEIGHT));

        // Initializes tabbed panel to only contain a main parameters tab
        tabbedPane = new JTabbedPane();
        tabbedPane.add("Main Parameters", new MainParameters());

        frame.add(tabbedPane, BorderLayout.CENTER);
        frame.pack();
        frame.setVisible(true);

    }

    @Override
    public void onTimeSignatureSet(TimeSignature timeSignature) {

    }

    @Override
    public void onKeySignatureSet(KeySignature keySignature) {

    }

    @Override
    public void onStructureSet(String structure) {

    }

    @Override
    public void onTempoSet(int tempo) {

    }

    /**
     * JPanel that contains all the main parameters for the full piece:
     * Key signature, time signature, structure, and tempo
     */
    private class MainParameters extends JPanel {
        MainParameters() {
            super();
            this.add(new JTextField("HELLO"), BorderLayout.CENTER);
        }
    }
}
