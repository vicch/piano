\version "2.24.3"

#(define title      "")
#(define title-font "")
#(define source     "")
#(define total-page 1)

\include "../template/base.ly"

\markup \vspace #1.5

\score {
  \new PianoStaff <<
    \chords {
    }
    \new Staff {
      \tempo 4 = 96
      \clef treble
      \key c \major
      \time 3/4
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 3/4
    }
  >>
  \layout {}
  \midi {}
}
