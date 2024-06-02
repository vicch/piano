\version "2.24.3"
\include "../template.v1.ly"

\header {
  title = \markup \override #'((font-size . 6)) "Happy Birthday to You"
  tagline = "EveryonePiano 495"
}

\markup \vspace #1.25

C    = { c4 <<g4 c'4>> <<g4 c'4>> }
Csus = { c4 <<g4 bf4>> <<g4 bf4>> }
Edim = { e4 <<g4 bf4>> <<g4 bf4>> }
F    = { f4 <<a4 c'4>> <<a4 c'4>> }
As   = { d4 <<f4 bf4>> <<f4 bf4>> }

\score {
  \new PianoStaff <<
    \new Staff {
      \tempo 4 = 120
      \clef treble
      \key f \major
      \time 3/4
      
      \partial 4 c''8^1 c''8 | d''4^2  c''4^1 f''4^4 | e''2^3        c''8^1  c''8  | d''4^2 c''4^1 g''4^5 | f''2^4    \break
                 c''8^1 c''8 | c'''4^5 a''4^3 f''4^1 | e''4^2 d''4^2 bf''8^4 bf''8 | a''4^3 f''4^1 g''4^2 | f''2.^1 | \bar "|."
    }
    \new Staff {
      \clef bass
      \key f \major
      \time 3/4
      
      r4 | \F | \C  | \Edim | \F
         | \F | \As | \Csus | <f a c'>2.\arpeggio
    }
    \chords {
      \set noChordSymbol = ""

      r4 | f2. | c2.  | e2.:dim | f2.
         | f2. | as2. | c2.:sus | f2.
    }
  >>
  \layout {}
  \midi {}
}
