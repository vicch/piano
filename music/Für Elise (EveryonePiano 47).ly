\version "2.24.3"

#(define title      "Für Elise")
#(define title-font "")
#(define sequence   "EveryonePiano 47")
#(define total-page 2)

\include "../template/base.ly"

\markup \vspace #1.5

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 96
      \clef treble
      \key c \major
      \time 3/4
      
      e''8 ds''8 e''8 ds''8 e''8 b'8 | d''8 c''8 a'2 | e'8 a'8 b'2 | e'8  b'8 c''2 | \break
      e''8 ds''8 e''8 ds''8 e''8 b'8 | d''8 c''8 a'2 | e'8 a'8 b'2 | c''8 b'8 a'2  | \break
      e''8 ds''8 e''8 ds''8 e''8 b'8 | d''8 c''8 a'2 | e'8 a'8 b'2 | e'8  b'8 c''2 | \break
      
      e''8 ds''8 e''8 ds''8 e''8 b'8 | d''8 c''8 a'2 | e'8 a'8 b'2 | c''8 b'8 a'4. b'8 | c''8 d''8 e''4. g'8 | \break
      f''8 e''8 d''4. g'8 | e''8 d''8 c''4. e'8 | d''8 c''8 b'4 e'8 e'8 | e''8 e'8 e''8 e'8 e''8 e'8 | e''8[ e'8 e''8 e'8] e''8 e'''8 | \break
      e''8 ds''8 e''8 ds''8 e''8 b'8 | d''8 c''8 a'2 | e'8 a'8 b'2 | e'8  b'8 c''2 | \break
      
      e''8 ds''8 e''8 ds''8 e''8 b'8 | d''8 c''8 a'2 | e'8 a'8 b'2 | c''8 b'8 a'4. b'8 | c''8 d''8 e''4. g'8 | \break
      f''8 e''8 d''4. g'8 | e''8 d''8 c''4. e'8 | d''8 c''8 b'4 e'8 e'8 | e''8 e'8 e''8 e'8 e''8 e'8 | e''8[ e'8 e''8 e'8] e''8 e'''8 | \break
      e''8 ds''8 e''8 ds''8 e''8 b'8 | d''8 c''8 a'2 | e'8 a'8 b'2 | e'8 b'8 c''2  | \break
      
      e''8 ds''8 e''8 ds''8 e''8 b'8 | d''8 c''8 a'2 | e'8 a'8 b'2 | c''4 b'4 <a' e' a>4~ | <a' e' a>2. | \bar "|."
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 3/4
      
      r2. | r4 a,8 e8 a8 c'8 | r4 e,8 e8 gs8 b8  | r4 a,8 e8 a8 e'8 |
      r2. | r4 a,8 e8 a8 c'8 | r4 e,8 e8 gs8 e'8 | r4 a,8 e8 a4     |
      r2. | r4 a,8 e8 a8 c'8 | r4 e,8 e8 gs8 b8  | r4 a,8 e8 a8 e'8 |

      r2. | r4 a,8 e8 a8 c'8 | r4 e,8 e8 gs8 e'8 | r4 a,8 e8 a4     | r4 c8 g8 c'4 |
      r4 g,8 d8 g4 | r4 a,8 e8 a4 | r4 e,8 e8 gs4 | r2. | r2. |
      r2. | r4 a,8 e8 a8 c'8 | r4 e,8 e8 gs8 b8  | r4 a,8 e8 a8 e'8 |

      r2. | r4 a,8 e8 a8 c'8 | r4 e,8 e8 gs8 e'8 | r4 a,8 e8 a4     | r4 c8 g8 c'4 |
      r4 g,8 d8 g4 | r4 a,8 e8 a4 | r4 e,8 e8 gs4 | r2. | r2. |
      r2. | r4 a,8 e8 a8 c'8 | r4 e,8 e8 gs8 b8  | r4 a,8 e8 a8 e'8 |

      r2. | r4 a,8 e8 a8 c'8 | r4 e,8 e8 gs8 e'8 | r2 <a, c e>4\arpeggio~ | <a, c e>2. |
    }
    \chords {
    }
  >>
  \layout {}
  \midi {}
}
