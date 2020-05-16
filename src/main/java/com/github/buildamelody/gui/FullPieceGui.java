package com.github.buildamelody.gui;

import com.github.buildamelody.generation.FullPiece;
import com.github.buildamelody.generation.InputListener;
import com.github.buildamelody.theory.KeySignature;
import org.jfugue.theory.TimeSignature;

import javax.swing.Box;
import javax.swing.BoxLayout;
import javax.swing.ButtonGroup;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JRadioButton;
import javax.swing.JSlider;
import javax.swing.JTabbedPane;
import javax.swing.JTextField;
import javax.swing.border.Border;
import javax.swing.event.DocumentEvent;
import javax.swing.event.DocumentListener;
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.GridLayout;
import java.util.Hashtable;

public class FullPieceGui implements InputListener {
    private static final String TITLE = "Build-a-Melody";

    private static final int DEF_WIDTH = 900;
    private static final int DEF_HEIGHT = 850;
    private static final int NUM_MAJOR = 15;
    private static final int NUM_MINOR = 15;
    private static final TimeSignature[] DEF_TIME_SIGNATURE_CHOICES = new TimeSignature[] {
            new TimeSignature(4, 4),
            new TimeSignature(3, 4),
            new TimeSignature(2, 4),
            new TimeSignature(3, 8),
            new TimeSignature(6, 8),
    };
    private static final String[] DEF_STRUCTURE_CHOICES = new String[] {
            "ABC",
            "ABCBA",
            "ABBA"
    };

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
            this.setLayout(new BoxLayout(this, BoxLayout.PAGE_AXIS));
            this.setBackground(new Color(154, 205, 217));
            JLabel keySigLabel = new JLabel("Key Signature:");
            JLabel timeSigLabel = new JLabel("Time Signature:");
            JLabel structureLabel = new JLabel("Structure:");
            JLabel tempoLabel = new JLabel("Tempo:");
            keySigLabel.setAlignmentX(CENTER_ALIGNMENT);
            timeSigLabel.setAlignmentX(CENTER_ALIGNMENT);
            structureLabel.setAlignmentX(CENTER_ALIGNMENT);
            tempoLabel.setAlignmentX(CENTER_ALIGNMENT);
            Font font = new Font(Font.SANS_SERIF, Font.PLAIN, 30);
            keySigLabel.setFont(font);
            timeSigLabel.setFont(font);
            structureLabel.setFont(font);
            tempoLabel.setFont(font);
            this.add(keySigLabel);
            this.add(Box.createRigidArea(new Dimension(0,5)));
            this.add(getKeySignatureChoices());
            this.add(Box.createRigidArea(new Dimension(0,50)));

            this.add(timeSigLabel);
            this.add(Box.createRigidArea(new Dimension(0,5)));
            this.add(getTimeSignatureChoices());
            this.add(Box.createRigidArea(new Dimension(0,50)));

            this.add(structureLabel);
            this.add(Box.createRigidArea(new Dimension(0,5)));
            this.add(getStructureChoices());
            this.add(Box.createRigidArea(new Dimension(0,50)));

