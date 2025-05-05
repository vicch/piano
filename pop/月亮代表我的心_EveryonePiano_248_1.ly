\version "2.24.3"
\include "../settings.v1.ly"

\header {
  title = \markup \override #'((font-name . "FangSong")(font-size . 6)) "月亮代表我的心"
  tagline = "EveryonePiano 248"
}

\paper {
  total-page = 1
}

\markup \vspace #1.5

CI  = { c8  g8  c'8 e'8 g'2  }
EmI = { e,8 b,8 e8  g8  b2   }
FI  = { f8  c'8 f'8 a'8 c''2 }
FII = { f,8 c8  f8  a8  c'2  }
GI  = { g,8 d8  g8  b8  d'2  }
AmI = { a,8 e8  a8  c'8 e'2  }

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 84
      \clef treble
      \key c \major
      \time 4/4
      
      g''2~ g''8 e''8 d''8 c''8 | e''2 r8 a'8 c''8 e''8 | a''2~ a''8 f''8 d''8 c''8 | \break
      
      b'2.  r8   g'8  | c''4. e''8 g''4. c''8 | b'4. e''8 g''4. g''8 | a''4. b''8 c'''4 a''4 | \break
      g''2. e''8 d''8 |
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 4/4
      
      \CI | \AmI | \FI |
      
      \GI | \CI | \EmI | \FII |
      \GI |
    }
    \chords {
      
      c1 | a1:m | f1 |
      
      g1 | c1 | e1:m | f1 |
      g1 |
    }
  >>
  \layout {}
  \midi {}
}
