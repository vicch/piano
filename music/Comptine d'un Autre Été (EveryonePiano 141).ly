\version "2.24.3"
\include "../settings.v1.ly"

\header {
  title = \markup \override #'((font-size . 6)) "Comptine d'un Autre Été"
  tagline = "EveryonePiano 141"
}

\paper {
  total-page = 2
}

\markup \vspace #1.5

DI    = { <<d8 d'8>> a8 <<fs8 d'8>> a8 <<d8 d'8>> a8 <<fs8 d'8>> a8 }
DsixI = { <<d8 d'8>> b8 <<fs8 d'8>> b8 <<d8 d'8>> b8 <<fs8 d'8>> b8 }
EmI   = { <<e8 e'8>> b8 <<g8  e'8>> b8 <<e8 e'8>> b8 <<g8  e'8>> b8 }
GI    = { <<d8 d'8>> b8 <<g8  d'8>> b8 <<d8 d'8>> b8 <<g8  d'8>> b8 }

BEB = { b'16[  e''16 b''16]  }
BDB = { b'16[  d''16 b''16]  }
FBF = { fs'16[ b'16  fs''16] }
ADA = { a'16[  d''16 a''16]  }

BEBs = { b''16[  e'''16 b'''16]  }
BDBs = { b''16[  d'''16 b'''16]  }
FBFs = { fs''16[ b''16  fs'''16] }
ADAs = { a''16[  d'''16 a'''16]  }

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 96
      \clef treble
      \key g \major
      \time 4/4
      
      r1 | r1 | r1 | r1 | \break
      
      \repeat volta 2 {
        r8 g'16^1 fs'16^2 g'8^1 b'16^4 c''16 b'2 | r8 fs'16^2 g'16 fs'8 g'16 a'16 g'2 | r8 fs'16^2 e'16 fs'8 b'16^4 c''16 b'2 | r8 fs'16^2 e'16 fs'2. | \break
      }
      
        e''4.          b'8~           b'2        |   d''4.          b'8~           b'2        |   fs''4.          b'8~            b'2         |   fs''4.          a'8~            a'2         | \break
      <<b'4. g''4.>> <<g'8~ e''8~>> <<g'2 e''2>> | <<b'4. g''4.>> <<g'8~ d''8~>> <<g'2 d''2>> | <<b'4. fs''4.>> <<fs'8~ d''8~>> <<fs'2 d''2>> | <<a'4. fs''4.>> <<fs'8~ d''8~>> <<fs'2 d''2>> | \break
      
      \repeat volta 2 {
        \BEB \BEB \BEB \BEB b'16 e''16 c''16 e''16 | \BDB \BDB \BDB \BDB b'16 d''16 a'16 d''16 | \FBF \FBF \FBF \FBF fs'16 b'16 g'16 b'16 | \break
        
        \alternative {
          \volta 1 {
            \ADA \ADA \ADA \ADA a'16 d''16 g'16 d''16 |
          }
          \volta 2 {
            \ADA \ADA \ADA \ADA a'16 d''16 a'16 r16 | \break
          }
        }
      }
      
      \repeat volta 2 {
        r8 g'16^1 fs'16^2 g'8^1 b'16^4 c''16 b'2 | r8 fs'16^2 g'16 fs'8 g'16 a'16 g'2 | r8 fs'16^2 e'16 fs'8 b'16^4 c''16 b'2 | r8 fs'16^2 e'16 fs'2. | \break
      }
      
      \clef "treble^8"
      
        e'''4.           b''8~            b''2         |   d'''4.           b''8~            b''2         |   fs'''4.           b''8~             b''2          |   fs'''4.           a''8~             a''2          | \break
      <<b''4. g'''4.>> <<g''8~ e'''8~>> <<g''2 e'''2>> | <<b''4. g'''4.>> <<g''8~ d'''8~>> <<g''2 d'''2>> | <<b''4. fs'''4.>> <<fs''8~ d'''8~>> <<fs''2 d'''2>> | <<a''4. fs'''4.>> <<fs''8~ d'''8~>> <<fs''2 d'''2>> | \break
      
      \repeat volta 2 {
        \BEBs \BEBs \BEBs \BEBs b''16 e'''16 c'''16 e'''16 | \BDBs \BDBs \BDBs \BDBs b''16 d'''16 a''16 d'''16 | \break
        
        \alternative {
          \volta 1 {
            \FBFs \FBFs \FBFs \FBFs fs''16 b''16 g''16 b''16 | \ADAs \ADAs \ADAs \ADAs a''16 d'''16 g''16 d'''16 | \break
          }
          \volta 2 {
            \FBFs \FBFs \FBFs \FBFs fs''16 b''16 g''16 b''16 | \ADAs \ADAs \ADAs \ADAs a''16 d'''16 g''16 d'''16 | <g'' b'' e'''>1 | \bar "|."
          }
        }
      }
    }
    \new Staff {
      \clef bass
      \key g \major
      \time 4/4
      
      \EmI | \GI | \DsixI | \DI |
      
      \EmI | \GI | \DsixI | \DI |
      \EmI | \GI | \DsixI | \DI |
      \EmI | \GI | \DsixI | \DI |
      
      \EmI | \GI | \DsixI |
      \DI  | <<d8 d'8>> b8 <<fs8 d'8>> b8 <<d8 d'8>> b8 <<fs8 d'8>> a8 |
      
      \EmI | \GI | \DsixI | \DI |
      \EmI | \GI | \DsixI | \DI |
      \EmI | \GI | \DsixI | \DI |
      
      \EmI   | \GI |
      \DsixI | \DI |
      \DsixI | <<d8 d'8>> a8 <<fs8 d'8>> a8 <<d4. d'4.>> r8 | <e b e'>1 |
    }
    \chords {
      
      e1:m | g1   | d1:6 | d1 |
      
      e1:m | g1   | d1:6 | d1 |
      e1:m | g1   | d1:6 | d1 |
      e1:m | g1   | d1:6 | d1 |
      
      e1:m | g1   | d1:6 |
      d1   | d1:6 |
      
      e1:m | g1   | d1:6 | d1 |
      e1:m | g1   | d1:6 | d1 |
      e1:m | g1   | d1:6 | d1 |
      
      e1:m | g1    |
      d1:6 | d1    |
      d1:6 | d2 r2 | r1 |
    }
  >>
  \layout {}
}

\score {
  \new PianoStaff \with {
    instrumentName = "Piano"
  } <<
    \new Staff {
      \tempo 4 = 96
      \clef treble
      \key g \major
      \time 4/4
      
      r1 | r1 | r1 | r1 | \break
      
      r8 g'16^1 fs'16^2 g'8^1 b'16^4 c''16 b'2 | r8 fs'16^2 g'16 fs'8 g'16 a'16 g'2 | r8 fs'16^2 e'16 fs'8 b'16^4 c''16 b'2 | r8 fs'16^2 e'16 fs'2. | \break
      r8 g'16^1 fs'16^2 g'8^1 b'16^4 c''16 b'2 | r8 fs'16^2 g'16 fs'8 g'16 a'16 g'2 | r8 fs'16^2 e'16 fs'8 b'16^4 c''16 b'2 | r8 fs'16^2 e'16 fs'2. | \break
      
        e''4.          b'8~           b'2        |   d''4.          b'8~           b'2        |   fs''4.          b'8~            b'2         |   fs''4.          a'8~            a'2         | \break
      <<b'4. g''4.>> <<g'8~ e''8~>> <<g'2 e''2>> | <<b'4. g''4.>> <<g'8~ d''8~>> <<g'2 d''2>> | <<b'4. fs''4.>> <<fs'8~ d''8~>> <<fs'2 d''2>> | <<a'4. fs''4.>> <<fs'8~ d''8~>> <<fs'2 d''2>> | \break
      
      \BEB \BEB \BEB \BEB b'16 e''16 c''16 e''16 | \BDB \BDB \BDB \BDB b'16 d''16 a'16 d''16 | \FBF \FBF \FBF \FBF fs'16 b'16 g'16 b'16 | \ADA \ADA \ADA \ADA a'16 d''16 g'16 d''16 | \break
      \BEB \BEB \BEB \BEB b'16 e''16 c''16 e''16 | \BDB \BDB \BDB \BDB b'16 d''16 a'16 d''16 | \FBF \FBF \FBF \FBF fs'16 b'16 g'16 b'16 | \ADA \ADA \ADA \ADA a'16 d''16 a'16 r16   | \break
      
      r8 g'16^1 fs'16^2 g'8^1 b'16^4 c''16 b'2 | r8 fs'16^2 g'16 fs'8 g'16 a'16 g'2 | r8 fs'16^2 e'16 fs'8 b'16^4 c''16 b'2 | r8 fs'16^2 e'16 fs'2. | \break
      r8 g'16^1 fs'16^2 g'8^1 b'16^4 c''16 b'2 | r8 fs'16^2 g'16 fs'8 g'16 a'16 g'2 | r8 fs'16^2 e'16 fs'8 b'16^4 c''16 b'2 | r8 fs'16^2 e'16 fs'2. | \break
      
      \clef "treble^8"
      
        e'''4.           b''8~            b''2         |   d'''4.           b''8~            b''2         |   fs'''4.           b''8~             b''2          |   fs'''4.           a''8~             a''2          | \break
      <<b''4. g'''4.>> <<g''8~ e'''8~>> <<g''2 e'''2>> | <<b''4. g'''4.>> <<g''8~ d'''8~>> <<g''2 d'''2>> | <<b''4. fs'''4.>> <<fs''8~ d'''8~>> <<fs''2 d'''2>> | <<a''4. fs'''4.>> <<fs''8~ d'''8~>> <<fs''2 d'''2>> | \break
      
      \BEBs \BEBs \BEBs \BEBs b''16 e'''16 c'''16 e'''16 | \BDBs \BDBs \BDBs \BDBs b''16 d'''16 a''16 d'''16 | \FBFs \FBFs \FBFs \FBFs fs''16 b''16 g''16 b''16 | \ADAs \ADAs \ADAs \ADAs a''16 d'''16 g''16 d'''16 | \break
      \BEBs \BEBs \BEBs \BEBs b''16 e'''16 c'''16 e'''16 | \BDBs \BDBs \BDBs \BDBs b''16 d'''16 a''16 d'''16 | \FBFs \FBFs \FBFs \FBFs fs''16 b''16 g''16 b''16 | \ADAs \ADAs \ADAs \ADAs a''16 d'''16 g''16 d'''16 | <g'' b'' e'''>1 | \bar "|."
    }
    \new Staff {
      \clef bass
      \key g \major
      \time 4/4
      
      \EmI | \GI | \DsixI | \DI |
      
      \EmI | \GI | \DsixI | \DI |
      \EmI | \GI | \DsixI | \DI |
      
      \EmI | \GI | \DsixI | \DI |
      \EmI | \GI | \DsixI | \DI |
      
      \EmI | \GI | \DsixI | \DI |
      \EmI | \GI | \DsixI | <<d8 d'8>> b8 <<fs8 d'8>> b8 <<d8 d'8>> b8 <<fs8 d'8>> a8 |
      
      \EmI | \GI | \DsixI | \DI |
      \EmI | \GI | \DsixI | \DI |
      
      \EmI | \GI | \DsixI | \DI |
      \EmI | \GI | \DsixI | \DI |
      
      \EmI | \GI | \DI    | \DsixI |
      \EmI | \GI | \DsixI | <<d8 d'8>> a8 <<fs8 d'8>> a8 <<d4. d'4.>> r8 | <e b e'>1 |
    }
  >>
  \midi {}
}
