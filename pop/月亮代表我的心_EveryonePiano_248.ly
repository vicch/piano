\version "2.24.3"
\include "../settings.v1.ly"

\header {
  title = \markup \override #'((font-name . "FangSong")(font-size . 6)) "月亮代表我的心"
  tagline = "EveryonePiano 248"
}

\paper {
  total-page = 2
  ragged-last = ##t
}

\markup \vspace #1.5

CI   = { c8  g8  c'8 e'8 g'2  }
CII  = { c,8 g,8 c8  e8  g2   }
DmI  = { d,8 a,8 d8  f8  a2   }
EmI  = { e,8 b,8 e8  g8  b2   }
FI   = { f8  c'8 f'8 a'8 c''2 }
FII  = { f,8 c8  f8  a8  c'2  }
GI   = { g,8 d8  g8  b8  d'2  }
AmI  = { a,8 e8  a8  c'8 e'2  }

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
      
      b'2.  r8   g'8  | c''4. e''8 g''4.      c''8 | b'4.  e''8 g''4.     g''8 | a''4. b''8 c'''4 a''4      | \break
      g''2. e''8 d''8 | c''4. c''8 c''4  e''8 d''8 | c''4. c''8 c''4 d''8 e''8 | d''4. c''8 a'4   e''4      | \break
      d''2. r8   g'8  | c''4. e''8 g''4.      c''8 | b'4.  e''8 g''4.     g''8 | a''4. b''8 c'''4 a''4      | \break
      g''2. e''8 d''8 | c''4. c''8 c''4  e''8 d''8 | c''4. c''8 c''4 d''8 e''8 | d''4. a'8  b'4   c''8 d''8 | \break
      
      c''2. g''4 | e''4. d''8 c''4 g''4 | b'2. a'8 b'8 | a'4.  b'8  a'4  g'4       | \break \noPageBreak
      e''2. g''4 | e''4. d''8 c''4 g''4 | b'2. a'8 b'8 | c''4. c''8 c''4 d''8 e''8 | \break \noPageBreak
      
      d''2. r8   g'8  | c''4. e''8 g''4.      c''8 | b'4.  e''8 g''4.     g''8 | a''4. b''8 c'''4 a''4      | \break \noPageBreak
      g''2. e''8 d''8 | c''4. c''8 c''4  e''8 d''8 | c''4. c''8 c''4 d''8 e''8 | d''4. a'8  b'4   c''8 d''8 | \break \noPageBreak
      c''2. e''8 d''8 | c''4. c''8 c''4  e''8 d''8 | c''4. c''8 c''4 d''8 e''8 | d''4. a'8  b'4   d''4      | \break \noPageBreak
      
      c''1 | <c' e' g' c''>1\arpeggio | \bar "|."
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 4/4
      
      \CI | \AmI | \FI |
      
      \GI | \CI  | \EmI | \FII |
      \GI | \CII | \AmI | \DmI |
      \GI | \CII | \EmI | \FII |
      \GI | \CII | \AmI | \DmI |
      
      \CII | \CII | \EmI | \FII |
      \AmI | \CII | \EmI | \FII |
      
      \GI  | \CII | \EmI | \FII |
      \GI  | \CII | \AmI | \DmI |
      \CII | \CI  | \AmI | \DmI |
      
      c,8 g,8 c8 e8 g8 c'8 e'8 g'8 | <c, c>1 |
    }
    \chords {
      
      c1 | a1:m | f1 |
      
      g1 | c1 | e1:m | f1   |
      g1 | c1 | a1:m | d1:m |
      g1 | c1 | e1:m | f1   |
      g1 | c1 | a1:m | d1:m |
      
      c1   | c1 | e1:m | f1 |
      a1:m | c1 | e1:m | f1 |
      
      g1 | c1 | e1:m | f1   |
      g1 | c1 | a1:m | d1:m |
      c1 | c1 | a1:m | d1:m |
      
      c1 | c1 |
    }
  >>
  \layout {}
}

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
      
      b'2.  r8   g'8  | c''4. e''8 g''4.      c''8 | b'4.  e''8 g''4.     g''8 | a''4. b''8 c'''4 a''4      | \break
      g''2. e''8 d''8 | c''4. c''8 c''4  e''8 d''8 | c''4. c''8 c''4 d''8 e''8 | d''4. c''8 a'4   e''4      | \break
      d''2. r8   g'8  | c''4. e''8 g''4.      c''8 | b'4.  e''8 g''4.     g''8 | a''4. b''8 c'''4 a''4      | \break
      g''2. e''8 d''8 | c''4. c''8 c''4  e''8 d''8 | c''4. c''8 c''4 d''8 e''8 | d''4. a'8  b'4   c''8 d''8 | \break
      
      c''2. g''4 | e''4. d''8 c''4 g''4 | b'2. a'8 b'8 | a'4.  b'8  a'4  g'4       | \break \noPageBreak
      e''2. g''4 | e''4. d''8 c''4 g''4 | b'2. a'8 b'8 | c''4. c''8 c''4 d''8 e''8 | \break \noPageBreak
      
      d''2. r8   g'8  | c''4. e''8 g''4.      c''8 | b'4.  e''8 g''4.     g''8 | a''4. b''8 c'''4 a''4      | \break \noPageBreak
      g''2. e''8 d''8 | c''4. c''8 c''4  e''8 d''8 | c''4. c''8 c''4 d''8 e''8 | d''4. a'8  b'4   c''8 d''8 | \break \noPageBreak
      c''2. e''8 d''8 | c''4. c''8 c''4  e''8 d''8 | c''4. c''8 c''4 d''8 e''8 | d''4. a'8  b'4   d''4      | \break \noPageBreak
      
      c''1 | <c' e' g' c''>1\arpeggio | \bar "|."
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 4/4
      
      \CI | \AmI | \FI |
      
      \GI | \CI  | \EmI | \FII |
      \GI | \CII | \AmI | \DmI |
      \GI | \CII | \EmI | \FII |
      \GI | \CII | \AmI | \DmI |
      
      \CII | \CII | \EmI | \FII |
      \AmI | \CII | \EmI | \FII |
      
      \GI  | \CII | \EmI | \FII |
      \GI  | \CII | \AmI | \DmI |
      \CII | \CI  | \AmI | \DmI |
      
      c,8 g,8 c8 e8 g8 c'8 e'8 g'8 | <c, c>1 |
    }
  >>
  \midi {}
}
