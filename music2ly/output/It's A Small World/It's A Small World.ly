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
      
      \partial 4 fs'8 g'8 |
      a'4 fs''4 d''4 e''8 d''8 |
      d''4 cs''4 cs''4 e'8 fs'8 |
      g'4 e''4 cs''4 d''8 cs''8 \break |
      b'4 a'4 a'4 fs'8 g'8 |
      a'4 d''8 e''8 fs''4 e''8 d''8 |
      b'4 e''8 fs''8 g''4 fs''8 e''8 |
      a'4 g''4 fs''4. e''8 \break |
      d''1 |
      d''4. d''8 fs''4 d''4
      
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
      
      r4 |
      d,4 a,4 d'2 |
      e,4 a,4 cs'2 |
      e,4 a,4 cs'2 \break |
      d,4 a,4 d'2 |
      d,4 a,4 d'4 a,4 |
      g,4 b,4 e,4 b,4 |
      <cs' a,>4 e,4 <gs cs'>4 e,4 \break |
      d'8 a,8 fs,8 a,8 d,2 |
      <fs, a,>4 d,4 <fs, a,>4 d,4
      
            <cs' a>4 e4 <cs' a>4 e4 |
      <cs' a>4 e4 <cs' a>4 e4 |
      <fs a>4 d4 <fs a>4 d4 |
      <fs a>4 d4 <fs a>4 d4 \break |
      <g b>4 d4 <g b>4 d4 |
      <e cs' a>2 <g cs' a>2 |
      d'8 a8 fs8 a8 d2 \bar "|."
    }
    \chords {
    }
  >>
  \layout {}
  \midi {}
}
