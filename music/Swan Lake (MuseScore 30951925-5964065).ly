\version "2.24.3"

#(define title      "Swan Lake")
#(define title-font "")
#(define sequence   "MuseScore 30951925-5964065")
#(define total-page 2)

\include "../base.ly"

\markup \vspace #1.5

"B135" = { b8 d'8 fs'8 d'8 }

"E513" = { b8 e'8 g'8 e'8 }

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 96
      \clef treble
      \key d \major
      \time 4/4
      
      r1                            | r1                        | fs''2 b'8 cs''8 d''8 e''8 | fs''4. d''8 fs''4. d''8 | \break
      fs''4. b'8 d''8 b'8 fs'8 d''8 | b'2    r8 e''8 d''8 cs''8 | fs''2 b'8 cs''8 d''8 e''8 | fs''4. d''8 fs''4. d''8 | \break
      fs''4. b'8 d''8 b'8 fs'8 d''8 | b'4 r4 r4      b'4        |
    }
    \new Staff {
      \clef bass
      \key d \major
      \time 4/4
      
      \"B135" \"B135"       | \"B135" \"B135" | \"B135" \"E513" | \"B135" \"B135" |
      \"B135" g8 b8 fs8 as8 | \"B135" \"E513" | \"B135" \"E513" | \"B135" \"B135" |
      \"B135" g8 b8 fs8 as8 | \"B135" g4 r4   |
    }
    \chords {
      b2:m b2:m | b2:m b2:m | b2:m e2:m | b2:m b2:m |
      b2:m r2   | b2:m e2:m | b2:m e2:m | b2:m b2:m |
      b2:m r2   | b2:m r2   |
    }
  >>
  \layout {}
  \midi {}
}
