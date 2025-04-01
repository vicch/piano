\language "english"

#(define-markup-command (total-page layout props) ()
   (interpret-markup layout props 
     (number->string (ly:output-def-lookup layout 'total-page))))

#(set-global-staff-size 20)

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
  
  % indent = #0
  
  print-page-number = ##t
  
  oddHeaderMarkup = \markup \null
  evenHeaderMarkup = \oddHeaderMarkup
  
  oddFooterMarkup = \markup {
    \fill-line {
      % \fromproperty #'header:tagline
      \null
      \null
      \concat {
        \fromproperty #'page:page-number-string
        "/"
        \total-page
      }
    }
  }
  evenFooterMarkup = \oddFooterMarkup
}

\layout {
  \context {
    \Score
    % barNumberVisibility = #all-bar-numbers-visible
    barNumberVisibility = #first-bar-number-invisible-save-broken-bars
    
    \override StaffGrouper.staff-staff-spacing.basic-distance = #11
    \override StaffGrouper.staff-staff-spacing.padding = #2
    
    \override Stem.length-fraction = #1.1
    \override Stem.thickness = #1.6
    \override Beam.damping = #2.0
    
    \override TimeSignature.style = #'numbered
    \override TimeSignature.break-visibility = #end-of-line-invisible
    
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
