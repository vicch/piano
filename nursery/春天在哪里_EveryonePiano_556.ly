\version "2.24.3"
\include "../settings.v1.ly"

\header {
  title = \markup \override #'((font-name . "FangSong")(font-size . 6)) "春天在哪里"
  tagline = "EveryonePiano 556"
}

\paper {
  total-page = 2
}

\markup \vspace #1.5

Ci    = { e8 <<g8  c'8>> c8          <<g8  c'8>> }
Cii   = { c8 <<g8  c'8>> e8          <<g8  c'8>> }
DmSix = { f8 <<bf8 d'8>> <<bf8 d'8>> <<bf8 d'8>> }
Fi    = { f8 <<a8  c'8>> <<a8  c'8>> <<a8  c'8>> }
Fii   = { f8 <<a8  c'8>> c8          <<a8  c'8>> }

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 120
      \clef treble
      \key f \major
      \time 2/4
      
      a''8  a''8  a''8  f''8  | c''4        c''4      | a''8 a''8 a''8 f''8 | a''4      r4 | \break
      c'''8 c'''8 a''8  f''8  | c''8  c''8  c''4      | d''8 e''8 f''8 a''8 | g''4      r4 | \break
      a''8  a''8  a''8  f''8  | c''4        c''4      | a''8 a''8 a''8 f''8 | a''4      r4 | \break
      c'''8 d'''8 c'''8 d'''8 | c'''8 bf''8 a''8 f''8 | c''4      a''4      | g''8 f''8 r4 | \break
    }
    \new Staff {
      \clef bass
      \key f \major
      \time 2/4
      
      \Fi | \Fii | \Fi    | \Fii                |
      \Fi | \Fii | \DmSix | \Ci                 |
      \Fi | \Fii | \Fi    | \Fii                |
      \Fi | \Fii | \Cii   | f8 <<a8 c'8>> g8 a8 |
    }
    \chords {
      
      f2 | f2 | f2    | f2 |
      f2 | f2 | d2:m6 | c2 |
      f2 | f2 | f2    | f2 |
      f2 | f2 | c2    | r2 |
    }
  >>
  \layout {}
  \midi {}
}
