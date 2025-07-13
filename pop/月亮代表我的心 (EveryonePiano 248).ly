\version "2.24.3"

#(define title      "月亮代表我的心")
#(define title-font "FangSong")
#(define sequence   "EveryonePiano 248")
#(define total-page 2)

\include "../base.ly"

\paper {
  ragged-last = ##t
}

\markup \vspace #1.5

"C58ac"  = { c8  g8  c'8 e'8 g'2  }
"Dm58ac" = { d,8 a,8 d8  f8  a2   }
"Em58ac" = { e,8 b,8 e8  g8  b2   }
"F58ac"  = { f8  c'8 f'8 a'8 c''2 }
"G58ac"  = { g,8 d8  g8  b8  d'2  }
"Am58ac" = { a,8 e8  a8  c'8 e'2  }

"C58ac," = { c,8 g,8 c8  e8  g2  }
"F58ac," = { f,8 c8  f8  a8  c'2 }

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 88
      \clef treble
      \key c \major
      \time 4/4
      
      g''2~^5 g''8 e''8 d''8 c''8 | e''2 r8 a'8^1 c''8^2 e''8^3 | a''2~^5 a''8 f''8 d''8 c''8^3 | \break
      
      b'2.  r8 \A  g'8^1 | c''4.^2 e''8^3 g''4.      c''8 | b'4.^1 e''8 g''4.     g''8^2 | a''4. b''8 c'''4 a''4      | \break
      g''2. e''8^5 d''8  | c''4.   c''8   c''4  e''8 d''8 | c''4.  c''8 c''4 d''8 e''8   | d''4. c''8 a'4   e''4      | \break
      d''2. r8     g'8   | c''4.   e''8   g''4.      c''8 | b'4.   e''8 g''4.     g''8   | a''4. b''8 c'''4 a''4      | \break
      g''2. e''8   d''8  | c''4.   c''8   c''4  e''8 d''8 | c''4.  c''8 c''4 d''8 e''8   | d''4. a'8  b'4   c''8 d''8 | \break
      
      c''2. \B g''4^5 | e''4. d''8 c''4 g''4 | b'2.^1 a'8^2 b'8 | a'4.  b'8  a'4  g'4       | \break \noPageBreak
      e''2.^5  g''4   | e''4. d''8 c''4 g''4 | b'2.   a'8^1 b'8 | c''4. c''8 c''4 d''8 e''8 | \break \noPageBreak
      
      d''2. r8 \A g'8  | c''4. e''8 g''4.      c''8 | b'4.  e''8 g''4.     g''8 | a''4. b''8 c'''4 a''4      | \break \noPageBreak
      g''2. e''8  d''8 | c''4. c''8 c''4  e''8 d''8 | c''4. c''8 c''4 d''8 e''8 | d''4. a'8  b'4   c''8 d''8 | \break \noPageBreak
      c''2. e''8  d''8 | c''4. c''8 c''4  e''8 d''8 | c''4. c''8 c''4 d''8 e''8 | d''4. a'8  b'4   d''4      | \break \noPageBreak
      
      c''1 | <c' e' g' c''>1\arpeggio | \bar "|."
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 4/4
      
      \"C58ac" | \"Am58ac" | \"F58ac" |
      
      \"G58ac" | \"C58ac"  | \"Em58ac" | \"F58ac," |
      \"G58ac" | \"C58ac," | \"Am58ac" | \"Dm58ac" |
      \"G58ac" | \"C58ac," | \"Em58ac" | \"F58ac," |
      \"G58ac" | \"C58ac," | \"Am58ac" | \"Dm58ac" |
      
      \"C58ac," | \"C58ac," | \"Em58ac" | \"F58ac," |
      \"Am58ac" | \"C58ac," | \"Em58ac" | \"F58ac," |
      
      \"G58ac"  | \"C58ac," | \"Em58ac" | \"F58ac," |
      \"G58ac"  | \"C58ac," | \"Am58ac" | \"Dm58ac" |
      \"C58ac," | \"C58ac"  | \"Am58ac" | \"Dm58ac" |
      
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
  \midi {}
}
