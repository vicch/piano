\version "2.24.3"
\include "../settings.v1.ly"

\header {
  title = \markup \override #'((font-name . "FangSong")(font-size . 6)) "Title"
  tagline = "Sequence"
}

\paper {
  total-page = 1
}

\markup \vspace #1.5

\score {
  \new PianoStaff <<
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
    \chords {
    }
  >>
  \layout {}
  \midi {}
}
