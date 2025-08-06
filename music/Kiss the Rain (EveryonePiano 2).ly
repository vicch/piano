\version "2.24.3"

#(define title      "Kiss the Rain")
#(define title-font "")
#(define sequence   "EveryonePiano 2")
#(define total-page 2)

\include "../base.ly"

\paper {
  ragged-last = ##t
}

\markup \vspace #1.5

"C1589a" = { c8  g8 c'8 d'8 e'8 r8 }
"D1589a" = { d8  a8 d'8 e'8 f'8 r8 }
"F1589a" = { f,8 c8 f8  g8  a8  r8 }
"G1589a" = { g,8 d8 g8  a8  b8  r8 }
"A1589a" = { a,8 e8 a8  b8  c'8 r8 }

"E158ac" = { e,8 b,8 e8 g8 b8 r8 }

"D158-2" = { d,8 a,8 d8  r8 }
"D158-3" = { d8  a8  d'8 r8 }
"G158"   = { g,8 d8  g8  r8 }

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 72
      \clef treble
      \key c \major
      \time 4/4
      
      \partial 4 \A r16 a'16 c''16 d''16 | d''8 e''8 e''2 r16 c''16 d''16 e''16 | d''8 g''8 g''2 r16 g''16 a''16 b''16 | b''8 c'''8 c'''4. d'''8 \tuplet 3/2 { e''' d''' c'''} | \break
      b''2 r8 c'''8 b''8     g''8        | g''8 a''8 a''2 r8        g''16 f''16 | f''8 g''8 g''2 c''8      d''8        | e''8 f''8  f''2         g''8 f''8                     | \break
      
      e''2.      \A d''16 a'16 c''16 d''16 | d''8 e''8 e''2 r16 c''16 d''16 e''16 | d''8 g''8 g''2 r16 g''16 a''16 b''16 | b''8 c'''8 c'''4. d'''8 \tuplet 3/2 { e''' d''' c'''} | \break
      b''2 r8 c'''8 b''8       g''8        | g''8 a''8 a''2 r8        g''16 f''16 | f''8 g''8 g''2 c''8      d''8        | e''8 f''4 a'8 c''4      b'4                           | \break
      
      c''2 r8      \B c''8 e''8 g''8 | a''2 r8 c''8 c''8 b'8  | c''8 a''8 g''4. c''8 c''8 b'8 | c''8 g''8 g''8 f''8 f''8 e''8 e''8 d''8 | \break
      d''8 e''8 e''4. c''8 e''8 g''8 | a''2 r8 c''8 c''8 a''8 | b''8 g''4. r8   c''8 c''8 b'8 | c''8 g''8 g''8 f''8 e''4.          d''8 | \break
      
      d''2.      \A r16 g'16 c''16 d''16 | d''8 e''8 e''2 r16 c''16 d''16 e''16 | d''8 g''8 g''2 r16 g''16 a''16 b''16 | b''8 c'''8 c'''4. d'''8 \tuplet 3/2 { e''' d''' c'''} | \break
      b''2 r8 c'''8 b''8     g''8        | g''8 a''8 a''2 r8        g''16 f''16 | f''8 g''8 g''2 c''8      d''8        | e''8 f''8  f''2         g''8 f''8                     | \break
      
      e''2.      \A d''16 a'16 c''16 d''16 | d''8 e''8 e''2 r16 c''16 d''16 e''16 | d''8 g''8 g''2 r16 g''16 a''16 b''16 | b''8 c'''8 c'''4. d'''8 \tuplet 3/2 { e''' d''' c'''} | \break
      b''2 r8 c'''8 b''8       g''8        | g''8 a''8 a''2 r8        g''16 f''16 | f''8 g''8 g''2 c''8      d''8        | e''8 f''4 a'8 c''4      b'4                           | \break
      
      c''1 | r1 | \bar "|."
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 4/4
      
                r4 | \"C1589a" r4 | \"E158ac" r4 | \"A1589a" r4 |
      \"G1589a" r4 | \"F1589a" r4 | \"C1589a" r4 | \"D1589a" r4 |
      
      \"E158ac" <g b d'>4 | \"C1589a" r4 | \"E158ac" r4 | \"A1589a" r4      |
      \"G1589a" r4        | \"F1589a" r4 | \"C1589a" r4 | \"D158-3" \"G158" |
      
      \"C1589a" r4 | \"F1589a" r4 | \"C1589a" r4 | \"D1589a" r4             |
      \"C1589a" r4 | \"F1589a" r4 | \"E158ac" r4 | c8 g8 c'8 d'8 <g c' e'>2 |
      
      \"G1589a" r4 | \"C1589a" r4 | \"E158ac" r4 | \"A1589a" r4 |
      \"G1589a" r4 | \"F1589a" r4 | \"C1589a" r4 | \"D1589a" r4 |
      
      \"E158ac" <g b d'>4 | \"C1589a" r4 | \"E158ac" r4      | \"A1589a" r4           |
      \"G1589a" r4        | \"F1589a" r4 | \var \"E158ac" r4 | \var \"D158-2" \"G158" |
      
      c8 g8 c'8 d'8 e'8 g'8 a'8 b'8 | c''1 |
    }
    \chords {
      
          r4 | c2. r4 | e2.:m r4 | a2.:m r4 |
      g2. r4 | f2. r4 | c2.   r4 | d2.:m r4 |
      
      e2.:m g4 | c2. r4 | e2.:m r4 | a2.:m r4 |
      g2.   r4 | f2. r4 | c2.   r4 | d2:m g2  |
      
      c2. r4 | f2. r4 | c2.   r4 | d2.:m r4 |
      c2. r4 | f2. r4 | e2.:m r4 | c1       |
      
      g2. r4 | c2. r4 | e2.:m r4 | a2.:m r4 |
      g2. r4 | f2. r4 | c2.   r4 | d2.:m r4 |
      
      e2.:m g4 | c2. r4 | e2.:m r4 | a2.:m r4 |
      g2.   r4 | f2. r4 | e2.:m r4 | d2:m g2  |
      
      r1 | r1 |
    }
  >>
  \layout {}
  \midi {}
}
