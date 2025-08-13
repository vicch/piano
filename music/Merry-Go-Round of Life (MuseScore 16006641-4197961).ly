\version "2.24.3"

#(define title      "Merry-Go-Around of Life")
#(define title-font "")
#(define sequence   "MuseScore 16006641-4197961")
#(define total-page 1)

\include "../base.ly"

\markup \vspace #1.5

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 96
      \clef treble
      \key bf \major
      \time 3/4
      
      d''8[ ef''8] d''8[ ef''8] d''8[ ef''8] | c''8[ d''8] c''8[ d''8] c''8[ d''8] | bf'8[ c''8] bf'8[ c''8] bf'8[ c''8] | a'16 g'16 fs'8~ fs'4.~ fs'16 r16 |  r4 r4 <a d' fs'>4~ | <a d' fs'>2. | \break
    }
    \new Staff {
      \clef bass
      \key bf \major
      \time 3/4
      
      \clef treble bf'8[ c''8] bf'8[ c''8] bf'8[ c''8] | a'8[ bf'8] a'8[ bf'8] a'8[ bf'8] | g'8[ a'8] g'8[ a'8] g'8[ a'8] | fs'16 e'16 d'8~ d'4.~ d'16_[ \clef bass d,16]~ | d,8 a,8 d8[ fs8] r4 | r1 | \break
    }
    \chords {
    }
  >>
  \layout {}
  \midi {}
}
