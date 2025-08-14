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

      <bf' d''>8[ <c'' ef''>8] <bf' d''>8[ <c'' ef''>8] <bf' d''>8[ <c'' ef''>8] | <a' c''>8[ <bf' d''>8] <a' c''>8[ <bf' d''>8] <a' c''>8[ <bf' d''>8] | <g' bf'>8[ <a' c''>8] <g' bf'>8[ <a' c''>8] <g' bf'>8[ <a' c''>8] | <fs' a'>16 <e'g'>16 <d' fs'>8~ <d' fs'>4.~ <d' fs'>16 r16 | r4 r4 <a d' fs'>4~ | <a d' fs'>2. | \break
      
      d'4 g'4 bf'4 | <ef' g' bf' d''>4\arpeggio r4 <ef' g' bf' d''>4 | <d'~ fs' c''>4 <d'~ fs'~ bf'>4 <d' fs' a'>4 | bf'2. | r4 r8 g'8 bf'8 d''8 | <bf' g''>2 <bf' g''>4 | <bf'_~ g''>4 <bf'_~ f''>4 <bf' ef''>4 | <f' a' d'' f''>2.\arpeggio | \break
    }
    \new Staff {
      \clef bass
      \key bf \major
      \time 3/4
      
      r2. | r2. | r2. | r2 r8 r16 d,16~ | d,8 a,8 d8[ fs8] r4 | r2. |
      
      r2. | c,4 <g bf d' ef'>4 r4 | <d, d>2. | g,4 <g bf d' ef'>2 | g4 <g bf d' ef'>2 | c4 <g c' ef' g'>2 | f,4 <a c' f'>2 | bf,4 <f a bf d'>2 |
    }
    \chords {
    }
  >>
  \layout {}
  \midi {}
}
