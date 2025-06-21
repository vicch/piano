\version "2.24.3"
\include "../settings.v1.ly"

\header {
  title = \markup \override #'((font-name . "FangSong")(font-size . 6)) "Title"
  tagline = "Sequence"
  transcriber = "Transcribed by vicch"
}

\paper {
  total-page = 1
  scoreTitleMarkup = \markup \fill-line {
    \null { \fromproperty #'header:transcriber }
  }
}

\markup \vspace #1.5

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
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
