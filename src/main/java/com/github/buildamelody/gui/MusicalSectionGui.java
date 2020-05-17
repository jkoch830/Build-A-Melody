package com.github.buildamelody.gui;


import com.github.buildamelody.generation.MusicalSection;

import javax.swing.BoxLayout;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JSpinner;
import javax.swing.SpinnerModel;
import javax.swing.SpinnerNumberModel;
import javax.swing.SwingConstants;
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Font;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.GridLayout;

/**
 * Panel containing all GUI-related operations with each musical section
 */
public class MusicalSectionGui extends JPanel {
    private static final int[] DEF_LENGTH_CHOICES = new int[] {4, 5, 6, 7, 8};
    private static final int[] DEF_REPETITION_CHOICES = new int[] {1, 2, 3, 4};
    private static final int INITIAL_LENGTH = 4;
    private static final int INITIAL_REPETITION = 1;
    private final MusicalSection musicalSection;
    private final char sectionID;

    public MusicalSectionGui(MusicalSection musicalSection, char section) {
        super();
        this.musicalSection = musicalSection;
        this.sectionID = section;
        this.setLayout(new BoxLayout(this, BoxLayout.PAGE_AXIS));
        this.setBackground(Color.ORANGE);

        Font font = new Font(Font.SANS_SERIF, Font.PLAIN, 30);
        JLabel sectionTitle = new JLabel("Section " + sectionID + " Parameters");
        sectionTitle.setAlignmentX(CENTER_ALIGNMENT);
        sectionTitle.setFont(new Font(Font.SANS_SERIF, Font.PLAIN, 40));
        this.add(sectionTitle);
        this.add(getLengthRepetitionChoices());
    }

    private JPanel getLengthRepetitionChoices() {
        JPanel spinnerPanel = new JPanel();
        spinnerPanel.setLayout(new GridBagLayout());
        GridBagConstraints cst = new GridBagConstraints();
        JLabel numMeasuresLabel = new JLabel("Total Amount of Measures: " + INITIAL_LENGTH);
        SpinnerModel lengthModel = new SpinnerNumberModel(INITIAL_LENGTH,
                1, null, 1);
        SpinnerModel repetitionModel = new SpinnerNumberModel(INITIAL_REPETITION,
                1, null, 1);
        JSpinner lengthSpinner = new JSpinner(lengthModel);
        JSpinner repetitionSpinner = new JSpinner(repetitionModel);
        ((JSpinner.DefaultEditor)lengthSpinner.getEditor()).getTextField().setEditable(false);
        ((JSpinner.DefaultEditor)repetitionSpinner.getEditor()).getTextField().setEditable(false);
        lengthSpinner.addChangeListener(e -> {
            int numMeasures = (int) lengthSpinner.getValue() * (int) repetitionSpinner.getValue();
            numMeasuresLabel.setText("Total Amount of Measures: " + numMeasures);
            numMeasuresLabel.revalidate();
            numMeasuresLabel.repaint();
        });
        repetitionSpinner.addChangeListener(e -> {
            int numMeasures = (int) lengthSpinner.getValue() * (int) repetitionSpinner.getValue();
            numMeasuresLabel.setText("Total Amount of Measures: " + numMeasures);
            numMeasuresLabel.revalidate();
            numMeasuresLabel.repaint();
        });
        JLabel lengthLabel = new JLabel("Length:");
        JLabel repetitionLabel = new JLabel("Repetition:");
        cst.gridx = 0;
        cst.gridy = 0;
        cst.anchor = GridBagConstraints.EAST;
        System.out.println("Length label: Gridx: " + cst.gridx + ", Gridy: " + cst.gridy);
        spinnerPanel.add(lengthLabel, cst);
        cst.gridx++;
        System.out.println("Length Spinner: Gridx: " + cst.gridx + ", Gridy: " + cst.gridy);
        spinnerPanel.add(lengthSpinner, cst);
        cst.gridx--;
        cst.gridy++;
        System.out.println("Reptitiona Label: Gridx: " + cst.gridx + ", Gridy: " + cst.gridy);
        spinnerPanel.add(repetitionLabel, cst);
        cst.gridx++;
        System.out.println("Reptitiona Spinner: Gridx: " + cst.gridx + ", Gridy: " + cst.gridy);
        spinnerPanel.add(repetitionSpinner, cst);
        cst.gridx++;
        cst.gridy--;
        cst.gridheight++;
        spinnerPanel.add(numMeasuresLabel, cst);
        //spinnerPanel.setMaximumSize(spinnerPanel.getPreferredSize());
        return spinnerPanel;
    }
}
