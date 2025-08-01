\language "english"

#(define (title-font-override)
   (let ((base `((font-size . 6))))
     (if (or (not title-font) (string=? title-font ""))
         base ; fallback to default font if title-font is #f or ""
         (cons (cons 'font-name title-font) base))))

#(define total-page-markup (markup (number->string total-page)))

#(set-global-staff-size 20)

\header {
  title = \markup \override #(title-font-override) #title
  tagline = #sequence
}

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
  
  scoreTitleMarkup = \markup \fill-line {
    \null "Engraved by vicch"
  }

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
        #total-page-markup
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
    
    \override StaffGrouper.staff-staff-spacing.basic-distance = #10
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
    explicitKeySignatureVisibility = #end-of-line-invisible
  }
}

\layout {
  \context {
    \ChordNames
    noChordSymbol = #""
  }
}

\midi {
  \context {
    \ChordNames
    \remove "Note_performer"
  }
}

A = \sectionLabel \markup { \box "A" }
B = \sectionLabel \markup { \box "B" }
C = \sectionLabel \markup { \box "C" }
D = \sectionLabel \markup { \box "D" }
E = \sectionLabel \markup { \box "E" }

VAR = _\markup { "*" }
