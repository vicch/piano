\version "2.24.3"
\language "english"

\paper {
  #(set-paper-size "letter")
  top-margin    = #18
  bottom-margin = #12
  left-margin   = #24
  right-margin  = #24
  system-system-spacing.basic-distance = #12
  system-system-spacing.padding = #6
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

\header {
  title = \markup \override #'((font-name . "FangSong")(font-size . 7)) "祝你生日快乐"
  tagline = "495"
}

\markup \vspace #1.5

chordC    = { c4 <<g4 c'4>> <<g4 c'4>> }
chordCsus = { c4 <<g4 bf4>> <<g4 bf4>> }
chordEdim = { e4 <<g4 bf4>> <<g4 bf4>> }
chordF    = { f4 <<a4 c'4>> <<a4 c'4>> }
chordAs   = { d4 <<f4 bf4>> <<f4 bf4>> }

\score {
  \new PianoStaff <<
    \new Staff {
      \tempo 4 = 120
      \clef treble
      \key f \major
      \time 3/4
      
      \partial 4 c''8 c''8 | d''4  c''4 f''4 | e''2      c''8  c''8  | d''4 c''4 g''4 | \break
      f''2       c''8 c''8 | c'''4 a''4 f''4 | e''4 d''4 bf''8 bf''8 | a''4 f''4 g''4 | f''2. \bar "|."
    }
    \new Staff {
      \clef bass
      \key f \major
      \time 3/4
      
      \partial 4 r4 | \chordF | \chordC  | \chordEdim | \break
      \chordF       | \chordF | \chordAs | \chordCsus | <f a c'>2.\arpeggio \bar "|."
    }
    \chords {
      ""4  f2. c2. e2.:dim \break
      f2. f2. as2. c2.:sus f2.
    }
  >>
  \layout {}
  \midi {}
}