\version "2.24.3"
\include "../template.v1.ly"

\header {
  title = \markup \override #'((font-size . 6)) "Happy Birthday to You"
  tagline = "MuseScore 173585-166951"
}

\markup \vspace #1.25

\score {
  \new PianoStaff <<
    \new Staff {
      \tempo 4 = 120
      \clef treble
      \key c \major
      \time 3/4
      
      g'8^1 g'8 a'4^2  g'4^1  | c''4^4 b'2^3       | g'8^1  g'8  a'4^2  g'4^1  | d''4^5 c''2^4 | \break
      g'8^1 g'8 g''4^5 e''4^3 | c''4^1 b'4^3 a'4^2 | f''8^4 f''8 e''4^3 c''4^1 | d''4^2 c''2^1 | \bar "|."
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 3/4
      
      r4 <c e  g >2 | r4 <d f g >2 | r4 <b, f g >2 | r4       <c e g>2 |
      r4 <e as c'>2 | r4 <f a c'>2 | r4 <e  g c'>2 | <d f g>4 <c e g>2 |
    }
    \chords {
      \set noChordSymbol = ""

      r4 c2   | r4 g2:7 | r4 g2:7 | r4   c2 | \break
      r4 c2:7 | r4 f2   | r4 c2   | g4:7 c2 |
    }
  >>
  \layout {}
  \midi {}
}
