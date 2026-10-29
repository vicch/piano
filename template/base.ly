\version "2.24.0"
\language "english"

% ==============================================================================
% SCHEME HELPERS & DYNAMIC TITLE HANDLERS
% ==============================================================================

% Safe font generator for title (handles empty/missing 'title-font' gracefully)
#(define (title-font-override)
   (let ((tf (ly:parser-lookup 'title-font))
         (base `((font-size . 6) (font-series . bold))))
     (if (and (string? tf) (not (string=? tf "")))
         (cons (cons 'font-name tf) base)
         base)))

% Custom markup command to fetch title from either \header { title = ... } or #(define title ...)
#(define-markup-command (format-title layout props) ()
   (let* ((header-title (chain-assoc-get 'header:title props #f))
          (scheme-title (ly:parser-lookup 'title))
          (final-title (cond
                        ((string? header-title) header-title)
                        ((string? scheme-title) scheme-title)
                        (else "")))
          (font-list (title-font-override)))
     (interpret-markup layout props
       (markup #:override font-list final-title))))

% Evaluates total pages for use in the custom footer
#(define total-page-markup 
   (markup (number->string (if (defined? 'total-page) total-page 1))))

% Global staff size setting (20pt)
#(set-global-staff-size 20)


% ==============================================================================
% HEADER DEFAULTS
% ==============================================================================

\header {
  % Automatically pulls global 'source' variable if defined
  tagline = #(if (defined? 'source) source #f)
}


% ==============================================================================
% PAPER & PAGE LAYOUT
% ==============================================================================

\paper {
  #(set-paper-size "letter")

  top-margin    = #20
  bottom-margin = #20
  left-margin   = #16
  right-margin  = #16
  
  system-system-spacing.basic-distance = #16
  system-system-spacing.padding = #4

  last-bottom-spacing.basic-distance = #16
  last-bottom-spacing.padding = #4
  
  indent = #0
  
  scoreTitleMarkup = \markup \fill-line {
    \null "Engraved by vicch"
  }
  
  bookTitleMarkup = \markup {
    \override #'(baseline-skip . 3)
    \column {
      \fill-line {
        \null
        \format-title % Renders the title with your size & font overrides
        \null
      }
      \vspace #2.0
      \fill-line {
        \fromproperty #'header:poet
        \fromproperty #'header:composer
      }
    }
  }

  print-page-number = ##t
  oddHeaderMarkup  = \markup \null
  evenHeaderMarkup = \oddHeaderMarkup
  
  oddFooterMarkup = \markup {
    \fill-line {
      \null
      \null
      \concat {
        \fromproperty #'page:page-number-string
        "/"
        #total-page-markup
      }
    }
  }
  evenFooterMarkup = \oddFooterMarkup
}


% ==============================================================================
% GLOBAL SCORE LAYOUT & CONTEXT OVERRIDES
% ==============================================================================

\layout {
  \context {
    \Score
    barNumberVisibility = #first-bar-number-invisible-save-broken-bars
    
    \override StaffGrouper.staff-staff-spacing.basic-distance = #10
    \override StaffGrouper.staff-staff-spacing.padding = #2
    
    \override Stem.length-fraction = #1
    \override Stem.thickness = #1.5
    \override Beam.damping = #1.2
    
    \override TimeSignature.style = #'numbered
    \override TimeSignature.break-visibility = #end-of-line-invisible
    \override SectionLabel.font-size = #-2
  }

  \context {
    \Staff
    ottavationMarkups = #ottavation-ordinals
    explicitKeySignatureVisibility = #end-of-line-invisible
  }

  \context {
    \Voice
    \override Fingering.font-size = #-6
    \override Fingering.font-series = #'medium
  }

  \context {
    \ChordNames
    \override ChordName.font-family = #'roman
    \override ChordName.font-size = #-2
    noChordSymbol = #""
  }
}


% ==============================================================================
% MIDI EXPORT SETTINGS
% ==============================================================================

\midi {
  \context {
    \ChordNames
    \remove "Note_performer"
  }
}


% ==============================================================================
% REUSABLE SHORTCUTS & MACROS
% ==============================================================================

A = \sectionLabel \markup { \box "A" }
B = \sectionLabel \markup { \box "B" }
C = \sectionLabel \markup { \box "C" }
D = \sectionLabel \markup { \box "D" }
E = \sectionLabel \markup { \box "E" }

var = _\markup { "*" }