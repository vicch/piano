\version "2.24.3"

#(define title      "Oh My Darling, Clementine")
#(define title-font "")
#(define sequence   "EveryonePiano 979")
#(define total-page 1)

\include "../base.ly"

\markup \vspace #1.5

CI = { c4 <e g>4  <e g>4  }
GI = { g4 <b d'>4 <b d'>4 }

CII = { c8  g8 c'8 e'8 g'4 }
GII = { g,8 d8 g8  b8  d'4 }

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 96
      \clef treble
      \key c \major
      \time 3/4
      
      \partial 4 c''8 c''8 | c''4 g'4  e''8 e''8 | e''4 c''4 c''8 e''8 | g''4 g''4 f''8 e''8 | \break
      d''2       d''8 e''8 | f''4 f''4 e''8 d''8 | e''4 c''4 c''8 e''8 | d''4 g'4  b'8  d''8 | \break
      
      c''2       c''8 c''8 | c''4 g'4  e''8 e''8 | e''4 c''4 c''8 e''8 | g''4 g''4 f''8 e''8 | \break
      d''2       d''8 e''8 | f''4 f''4 e''8 d''8 | e''4 c''4 c''8 e''8 | d''4 g'4  b'8  d''8 | c''2. | \bar "|."
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 3/4
      
      r4  | \CI | \CI | \GI |
      \GI | \GI | \CI | \GI |
      
      <c e g>2\arpeggio r4 | \CII | \CII | \GII |
      \GII                 | \GII | \CII | \GII | <c e g>2.\arpeggio
    }
    \chords {
      
      r4  | c2. | c2. | g2. |
      g2. | g2. | c2. | g2. |
      
      c2 r4 | c2. | c2. | g2. |
      g2.   | g2. | c2. | g2. | c2. |
    }
  >>
  \layout {}
}

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 96
      \clef treble
      \key c \major
      \time 3/4
      
      \partial 4 c''8 c''8 | c''4 g'4  e''8 e''8 | e''4 c''4 c''8 e''8 | g''4 g''4 f''8 e''8 | \break
      d''2       d''8 e''8 | f''4 f''4 e''8 d''8 | e''4 c''4 c''8 e''8 | d''4 g'4  b'8  d''8 | \break
      
      c''2       c''8 c''8 | c''4 g'4  e''8 e''8 | e''4 c''4 c''8 e''8 | g''4 g''4 f''8 e''8 | \break
      d''2       d''8 e''8 | f''4 f''4 e''8 d''8 | e''4 c''4 c''8 e''8 | d''4 g'4  b'8  d''8 | c''2. | \bar "|."
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 3/4
      
      r4  | \CI | \CI | \GI |
      \GI | \GI | \CI | \GI |
      
      <c e g>2\arpeggio r4 | \CII | \CII | \GII |
      \GII                 | \GII | \CII | \GII | <c e g>2.\arpeggio
    }
  >>
  \midi {}
}
