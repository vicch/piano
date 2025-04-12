\version "2.24.3"
\include "../settings.v1.ly"

\header {
  title = \markup \override #'((font-size . 6)) "The Blue Danube"
  tagline = "EveryonePiano 1681"
}

\paper {
  total-page = 2
}

\markup \vspace #1.5

Ci     = { c4  <<e4 g4>>  <<e4 g4>>  }
Cii    = { e4  <<g4 c'4>> <<g4 c'4>> }
F      = { f4  <<a4 c'4>> <<a4 c'4>> }
Gfive  = { d4  <<f4 g4>>  <<f4 g4>>  }
Gseven = { b,4 <<f4 g4>>  <<f4 g4>>  }

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 120
      \clef treble
      \key c \major
      \time 3/4
      
      c'4  e'4  g'4 | g'4  r4 <<e''4 g''4>> | <<e''4 g''4>> r4 <<c''4 e''4>> | <<c''4 e''4>> r4 c'4 | \break
      c'4  e'4  g'4 | g'4  r4 <<f''4 g''4>> | <<f''4 g''4>> r4 <<d''4 f''4>> | <<d''4 f''4>> r4 b4  | \break
      b4   d'4  a'4 | a'4  r4 <<f''4 a''4>> | <<f''4 a''4>> r4 <<d''4 f''4>> | <<d''4 f''4>> r4 b4  | \break
      b4   d'4  a'4 | a'4  r4 <<f''4 a''4>> | <<e''4 a''4>> r4 <<c''4 e''4>> | <<c''4 e''4>> r4 c'4 | \break
      c'4  e'4  g'4 | c''4 r4 <<g'4  c''4>> | <<g'4  c''4>> r4 <<e'4  g'4>>  | <<e'4  g'4>>  r4 c'4 | \break
      c'4  e'4  g'4 | c''4 r4 <<a'4  c''4>> | <<a'4  c''4>> r4 <<f'4  a'4>>  | <<f'4  a'4>>  r4 d'4 | \break
      d'4  f'4  a'4 | a'2.~                 |   a'4         fs'4 g'4         | e''2.~               | \break
      e''4 c''4 e'4 | e'2            d'4    |   a'2              g'4         | c'4. c'8         c'4 | \bar "|."
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 3/4
      
      r2.      | \Ci       | \Ci        | \Ci                  |
      \Ci      | \Gfive    | \Gfive     | \Gseven              |
      \Gseven  | \Gfive    | \Gfive     | \Gseven              |
      \Ci      | \Ci       | \Ci        | \Ci                  |
      \Ci      | \Cii      | \Cii       | e4 <<g4 c'4>> r4     |
      \Ci      | \F        | \F         | f4 <<a4 c'4>> r4     |
      d4 f4 a4 | \Gfive    | \Gfive     | \Ci                  |
      \Ci      | <c f a>2. | <b, d g>2. | <c e g>4 r4 <c e g>4 |
    }
    \chords {
      
      r2.   | c2.   | c2.   | c2.      |
      c2.   | g2.:5 | g2.:5 | g2.:7    |
      g2.:7 | g2.:5 | g2.:5 | g2.:7    |
      c2.   | c2.   | c2.   | c2.      |
      c2.   | c2.   | c2.   | c2    r4 |
      c2.   | f2.   | f2.   | f2    r4 |
      d2.:m | g2.:5 | g2.:5 | c2.      |
      c2.   | f2.   | g2.   | c4 r4 c4 |
    }
  >>
  \layout {}
}

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 120
      \clef treble
      \key c \major
      \time 3/4
      
      c'4  e'4  g'4 | g'4  r4 <<e''4 g''4>> | <<e''4 g''4>> r4 <<c''4 e''4>> | <<c''4 e''4>> r4 c'4 | \break
      c'4  e'4  g'4 | g'4  r4 <<f''4 g''4>> | <<f''4 g''4>> r4 <<d''4 f''4>> | <<d''4 f''4>> r4 b4  | \break
      b4   d'4  a'4 | a'4  r4 <<f''4 a''4>> | <<f''4 a''4>> r4 <<d''4 f''4>> | <<d''4 f''4>> r4 b4  | \break
      b4   d'4  a'4 | a'4  r4 <<f''4 a''4>> | <<e''4 a''4>> r4 <<c''4 e''4>> | <<c''4 e''4>> r4 c'4 | \break
      c'4  e'4  g'4 | c''4 r4 <<g'4  c''4>> | <<g'4  c''4>> r4 <<e'4  g'4>>  | <<e'4  g'4>>  r4 c'4 | \break
      c'4  e'4  g'4 | c''4 r4 <<a'4  c''4>> | <<a'4  c''4>> r4 <<f'4  a'4>>  | <<f'4  a'4>>  r4 d'4 | \break
      d'4  f'4  a'4 | a'2.~                     a'4         fs'4 g'4         | e''2.~                 \break
      e''4 c''4 e'4 | e'2            d'4    |   a'2              g'4         | c'4. c'8         c'4 | \bar "|."
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 3/4
      
      r2.      | \Ci       | \Ci        | \Ci                  |
      \Ci      | \Gfive    | \Gfive     | \Gseven              |
      \Gseven  | \Gfive    | \Gfive     | \Gseven              |
      \Ci      | \Ci       | \Ci        | \Ci                  |
      \Ci      | \Cii      | \Cii       | e4 <<g4 c'4>> r4     |
      \Ci      | \F        | \F         | f4 <<a4 c'4>> r4     |
      d4 f4 a4 | \Gfive    | \Gfive     | \Ci                  |
      \Ci      | <c f a>2. | <b, d g>2. | <c e g>4 r4 <c e g>4 |
    }
  >>
  \midi {}
}
