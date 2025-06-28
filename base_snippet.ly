\language "english"

#(set-global-staff-size 20)

\paper {
  #(set-paper-size "letter")

  top-margin    = #15
  bottom-margin = #15
  left-margin   = #15
  right-margin  = #15
  
  system-system-spacing.basic-distance = #14
  system-system-spacing.padding = #2
  
  last-bottom-spacing.basic-distance = #14
  last-bottom-spacing.padding = #2
  
  % indent = #0
}

\layout {
  \context {
    \Score
    % barNumberVisibility = #all-bar-numbers-visible
    barNumberVisibility = #first-bar-number-invisible-save-broken-bars
    
    \override StaffGrouper.staff-staff-spacing.basic-distance = #11
    \override StaffGrouper.staff-staff-spacing.padding = #2
    
    \override Stem.length-fraction = #1
    \override Stem.thickness = #1.5
    \override Beam.damping = #1.2
    
    \override TimeSignature.style = #'numbered
    \override TimeSignature.break-visibility = #end-of-line-invisible
    
    \override ChordName.font-size = #-2
    \override SectionLabel.font-size = #-2
  }
}

\layout {
  \context {
    \Staff
    ottavationMarkups = #ottavation-ordinals
  }
}
