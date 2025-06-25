\version "2.24.3"

#(define title      "粉刷匠")
#(define title-font "FangSong")
#(define sequence   "EveryonePiano 656")
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
      \key g \major
      \time 2/4
      
      d''8^. b'8^. d''8^. b'8^. | d''8^. b'8^. g'4-- | a'8^. c''8^. b'8^. a'8^. | d''2-- | \break
      d''8^. b'8^. d''8^. b'8^. | d''8^. b'8^. g'4-- | a'8^. c''8^. b'8^. a'8^. | g'2--  | \break
      
      a'8^.  a'8^. c''8^. c''8^. | b'8^.  g'8^. d''4-- | a'8^. c''8^. b'8^. a'8^. | d''2-- | \break
      d''8^. b'8^. d''8^. b'8^.  | d''8^. b'8^. g'4--  | a'8^. c''8^. b'8^. a'8^. | g'2--  | \bar "|"
    }
    \new Staff {
      \clef bass
      \key g \major
      \time 2/4
      
      r8 <<g8 d'8^.>> r8 <<g8 d'8^.>> | r8 <<g8 d'8^.>> r8 <<b8 d'8^.>> | r8 <<a8 c'8 d'8^.>> r8 <<a8 c'8 d'8^.>> | r8 <<c'8 d'8^.>> b8 a8 |
      r8 <<g8 d'8^.>> r8 <<g8 d'8^.>> | r8 <<g8 d'8^.>> r8 <<b8 d'8^.>> | r8 <<a8 c'8 d'8^.>> r8 <<a8 c'8 d'8^.>> | r8 <<b8  d'8^.>> a8 g8 |
      
      r8 <<a8 c'8 d'8^.>> r8 <<a8 c'8 d'8^.>> | r8 <<b8 d'8^.>> r8 <<b8 d'8^.>> | r8 <<a8 c'8 d'8^.>> r8 <<a8 c'8 d'8^.>> | r8 <<c'8 d'8^.>> b8 a8 |
      r8 <<g8 d'8^.>>     r8 <<g8 d'8^.>>     | r8 <<g8 d'8^.>> r8 <<b8 d'8^.>> | r8 <<d8 a8^.>>      r8 <<d8 c'8^.>>     | r8 <<g8  b8^.>>  g,4-- |
    }
    \chords {
    }
  >>
  \layout {}
  \midi {}
}
