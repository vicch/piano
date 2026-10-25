\version "2.24.3"

#(define title      "Oh! Susanna")
#(define title-font "")
#(define sequence   "EveryonePiano 509")
#(define total-page 1)

\include "../template/base.ly"

\markup \vspace #1.5

"C513" = { g8[  <e' c'>8^. <e' c'>8^. <e' c'>8^.] }
"D351" = { fs8[ <d' a>8^.  <d' a>8^.  <d' a>8^.]  }
"G135" = { g8[  <d' b>8^.  <d' b>8^.  <d' b>8^.]  }

"G5135" = { g8[  <d' b>8^. d8 <d' b>8^.] }
"D1358" = { fs8[ <d' a>8^. d8 <d' a>8^.] }

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 96
      \clef treble
      \key g \major
      \time 2/4
      
      \partial 8 g'16 a'16 | b'8 d''8 d''8. e''16 | d''8 b'8 g'8. a'16 | b'8 b'8 a'8 g'8 | \break
      a'4.       g'16 a'16 | b'8 d''8 d''8. e''16 | d''8 b'8 g'8. a'16 | b'8 b'8 a'8 a'8 | \break
      g'4.       g'16 a'16 | b'8 d''8 d''8. e''16 | d''8 b'8 g'8. a'16 | b'8 b'8 a'8 g'8 | \break
      a'4.       g'16 a'16 | b'8 d''8 d''8. e''16 | d''8 b'8 g'8. a'16 | b'8 b'8 a'8 a'8 | \break

      g'2 | <g' c''>4 <g' c''>4 | <c'' e''>8 <c'' e''>4 <c'' e''>8 | d''8 d''8 b'8 g'8 | \break
      
      a'4.       g'16 a'16 | b'8 d''8 d''8. e''16 | d''8 b'8 g'8. a'16 | b'8 b'8 a'8 a'8 | g'4 <b' d'' g''>4 | \bar "|."
    }
    \new Staff {
      \clef bass
      \key g \major
      \time 2/4
      
      \partial 8 r8 | \"G135" | \"G5135" | \"G135"                      |
      \"D1358"      | \"G135" | \"G5135" | g8[  <d' b>8^. d8 <c' a>8^.] |
      \"G5135"      | \"G135" | \"G5135" | \"G135"                      |
      \"D1358"      | \"G135" | \"G5135" | g8[  <d' b>8^. d8 <c' a>8^.] |
      
      g8[ <d' b>8^. a8 b8] | \"C513" | \"C513" | \"G135" |
      
      \"D351"       | \"G135" | \"G5135" | d8 <c' a>8 e8 fs8 | g4 g,4   |
    }
    \chords {
      r8 | g2 | g2 | g2 |
      d2 | g2 | g2 | r2 |
      g2 | g2 | g2 | g2 |
      d2 | g2 | g2 | r2 |
      r2 | c2 | c2 | g2 |
      d2 | g2 | g2 | r2 |
    }
  >>
  \layout {}
  \midi {}
}
