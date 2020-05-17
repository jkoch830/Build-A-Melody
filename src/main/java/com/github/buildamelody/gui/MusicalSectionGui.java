package com.github.buildamelody.gui;


import com.github.buildamelody.generation.MusicalSection;
import com.github.buildamelody.theory.Chord;
import com.github.buildamelody.theory.KeySignature;

import javax.swing.BoxLayout;
import javax.swing.ButtonGroup;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JRadioButton;
import javax.swing.JSpinner;
import javax.swing.SpinnerModel;
import javax.swing.SpinnerNumberModel;
import javax.swing.SwingConstants;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.GraphicsEnvironment;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.Insets;
import java.util.ArrayList;
import java.util.List;

/**
 * Panel containing all GUI-related operations with each musical section
 */
public class MusicalSectionGui extends JPanel {
    private static final String[] DEF_MAJOR_PROGRESSIONS = new String[] {
            "I, IV, V", "I, IV, vi, V", "I, IV, I, V", "I, vi, IV, V",
            "I, V, vi, IV", "vi, IV, I, V"
    };
    private static final String[] DEF_MINOR_PROGRESSIONS = new String[] {
            "i, VII, VI, VII", "VI, i, VII, iv", "i, VII, V, VI",
            "i, VI, VII, III", "i, iv, VII, III", "i, VI, III, VII"
    };
    private static final int TWO_CHAR_WIDTH = 40;
    private static final int PADDING = 50;
    private static final Font FONT = new Font(Font.SANS_SERIF, Font.PLAIN, 30);
    private final MusicalSection musicalSection;
    private final char sectionID;

    public MusicalSectionGui(MusicalSection musicalSection, char section) {
        super();
        this.musicalSection = musicalSection;
        this.sectionID = section;
        this.setLayout(new GridBagLayout());
        this.setBackground(Color.ORANGE);
        GridBagConstraints cst = new GridBagConstraints();

        JLabel sectionTitle = new JLabel("Section " + sectionID + " Parameters");
        sectionTitle.setHorizontalAlignment(SwingConstants.CENTER);
        sectionTitle.setFont(new Font("AppleGothic", Font.BOLD, 40));
        cst.gridx = 0;
        cst.gridy = 0;
        cst.weightx = 1;
        cst.fill = GridBagConstraints.HORIZONTAL;
        this.add(sectionTitle, cst);
        cst.gridy++;

        // Length and repetition
        JLabel lengthLabel = new JLabel("Length and Repetition:");
        JLabel progressionLabel = new JLabel("Chord Progression:");
        lengthLabel.setHorizontalAlignment(SwingConstants.CENTER);
        progressionLabel.setHorizontalAlignment(SwingConstants.CENTER);
        lengthLabel.setFont(FONT);
        progressionLabel.setFont(FONT);
        this.add(lengthLabel, cst);
        cst.gridy++;
        this.add(getLengthRepetitionChoices(), cst);
        cst.gridy++;

        // Chord progression
        this.add(progressionLabel, cst);
        cst.gridy++;
        this.add(getChordProgressionPanel(), cst);
    }

    private JPanel getLengthRepetitionChoices() {
        JPanel spinnerPanel = new JPanel();
        spinnerPanel.setLayout(new GridBagLayout());
        GridBagConstraints cst = new GridBagConstraints();
        int currNumMeasures = musicalSection.getNumMeasures();
        int currRepetition = musicalSection.getRepetition();
        JLabel numMeasuresLabel = new JLabel("Total Amount of Measures: "
                + (currNumMeasures * currRepetition));
        SpinnerModel lengthModel = new SpinnerNumberModel(currNumMeasures,
                1, null, 1);
        SpinnerModel repetitionModel = new SpinnerNumberModel(currRepetition,
                1, null, 1);
        JSpinner lengthSpinner = new JSpinner(lengthModel);
        JSpinner repetitionSpinner = new JSpinner(repetitionModel);
        // Should not be able to enter text
        JSpinner.DefaultEditor lengthSpinnerEditor = (JSpinner.DefaultEditor)lengthSpinner.getEditor();
        JSpinner.DefaultEditor repetitionSpinnerEditor = (JSpinner.DefaultEditor)repetitionSpinner.getEditor();
        lengthSpinnerEditor.getTextField().setEditable(false);
        repetitionSpinnerEditor.getTextField().setEditable(false);
        // Make width enough to hold 2 chars
        lengthSpinnerEditor.setPreferredSize(new Dimension(TWO_CHAR_WIDTH, 0));
        repetitionSpinnerEditor.setPreferredSize(new Dimension(TWO_CHAR_WIDTH, 0));
        lengthSpinner.addChangeListener(e -> {
            int numMeasures = (int) lengthSpinner.getValue();
            musicalSection.setNumMeasures(numMeasures);
            int totalNumMeasures = numMeasures * (int) repetitionSpinner.getValue();
            numMeasuresLabel.setText("Total Amount of Measures: " + totalNumMeasures);
            this.revalidate();
            this.repaint();
        });
        repetitionSpinner.addChangeListener(e -> {
            int repetition = (int) repetitionSpinner.getValue();
            musicalSection.setRepetition(repetition);
            int totalNumMeasures = (int) lengthSpinner.getValue() * repetition;
            numMeasuresLabel.setText("Total Amount of Measures: " + totalNumMeasures);
            numMeasuresLabel.revalidate();
            numMeasuresLabel.repaint();
        });
        JLabel lengthLabel = new JLabel("Length:");
        JLabel repetitionLabel = new JLabel("Repetition:");
        cst.gridx = 0; cst.gridy = 0;
        cst.anchor = GridBagConstraints.EAST;
        spinnerPanel.add(lengthLabel, cst);
        cst.gridx++;
        spinnerPanel.add(lengthSpinner, cst);
        cst.gridx--; cst.gridy++;
        spinnerPanel.add(repetitionLabel, cst);
        cst.gridx++;
        spinnerPanel.add(repetitionSpinner, cst);
        cst.gridx++; cst.gridy--;
        cst.gridheight++;
        cst.insets = new Insets(0, PADDING, 0, 0);
        spinnerPanel.add(numMeasuresLabel, cst);
        //spinnerPanel.setMaximumSize(spinnerPanel.getPreferredSize());
        return spinnerPanel;
    }

    private JPanel getChordProgressionPanel() {
        JPanel progressionPanel = new JPanel();
        progressionPanel.setLayout(new GridBagLayout());
        GridBagConstraints cst = new GridBagConstraints();
        cst.gridx = 0;
        cst.gridy = 0;
        String key = musicalSection.getKeySignature().getName();
        String[] progressions;
        if (!key.toLowerCase().equals(key)) { // major
            progressions = DEF_MAJOR_PROGRESSIONS;
        } else {
            progressions = DEF_MINOR_PROGRESSIONS;
        }
        ButtonGroup progressionGroup = new ButtonGroup();
        for (String progression : progressions) { // Default choices
            JRadioButton progressionButton = new JRadioButton(progression);
            progressionButton.addActionListener(e -> {
                List<Chord> chords = new ArrayList<>();
                String noWhitespace = progression.replaceAll("\\s", "");
                for (String numeral : noWhitespace.split(",")) {
                    chords.add(Chord.getChordFromNumeral(numeral));
                }
                musicalSection.setChordProgression(chords);
            });
            progressionGroup.add(progressionButton);
            progressionPanel.add(progressionButton, cst);
            cst.gridx++;
        }
        // Custom Choice

        return progressionPanel;
    }
}
