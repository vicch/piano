\version "2.24.3"

#(define title      "It's A Small World")
#(define title-font "")
#(define sequence   "Sheet image: source.png")
#(define total-page 1)

\include "../../../template/base.ly"

\markup \vspace #1.5

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 96
      \clef treble
      \key d \major
      \time 4/4
      
      \partial 2 r4 fs'8 g'8 |
      a'4 d4 fs''4 a4 |
      d''4 d'2 e''8 d''8 |
      d''4 e4 cs''4 a4 |
      cs''4 cs'2 e'8 fs'8 \break |
      g'4 e4 e''4 a4 |
      cs''4 cs'2 d''8 cs''8 |
      b'4 d4 a'4 a4 |
      a'4 d'2 fs'8 g'8 \break |
      a'4 d4 d''8 a4 e''8 |
      fs''4 d'4 e''8 a4 d''8 |
      b'4 g4 e''8 b4 fs''8 |
      g''4 e4 fs''8 b4 e''8 \break |
      a'4 <cs' a>4 g''4 e4 |
      fs''4. <g cs'>4 e4 e''8 |
      d''1 |
      d'8 a8 fs8 a8 d2 \break |
      d''4. <fs a>4 d4 d''8 |
      fs''4 <fs a>4 d''4 d4 |
      r2
      
            e''4. e''8 e''2 |
      e''4. e''8 g''4 e''4 |
      fs''4. fs''8 fs''2 |
      fs''4. fs''8 a''4 fs''4 \break |
      g''4. g''8 g''4 fs''8 e''8 |
      a'2 cs''2 |
      d''1 \bar "|."
    }
    \new Staff {
      \clef bass
      \key d \major
      \time 4/4
      
      \partial 2 r4 fs'8 g'8 |
      a'4 d4 fs''4 a4 |
      d''4 d'2 e''8 d''8 |
      d''4 e4 cs''4 a4 |
      cs''4 cs'2 e'8 fs'8 \break |
      g'4 e4 e''4 a4 |
      cs''4 cs'2 d''8 cs''8 |
      b'4 d4 a'4 a4 |
      a'4 d'2 fs'8 g'8 \break |
      a'4 d4 d''8 a4 e''8 |
      fs''4 d'4 e''8 a4 d''8 |
      b'4 g4 e''8 b4 fs''8 |
      g''4 e4 fs''8 b4 e''8 \break |
      a'4 <cs' a>4 g''4 e4 |
      fs''4. <g cs'>4 e4 e''8 |
      d''1 |
      d'8 a8 fs8 a8 d2 \break |
      d''4. <fs a>4 d4 d''8 |
      fs''4 <fs a>4 d''4 d4 |
      r2
      
            <cs' a>4 <e a,>4 <cs' a>4 <e a,>4 |
      <cs' a>4 <e a,>4 <cs' a>4 <e a,>4 |
      <fs' a>4 <d a,>4 <fs' a>4 <d a,>4 |
      <fs' a>4 <d a,>4 <fs' a>4 <d a,>4 \break |
      <g' b>4 <d b,>4 <g' b>4 <d b,>4 |
      <e cs' a>2 <g cs' a>2 |
      d'8 a8 fs8 a8 d2 \bar "|."
    }
    \chords {
    }
  >>
  \layout {}
  \midi {}
}
