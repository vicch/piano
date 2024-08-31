\language "english"

\paper {
  #(set-paper-size "letter")
  top-margin    = #15
  bottom-margin = #15
  left-margin   = #20
  right-margin  = #20
  
  system-system-spacing.basic-distance = #14
  system-system-spacing.padding = #2
  
  last-bottom-spacing.basic-distance = #14
  last-bottom-spacing.padding = #2
  
  indent = #0
  
  print-page-number = ##t
  
  oddHeaderMarkup = \markup \null
  evenHeaderMarkup = \markup \null
  
  oddFooterMarkup = \markup {
    \fill-line {
      \fromproperty #'header:tagline
      \null
      \fromproperty #'page:page-number-string
    }
  }
  evenFooterMarkup = \markup {
    \fill-line {
      \fromproperty #'header:tagline
      \null
      \fromproperty #'page:page-number-string
    }
  }
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

\layout {
  \context {
    \Staff
    ottavationMarkups = #ottavation-ordinals
  }
}

\layout {
  \context {
    \ChordNames
    noChordSymbol = #""
  }
}
