\version "2.24.3"
\include "../settings.v1.ly"

\header {
  title = \markup \override #'((font-name . "FangSong")(font-size . 6)) "送别"
  tagline = "EveryonePiano 519"
}

\paper {
  total-page = 1
}

\markup \vspace #1.5

Ci  = { c8  g8 c'8 g8 }
Cii = { e8  g8 c'8 g8 }
Fi  = { f8  a8 c'8 a8 }
Gi  = { d8  g8 b8  g8 }
Gii = { d'8 g8 b8  g8 }

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 96
      \clef treble
      \key c \major
      \time 4/4
      
      g''4 e''8 g''8 c'''2       | a''4 c'''4 g''2 | g''4 c''8 d''8 e''4 d''8 c''8 | d''1 | \break
      g''4 e''8 g''8 c'''4. b''8 | a''4 c'''4 g''2 | g''4 d''8 e''8 f''4.     b'8  | c''1 | \break
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 4/4
      
      \Ci \Cii | \Fi \Cii | \Ci \Cii | \Gi \Gii        |
      \Ci \Cii | \Fi \Cii | \Gi \Gii | \Ci c8 d8 e8 g8 |
    }
    \chords {
      
      c2 c2 | f2 c2 | c2 c2 | g2 g2 |
      c2 c2 | f2 c2 | g2 g2 | c2 r2 |
    }
  >>
  \layout {}
  \midi {}
}
