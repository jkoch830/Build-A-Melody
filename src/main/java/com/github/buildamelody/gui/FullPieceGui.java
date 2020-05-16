package com.github.buildamelody.gui;

import com.github.buildamelody.generation.FullPiece;
import com.github.buildamelody.generation.InputListener;
import com.github.buildamelody.generation.MusicalSection;
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
import javax.swing.SwingConstants;
import javax.swing.event.DocumentEvent;
import javax.swing.event.DocumentListener;
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.GridLayout;
import java.util.Map;

public class FullPieceGui implements InputListener {
    private static final String TITLE = "Build-a-Melody";

    private static final int DEF_WIDTH = 900;
    private static final int DEF_HEIGHT = 850;
    private static final int NUM_MAJOR = 15;
    private static final int NUM_MINOR = 15;
    private static final TimeSignature[] DEF_TIME_SIGNATURE_CHOICES = new TimeSignature[] {
            new TimeSignature(2, 2),
            new TimeSignature(4, 4),
            new TimeSignature(3, 4),
            new TimeSignature(2, 4),
            new TimeSignature(3, 8),
            new TimeSignature(6, 8),
            new TimeSignature(9, 8),
            new TimeSignature(12, 8),
    };
    private static final String[] DEF_STRUCTURE_CHOICES = new String[] {
            "ABC",
            "ABCBA",
            "ABBA"
    };

    // The parent window
    private final JFrame frame;

    // The pane that will contain tabs corresponding to musical sections
    private final StructureTabbedPane structureTabbedPane;

    private FullPiece fullPiece;

    public FullPieceGui(FullPiece fullPiece) {
        this.fullPiece = fullPiece;
        this.fullPiece.setInputListener(this);

        frame = new JFrame(TITLE);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setPreferredSize(new Dimension(DEF_WIDTH, DEF_HEIGHT));

        // Initializes tabbed panel
        structureTabbedPane = new StructureTabbedPane(fullPiece.getStructure());

        frame.add(structureTabbedPane, BorderLayout.CENTER);
        frame.pack();
        frame.setVisible(true);
    }

    @Override
    public void onTimeSignatureSet(TimeSignature timeSignature) {
        structureTabbedPane.setNewStructure(fullPiece.getStructure());
    }

    @Override
    public void onKeySignatureSet(KeySignature keySignature) {
        structureTabbedPane.setNewStructure(fullPiece.getStructure());
    }

    @Override
    public void onStructureSet(String structure) {
        structureTabbedPane.setNewStructure(structure);
    }

    @Override
    public void onTempoSet(int tempo) {

    }

    /**
     * JPanel that contains all the main parameters for the full piece:
     * Key signature, time signature, structure, and tempo
     */
    private class MainParameters extends JPanel {
        JTextField customStructureField = new JTextField("ABCDE");

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
            Dimension labelPadding = new Dimension(0, 5);
            Dimension parameterPadding = new Dimension(0, 50);

            // Key signature
            this.add(keySigLabel);
            this.add(Box.createRigidArea(labelPadding));
            this.add(getKeySignatureChoices());
            this.add(Box.createRigidArea(parameterPadding));

            // Time signature
            this.add(timeSigLabel);
            this.add(Box.createRigidArea(labelPadding));
            this.add(getTimeSignatureChoices());
            this.add(Box.createRigidArea(parameterPadding));

            // Structure
            this.add(structureLabel);
            this.add(Box.createRigidArea(labelPadding));
            this.add(getStructureChoices());
            this.add(Box.createRigidArea(parameterPadding));

