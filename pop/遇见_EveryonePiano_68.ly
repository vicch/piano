\version "2.24.3"
\include "../settings.v1.ly"

\header {
  title = \markup \override #'((font-name . "FangSong")(font-size . 6)) "遇见"
  tagline = "EveryonePiano 68"
}

\paper {
  total-page = 1
  ragged-last = ##t
}

\markup \vspace #1.5

Ci  = { c8  g8  c'4 }
D   = { d8  a8  d'4 }
Gi  = { g,8 d8  g4  }
Gii = { g8  d'8 g'4 }
Fi  = { f,8 c8  f4  }
Fii = { f8  c'8 f'4 }

Cii = { c8  g8 c'8 d'8 e'2 }
Am  = { a,8 e8 a8  b8  c'2 }

Fiii = { f,8 c8 f8 c8 }
Giii = { g,8 d8 g8 d8 }

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 88
      \clef treble
      \key c \major
      \time 4/4
      
      r2 r4  g''8 e''8( | e''4) g''8 d''8(  d''4)  e''8  d''8( | d''8) c''2  r8 c''8 b'8 | a'8 b'8 c''8 b'8( b'8) c''8 d''8 e''8( | \break
      e''2.) g''8 e''8( | e''4) g''8 d'''8( d'''4) c'''8 b''8( | b''8) c'''2 r8 c''8 b'8 | a'8 b'8 c''8 b'8( b'8) c''8 d''4       | \break

      c''2        r8 g''8 a''8 b''8 | c'''4 b''8 c'''8 b''8  a''8  g''8  a''8(  | a''8)  g''4. r8 c''8 d''8 e''8 | f''4 e''8 f''8 g''8 c''8 d''8 e''8( | \break
      e''8) e''4. r8 g''8 a''8 b''8 | c'''4 b''8 c'''8 d'''8 c'''8 d'''8 e'''8( | e'''8) g''4. r8 c''8 d''8 e''8 | f''4 e''8 f''8 e''8 d''4      c''8  | \break
      
      b'8 c''4.( c''2) | \bar "|."
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 4/4
      
      r1   | \Ci b,8 g8 b4 | \Am | \Fi   \Gi   |
      \Cii | \Ci b,8 g8 b4 | \Am | \Fiii \Giii |
      
      \Cii | \Fii \Gii | \Cii             | \D \Gi |
      \Cii | \Fii \Gii | c8 g8 b,8 g8 a,2 | \D \Gi |
      
      \Cii |
    }
    \chords {
      
      r1 | c2 g2 | a1:m | f2 g2 |
      c1 | c2 g2 | a1:m | f2 g2 |
      
      c1 | f2 g2 | c1 | d2 g2 |
      c1 | f2 g2 | r1 | d2 g2 |
      
      c1 |
    }
  >>
  \layout {}
  \midi {}
}
