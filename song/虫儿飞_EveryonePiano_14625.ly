\version "2.24.3"
\include "../template.v1.ly"

\header {
  title = \markup \override #'((font-name . "FangSong")(font-size . 6)) "虫儿飞"
  tagline = "EveryonePiano 14625"
}

\paper {
  total-page = 2
}

\markup \vspace #1.5

Cfive = { c4  g4 c'2 }
Ffive = { f,4 c4 f2  }
Gfive = { g,4 d4 g2  }
Afive = { a,4 e4 a2  }

\score {
  \new PianoStaff <<
    \new Staff {
      \tempo 4 = 108
      \clef treble
      \key c \major
      \time 4/4
      
      \ottava #1
      e'''4^3 e'''8 e'''8 f'''4 g'''4 | e'''2 d'''2 |
      c'''4^3 c'''8 c'''8 d'''4 e'''4 | e'''2 b''2  | \break
      
      a''4^1 e'''4 d'''2 | a''4 e'''4 d'''2 | a''4 e'''4 d'''4. c'''8 | c'''1 | \break
      
      \ottava #0
      e''4^3 e''8 e''8 f''4 g''4 | e''2 d''2 |
      c''4^3 c''8 c''8 d''4 e''4 | e''2 b'2  | \break
      
      a'4^1 e''4 d''2 | a'4 e''4 d''2 | a'4 e''4^3 d''4. c''8 | c''2 e''4 d''4 | \break
      
      g''2. f''8 e''8 | d''2. g''8 f''8 | e''4 f''8 g''8 r4 e''4 | d''2. r8 c''8^3 | \break
      
      a'4 e''4 d''4. c''8 | g'4^1 d''4 c''2 | f''8^4 e''8 f''8 e''8 c''2 | f''8 e''8 f''8 e''8 c''4 d''4 | c''1 | \bar "|."
    }
    \new Staff {
      \clef bass
      \key c \major
      \time 4/4
      
      <c'^3 e'^1> 1 | <b d'> 1 | <a^3 c'^1> 1 | <g b> 1 |
      
      f2^5 g2 | f2 g2 | f2 g2  <a c'> 1 |
      
      \Cfive | \Gfive | \Afive | \Gfive |
      
      f,2^5 g,2 | f,2 g,2 | f,2 g,2 | \Afive |
      
      \Cfive | \Gfive | \Afive | \Gfive |
      
      f,2^4 g,2 | e,2 a,2 | \Ffive | \Gfive | <c e g>1\arpeggio |
    }
    \chords {
      r1   | r1   | r1   | r1   |
      r1   | r1   | r1   | r1   |
      
      c1:5 | g1:5 | a1:5 | g1:5 |
      r1   | r1   | r1   | a1:5 |
      
      c1:5 | g1:5 | a1:5 | g1:5 |
      r1   | r1   | f1:5 | g1:5 | r1 |
    }
  >>
  \layout {}
  \midi {}
}