            this.add(tempoLabel);
            this.add(Box.createRigidArea(new Dimension(0,5)));
            this.add(getTempoSlider());
            this.add(Box.createRigidArea(new Dimension(0,50)));
            //displayTempo();
        }

        private JPanel getKeySignatureChoices() {
            JPanel keySignatureContainer = new JPanel();
            keySignatureContainer.setLayout(new GridLayout(2, NUM_MAJOR + 1));
            ButtonGroup keyGroup = new ButtonGroup();
            KeySignature[] keys = KeySignature.values();
            keySignatureContainer.add(new JLabel("Major: "));
            for (int i = 0; i < NUM_MAJOR; i++) { // major keys
                KeySignature currentKey = keys[i];
                JRadioButton majorKey = new JRadioButton(currentKey.getName());
                majorKey.addActionListener(e ->
                        fullPiece.setKeySignature(currentKey));
                keyGroup.add(majorKey);
                keySignatureContainer.add(majorKey);
            }
            keySignatureContainer.add(new JLabel("Minor: "));
            for (int i = NUM_MAJOR; i < NUM_MAJOR + NUM_MINOR; i++) { // minor keys
                KeySignature currentKey = keys[i];
                JRadioButton minorKey = new JRadioButton(currentKey.getName());
                minorKey.addActionListener(e ->
                        fullPiece.setKeySignature(currentKey));
                keyGroup.add(minorKey);
                keySignatureContainer.add(minorKey);
            }
            keySignatureContainer.setMaximumSize(keySignatureContainer.getPreferredSize());
            return keySignatureContainer;
        }

        private JPanel getTimeSignatureChoices() {
            JPanel timeSignatureContainer = new JPanel();
            timeSignatureContainer.setLayout(new BoxLayout(timeSignatureContainer,
                    BoxLayout.LINE_AXIS));
            ButtonGroup timeSignatureGroup = new ButtonGroup();
            // Default choices
            for (TimeSignature timeSignature : DEF_TIME_SIGNATURE_CHOICES) {
                JRadioButton timeSigButton = new JRadioButton();
                JPanel timeSigLabelPanel = new JPanel(new GridLayout(2,1));
                timeSigLabelPanel.add(new JLabel(String.valueOf(timeSignature.getBeatsPerMeasure())));
                timeSigLabelPanel.add(new JLabel(String.valueOf(timeSignature.getDurationForBeat())));
                timeSigButton.addActionListener(e ->
                        fullPiece.setTimeSignature(timeSignature));
                timeSignatureGroup.add(timeSigButton);
                timeSignatureContainer.add(timeSigButton);
                timeSignatureContainer.add(timeSigLabelPanel);
                timeSignatureContainer.add(Box.createRigidArea(new Dimension(10,0)));
            }

            timeSignatureContainer.setMaximumSize(timeSignatureContainer.getPreferredSize());
            return timeSignatureContainer;
        }

        private JPanel getStructureChoices() {
            JPanel structureContainer = new JPanel();
            structureContainer.setLayout(new BoxLayout(structureContainer,
                    BoxLayout.LINE_AXIS));
            ButtonGroup structureGroup = new ButtonGroup();
            // Default choices
            for (String structure : DEF_STRUCTURE_CHOICES) {
                JRadioButton structureButton = new JRadioButton(structure);
                structureButton.addActionListener(e ->
                    fullPiece.setStructure(structure)
                );
                structureGroup.add(structureButton);
                structureContainer.add(structureButton);
            }
            // Custom choice
            JTextField customField = new JTextField("Custom");
            int preferredHeight = customField.getPreferredSize().height;
            customField.setPreferredSize(new Dimension(100, preferredHeight));
            customField.getDocument().addDocumentListener(new DocumentListener() {
                @Override
                public void insertUpdate(DocumentEvent e) {
                    fullPiece.setStructure(customField.getText());
                }
                @Override
                public void removeUpdate(DocumentEvent e) {
                    fullPiece.setStructure(customField.getText());
                }
                @Override
                public void changedUpdate(DocumentEvent e) {
                    fullPiece.setStructure(customField.getText());
                }
            });
            JRadioButton customButton = new JRadioButton();
            customButton.addActionListener(e ->
                    fullPiece.setStructure(customField.getText())
            );
            structureGroup.add(customButton);
            structureContainer.add(customButton);
            structureContainer.add(customField);
            structureContainer.setMaximumSize(structureContainer.getPreferredSize());
            return structureContainer;
        }

        private JSlider getTempoSlider() {
            JSlider slider = new JSlider(20, 200);
            slider.addChangeListener(e ->
                    fullPiece.setTempo(slider.getValue()));
            Hashtable<Integer, JLabel> labels = new Hashtable<>();
            labels.put(20, new JLabel("20"));
            labels.put(200, new JLabel("200"));
            slider.setLabelTable(labels);
            slider.setPaintLabels(true);
            return slider;
        }
    }
}
