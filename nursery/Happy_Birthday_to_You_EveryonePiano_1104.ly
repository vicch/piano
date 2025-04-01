\version "2.24.3"
\include "../settings.v1.ly"

\header {
  title = \markup \override #'((font-size . 6)) "Happy Birthday to You"
  tagline = "EveryonePiano 1104"
}

\paper {
  total-page = 1
  ragged-last = ##t
}

\markup \vspace #1.5

Ci   = { c8[ g8  c'8 e'8] r4  }
Cii  = { c8  g8  c'8 e'8  g'4 }
Ciii = { c,8 g,8 c8  e8   g4  }
F    = { f,8 c8  f8  a8   c'4 }
G    = { g,8 d8  g8  b8   d'4 }

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 108
      \clef treble
      \key c \major
      \time 3/4
      
      
      
      \partial 4 g'8. g'16
      
      \repeat volta 3 {
                             | a'4  g'4  c''4 |                a'2 g'8.  g'16  | a'4  g'4  d''4 | \break
        c''2       g'8. g'16 | g''4 e''4 c''4 | \time 4/4  b'4 a'2 f''8. f''16 | \break
        
        \alternative {
          \volta 1 {
            \time 3/4 e''4 c''4 d''4 | c''2 g'8. g'16 |
          }
          \volta 2 {
            \time 3/4 e''4 c''4 d''4 | c''2 g'8. g'16 | \break
          }
          \volta 3 {
            \time 3/4 c''8[ c''8] af'8[ af'8] f'8  f'8 | \grace { c'16 d'16 } <<c'2. e'2.>> | \bar "|."
          }
        }
      }
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 3/4
      
      r4  | \F  | \G   | \F    |
          | \Ci | \Cii | \F r4 |
          
      \Cii | \Ci | \Ciii | \Ciii |
      <c f af>2.\arpeggio | <c, g, c>2.\arpeggio |
     
    }
    \chords {
      
      r4 | f2. | g2. | f2.    |
         | c2. | c2. | f2. r4 |
         
      c2.   | c2. | c2. | c2. |
      f2.:m | c2. |
    }
  >>
  \layout {}
  \midi {}
}
