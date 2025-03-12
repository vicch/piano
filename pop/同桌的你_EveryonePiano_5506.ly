\version "2.24.3"
\include "../settings.v1.ly"

\header {
  title = \markup \override #'((font-name . "FangSong")(font-size . 6)) "同桌的你"
  tagline = "EveryonePiano 5506"
}

\paper {
  total-page = 2
}

\markup \vspace #1.5

C  = { c8  g8 c'8 e'8 c'8 g8 }
Dm = { d8  a8 d'8 f'8 d'8 a8 }
F  = { f,8 c8 f8  a8  f8  c8 }
G  = { g,8 d8 g8  b8  g8  d8 }
Am = { a,8 e8 a8  c'8 a8  e8 }

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 85
      \clef treble
      \key c \major
      \time 6/8
      
      \repeat volta 2 {
        g''8 g''8 g''8 g''8 e''8 f''8 | g''4. b''4. | a''8 a''8 a''8 a''8 f''8 a''8 | g''2. | \break
        g''8 g''8 g''8 g''8 b''8 a''8 | g''4. f''4. | f''8 f''8 f''8 f''8 e''8 d''8 | c''2. | \break
      }
      
      c'''8 c'''8 c'''8 c'''8 g''8 a''8  | c'''4 c'''8 e'''4. | d'''8 d'''8 d'''8 d'''8 c'''8 b''8 | a''2.  | \break
      b''8  b''8  b''8  b''8  b''8 c'''8 | d'''4.      g''4.  | b''8  b''8  c'''8 d'''8 c'''8 b''8 | c'''2. | \break
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 6/8
      
      \C | \C  | \F | \G |
      \C | \Dm | \G | \C |
      
      \Am | \Am | \F | \F |
      \G  | \G  | \G | \C |
    }
    \chords {
      
      c2. | c2.   | f2. | g2. |
      c2. | d2.:m | g2. | c2. |
      
      a2.:m | a2.:m | f2. | f2. |
    }
  >>
  \layout {}
  \midi {}
}