            // Tempo
            this.add(tempoLabel);
            this.add(Box.createRigidArea(labelPadding));
            this.add(getTempoSlider());
            this.add(Box.createRigidArea(parameterPadding));
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
                if (i == 0) { majorKey.setSelected(true); }
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
                JPanel timeSigLabelPanel = new JPanel(new BorderLayout());
                JLabel beatsLabel = new JLabel(String.valueOf(timeSignature.getBeatsPerMeasure()));
                JLabel durationLabel = new JLabel(String.valueOf(timeSignature.getDurationForBeat()));
                beatsLabel.setHorizontalAlignment(SwingConstants.CENTER);
                durationLabel.setHorizontalAlignment(SwingConstants.CENTER);
                timeSigLabelPanel.add(beatsLabel, BorderLayout.NORTH);
                timeSigLabelPanel.add(durationLabel, BorderLayout.SOUTH);
                timeSigButton.addActionListener(e ->
                        fullPiece.setTimeSignature(timeSignature));
                timeSignatureGroup.add(timeSigButton);
                timeSignatureContainer.add(timeSigButton);
                timeSignatureContainer.add(timeSigLabelPanel);
                timeSignatureContainer.add(Box.createRigidArea(new Dimension(10,0)));
            }
            JRadioButton defaultChoice = (JRadioButton) timeSignatureContainer.getComponents()[0];
            defaultChoice.setSelected(true);
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
            int preferredHeight = customStructureField.getPreferredSize().height;
            customStructureField.setPreferredSize(new Dimension(100, preferredHeight));
            JRadioButton customButton = new JRadioButton();
            customButton.addActionListener(e ->
                    fullPiece.setStructure(customStructureField.getText())
            );
            customStructureField.getDocument().addDocumentListener(new DocumentListener() {
                @Override
                public void insertUpdate(DocumentEvent e) {
                    if (customButton.isSelected()) {
                        fullPiece.setStructure(customStructureField.getText());
                    }
                }
                @Override
                public void removeUpdate(DocumentEvent e) {
                    // If empty, structure is set to first choice
                    if (customStructureField.getText().equals("")) {
                        JRadioButton defaultChoice = (JRadioButton) structureContainer.getComponents()[0];
                        defaultChoice.setSelected(true);
                        fullPiece.setStructure(DEF_STRUCTURE_CHOICES[0]);
                    }
                    else if (customButton.isSelected()) {
                        fullPiece.setStructure(customStructureField.getText());
                    }
                }
                @Override
                public void changedUpdate(DocumentEvent e) {
                    throw new IllegalStateException();
                }
            });
            structureGroup.add(customButton);
            structureContainer.add(customButton);
            structureContainer.add(customStructureField);
            JRadioButton defaultChoice = (JRadioButton) structureContainer.getComponents()[0];
            defaultChoice.setSelected(true);
            structureContainer.setMaximumSize(structureContainer.getPreferredSize());
            return structureContainer;
        }

        private JSlider getTempoSlider() {
            JSlider slider = new JSlider(40, 200);
            slider.addChangeListener(e ->
                    fullPiece.setTempo(slider.getValue()));
            slider.setMajorTickSpacing(20);
            slider.setPaintLabels(true);
            slider.setPaintTicks(true);
            return slider;
        }
    }

    /**
     * Tabbed pane that is modified according to the set structure
     */
    private class StructureTabbedPane extends JTabbedPane {
        private String structure;

        StructureTabbedPane(String structure) {
            super();
            this.structure = structure;
            this.add("Main Parameters", new MainParameters());
            setNewStructure(structure);
        }

        void setNewStructure(String newStructure) {
            int numTabs = this.getTabCount();
            // Removes all tabs except for 'Main Parameters'
            for (int i = numTabs - 1; i >= 1; i--) {
                this.removeTabAt(i);
            }
            for (Map.Entry<Character, MusicalSection> entry :
                    fullPiece.getGeneratedMusicalSections().entrySet()) {
                char sectionID = entry.getKey();
                MusicalSection musicalSection = entry.getValue();
                this.add("Section " + sectionID,
                        new MusicalSectionGui(musicalSection, sectionID));
            }
            this.structure = newStructure;
        }
    }
}
