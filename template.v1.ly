\language "english"

\paper {
  #(set-paper-size "letter")
  top-margin    = #15
  bottom-margin = #10
  left-margin   = #20
  right-margin  = #20
  
  system-system-spacing.basic-distance = #14
  system-system-spacing.padding = #2
  
  indent = #0
  
  print-page-number = ##t
}

\layout {
  \context {
    \Score
    barNumberVisibility = #all-bar-numbers-visible
    
    \override StaffGrouper.staff-staff-spacing.basic-distance = #11
    \override StaffGrouper.staff-staff-spacing.padding = #2
    
    \override Stem.length-fraction = #1.1
    
    \override TimeSignature.style = #'numbered
    
    \override ChordName.font-size = #-1
  }
}