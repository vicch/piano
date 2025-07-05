\version "2.24.3"

#(define title      "虫儿飞")
#(define title-font "FangSong")
#(define sequence   "EveryonePiano 14625")
#(define total-page 1)

\include "../base.ly"

\markup \vspace #1.5

CI = { c4  g4 c'2 }
FI = { f,4 c4 f2 }
GI = { g,4 d4 g2 }
AI = { a,4 e4 a2 }

\score {
  \new PianoStaff <<
    \new Staff {
      \tempo 4 = 108
      \clef treble
      \key c \major
      \time 4/4
      
      \clef "treble^8"
      e'''4^3 e'''8 e'''8 f'''4 g'''4 | e'''2      d'''2 | c'''4^3 c'''8 c'''8 d'''4 e'''4  | e'''2 b''2 | \break
      a''4^1  e'''4       d'''2       | a''4 e'''4 d'''2 | a''4    e'''4       d'''4. c'''8 | c'''1      | \break
      
      \clef treble
      e''4^3 e''8 e''8 f''4 g''4 | e''2     d''2 | c''4^3 c''8 c''8 d''4 e''4  | e''2 b'2       | \break
      a'4^1  e''4      d''2      | a'4 e''4 d''2 | a'4    e''4^3    d''4. c''8 | c''2 e''4 d''4 | \break
      
      g''2. f''8 e''8 | d''2. g''8 f''8 | e''4 f''8 g''8 r4 e''4 | d''2. r8 c''8^3 | \break
      
      a'4 e''4 d''4. c''8 | g'4^1 d''4 c''2 | f''8^4 e''8 f''8 e''8 c''2 | f''8 e''8 f''8 e''8 c''4 d''4 | c''1 | \bar "|."
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 4/4
      
      \clef "bass^8"
      <c' e'>1 | <b d'>1 | <a c'>1 | <g b>1  |
      f2 g2    | f2 g2   | f2 g2   | <a c'>1 |
      
      \clef bass
      \CI     | \GI     | \AI     | \GI |
      f,2 g,2 | f,2 g,2 | f,2 g,2 | \AI |
      
      \CI | \GI | \AI | \GI |
      
      f,2 g,2 | e,2 a,2 | \FI | \GI | <c e g>1\arpeggio |
    }
    \chords {
      r1 | r1 | r1 | r1 |
      r1 | r1 | r1 | r1 |
      
      c1 | g1 | a1 | g1 |
      r1 | r1 | r1 | a1 |
      
      c1 | g1 | a1 | g1 |
      
      r1 | r1 | f1 | g1 | r1 |
    }
  >>
  \layout {}
  \midi {}
}
