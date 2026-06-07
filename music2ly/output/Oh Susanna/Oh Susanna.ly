\version "2.24.3"

#(define title      "Oh Susanna")
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
      \key g \major
      \time 2/4
      
      \partial 8
      g'16 a'16 |
      b'8 d''8 d''8. e''16 |
      d''8 b'8 g'8. a'16 |
      b'8 b'8 a'8 g'8 |
      a'4. g'16 a'16 \break |
      b'8 d''8 d''8. e''16 |
      d''8 b'8 g'8. a'16 |
      b'8 b'8 a'8 a'8 |
      g'4. g'16 a'16 \break |
      b'8 d''8 d''8. e''16 |
      d''8 b'8 g'8. a'16 |
      b'8 b'8 a'8 g'8 |
      a'4. g'16 a'16 \break |
      b'8 d''8 d''8. e''16 |
      d''8 b'8 g'8. a'16 |
      b'8 b'8 a'8 a'8 |
      g'2 \break |
      <g c'>4 <g c'>4 |
      <c'' e''>8 <c'' e''>4 <c'' e''>8 |
      d'''8 d'''8 b''8 g''8
      
            a'4. g'16 a'16 r2 |
      b'8 d''8 d''8. e''16 r2 |
      d''8 b'8 g'8. a'16 r2 |
      b'8 b'8 a'8 a'8 r2 \break |
      g'4 <g'' d'' b'>4 r2 \bar "|."
    }
    \new Staff {
      \clef bass
      \key g \major
      \time 2/4
      
      \partial 8
      r8 |
      g,8 <d' b>8 <d' b>8 <d' b>8 |
      g,8 <d' b>8 d,8 <d' b>8 |
      g,8 <d' b>8 <d' b>8 <d' b>8 |
      fs,8 <d' a>8 d,8 <d' a>8 \break |
      g,8 <d' b>8 <d' b>8 <d' b>8 |
      g,8 <d' b>8 d,8 <d' b>8 |
      g,8 <d' b>8 d,8 <c' a>8 |
      g,8 <d' b>8 d,8 <d' b>8 \break |
      g,8 <d' b>8 <d' b>8 <d' b>8 |
      g,8 <d' b>8 d,8 <d' b>8 |
      g,8 <d' b>8 <d' b>8 <d' b>8 |
      fs,8 <d' a>8 d,8 <d' a>8 \break |
      g,8 <d' b>8 <d' b>8 <d' b>8 |
      g,8 <d' b>8 d,8 <d' b>8 |
      g,8 <d' b>8 d,8 <c' a>8 |
      g,8 <d' b>8 a,8 b,8 \break |
      g,8 <e' c'>8 <e' c'>8 <e' c'>8 |
      g,8 <e' c'>8 <e' c'>8 <e' c'>8 |
      g,8 <d' b>8 <d' b>8 <d' b>8
      
            fs8 <d' a>8 <d' a>8 <d' a>8 r2 |
      g8 <d' b>8 <d' b>8 <d' b>8 r2 |
      g8 <d' b>8 d8 <d' b>8 r2 |
      d8 <c' a>8 e8 fs8 r2 \break |
      g4 g,4 r2 \bar "|."
    }
    \chords {
    }
  >>
  \layout {}
  \midi {}
}
