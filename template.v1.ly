\language "english"

\paper {
  #(set-paper-size "letter")
  top-margin    = #15
  bottom-margin = #10
  left-margin   = #20
  right-margin  = #20
  system-system-spacing.basic-distance = #12
  system-system-spacing.padding = #2
  print-page-number = ##t
}

\layout {
  \context {
    \Score
    \override StaffGrouper.staff-staff-spacing.basic-distance = #12
    \override StaffGrouper.staff-staff-spacing.padding = #2
    \override TimeSignature.style = #'numbered
    \override ChordName.font-size = #-1
  }
}