\version "2.24.3"

#(define title      "送别")
#(define title-font "FangSong")
#(define sequence   "EveryonePiano 519")
#(define total-page 1)

\include "../base.ly"

\markup \vspace #1.5

CI   = { c8  g8 c'8 g8 }
CII  = { e8  g8 c'8 g8 }
FI   = { f8  a8 c'8 a8 }
GI   = { d8  g8 b8  g8 }
GII  = { d'8 g8 b8  g8 }
GIII = { g8  b8 d'8 g8 }

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 96
      \clef treble
      \key c \major
      \time 4/4
      
      g''4 e''8 g''8 c'''2       | a''4 c'''4 g''2 | g''4 c''8 d''8 e''4 d''8 c''8 | d''1 | \break
      g''4 e''8 g''8 c'''4. b''8 | a''4 c'''4 g''2 | g''4 d''8 e''8 f''4.     b'8  | c''1 | \break
      
      <f'' a''>4 <a'' c'''>4 <a'' c'''>2 | <g'' b''>4 a''8 b''8 <e'' g'' c'''>2 | a''8 b''8 c'''8 a''8 a''8 g''8 e''8 c''8 | d''1 | \break
      
      g''4 e''8 g''8 c'''4. b''8 | a''4 c'''4 g''2 | g''4 d''8 e''8 f''4. b'8 | c''2 <e'' g'' c'''>2\arpeggio | \bar "|."
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 4/4
      
      \CI \CII | \FI \CII | \CI \CII | \GI \GII        |
      \CI \CII | \FI \CII | \GI \GII | \CI c8 d8 e8 g8 |
      
      \FI \FI | \GIII \CI | \FI \CII | \GI \GII |
      
      \CI \CII | \FI \CII | \GI \GII | c8 g8 c'8 e'8 g'2 |
    }
    \chords {
      c2 c2 | f2 c2 | c2 c2 | g2 g2 |
      c2 c2 | f2 c2 | g2 g2 | c2 r2 |
      
      f2 f2 | g2 c2 | f2 c2 | g2 g2 |
      
      c2 c2 | f2 c2 | g2 g2 | c1 |
    }
  >>
  \layout {}
  \midi {
    \context {
      \ChordNames
      \remove "Note_performer"
    }
  }
}