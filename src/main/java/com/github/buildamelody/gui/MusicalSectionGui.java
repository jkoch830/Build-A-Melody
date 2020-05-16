package com.github.buildamelody.gui;


import com.github.buildamelody.generation.MusicalSection;

import javax.swing.BoxLayout;
import javax.swing.JLabel;
import javax.swing.JPanel;
import java.awt.BorderLayout;

/**
 * Panel containing all GUI-related operations with each musical section
 */
public class MusicalSectionGui extends JPanel {
    private final MusicalSection musicalSection;
    private final char sectionID;

    public MusicalSectionGui(MusicalSection musicalSection, char section) {
        super();
        this.musicalSection = musicalSection;
        this.sectionID = section;
        this.setLayout(new BoxLayout(this, BoxLayout.PAGE_AXIS));

        JLabel sectionTitle = new JLabel("Section " + sectionID);
        this.add(sectionTitle);

    }
}
