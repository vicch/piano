\version "2.24.3"
\include "../template.v1.ly"

\header {
  title = \markup \override #'((font-name . "FangSong")(font-size . 6)) "四季の歌"
  tagline = "EveryonePiano 500"
}

\markup \vspace #1.25

chordaseven = { cs8 g8 a4 }
chorddmi    = { d8  f8 a4 }
chorddmii   = { d8  f8 a8 f8 }
chordgm     = { d8  g8 bf4 }

\score {
  \new PianoStaff <<
    \new Staff {
      \tempo 4 = 96
      \clef treble
      \key f \major
      \time 4/4
      
      a'4  a'8  g'8 f'8 g'8 f'8 e'8  | d'4 d'4     d'2     | bf'4 bf'8 a'8 g'8 f'8 g'8 bf'8 | a'1 | \break
      bf'4 bf'8 a'8 g'4     g'8 bf'8 | a'4 a'8 f'8 d'4 d'4 | e'4  a'8  a'8 g'8 f'8 e'8 f'8  | d'1 \bar "|."
    }
    \new Staff {
      \clef bass
      \key f \major
      \time 4/4
      
      \chorddmi \chorddmi | \chorddmii d8 f8 g8 a8 | \chordgm     \chordgm     | \chorddmii d8 e8 f8 a8 |
      \chordgm  \chordgm  | \chorddmi  \chorddmii  | \chordaseven \chordaseven | \chorddmii d2          |
    }
    \chords {
      \set noChordSymbol = ""
      
      d1:m | d1:m | g1:m | d1:m |
      d1:m | d1:m | a1:7 | d1:m |
    }
  >>
  \layout {}
  \midi {}
}
