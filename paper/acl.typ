// ACL Conference Template for Typst
// Based on the official ACL LaTeX style files
// https://github.com/acl-org/acl-style-files/

// ============================================================================
// TEMPLATE CONFIGURATION
// ============================================================================

#let acl-paper(
  // Paper metadata
  title: none,
  authors: (),  // Array of author dictionaries: (name: "", affiliation: "", email: "")
  abstract: none,
  
  // Paper mode: "review", "final", or "preprint"
  mode: "review",
  
  // Document body
  body,
) = {
  // ============================================================================
  // MODE SETTINGS
  // ============================================================================
  
  let is-review = mode == "review"
  let is-final = mode == "final"
  let is-preprint = mode == "preprint"
  
  let show-authors = not is-review
  let show-page-numbers = is-review or is-preprint
  
  // ============================================================================
  // DOCUMENT SETUP
  // ============================================================================
  
  set document(
    title: if title != none { title } else { "" },
  )
  
  // ============================================================================
  // PAGE SETUP - A4 paper with 2.5cm margins
  // ============================================================================
  
  set page(
    paper: "us-letter",
    margin: (
      top: 2.54cm,
      bottom: 2.54cm,
      left: 2.54cm,
      right: 2.54cm,
    ),
    numbering: if show-page-numbers { "1" } else { none },
  )
  
  // ============================================================================
  // FONT SETUP - Times New Roman, 10pt body
  // ============================================================================
  
  set text(
    // font: "Times New Roman",
    size: 11pt,
    lang: "en",
  )
  
  // Line spacing
  set par(
    leading: 0.55em,
    first-line-indent: 1em,
    justify: true,
    spacing: 1.5em,
  )
  
  // ============================================================================
  // HEADING STYLES
  // ============================================================================
  
  set heading(numbering: "1.1")
  
  show heading.where(level: 1): it => {
    set text(size: 12pt, weight: "bold")
    set par(first-line-indent: 0pt)
    v(1.5em, weak: true)
    block(below: 0.8em)[
      #if it.numbering != none {
        counter(heading).display()
        h(0.5em)
      }
      #it.body
    ]
  }
  
  show heading.where(level: 2): it => {
    set text(size: 11pt, weight: "bold")
    set par(first-line-indent: 0pt)
    v(1.2em, weak: true)
    block(below: 0.6em)[
      #if it.numbering != none {
        counter(heading).display()
        h(0.5em)
      }
      #it.body
    ]
  }
  
  show heading.where(level: 3): it => {
    set text(size: 10pt, weight: "bold")
    set par(first-line-indent: 0pt)
    v(1.0em, weak: true)
    block(below: 0.5em)[
      #if it.numbering != none {
        counter(heading).display()
        h(0.5em)
      }
      #it.body
    ]
  }
  
  // ============================================================================
  // LINKS AND REFERENCES
  // ============================================================================
  
  let dark-blue = rgb(0%, 0%, 50%)
  show link: set text(fill: dark-blue)
  show ref: set text(fill: dark-blue)
  
  // ============================================================================
  // FIGURES AND TABLES
  // ============================================================================
  
  show figure.caption: it => {
    set text(size: 10pt)
    set par(first-line-indent: 0pt)
    it
  }
  
  set table(
    stroke: none,
    inset: 5pt,
  )
  
  // ============================================================================
  // FOOTNOTES
  // ============================================================================
  
  set footnote.entry(
    separator: line(length: 5em, stroke: 0.5pt),
    gap: 0.65em,
  )
  
  // ============================================================================
  // EQUATIONS
  // ============================================================================
  
  set math.equation(numbering: "(1)")
  
  // ============================================================================
  // LISTS
  // ============================================================================
  
  set enum(
    indent: 2em,
    body-indent: 0.5em,
    spacing: auto,
  )
  
  set list(
    indent: 2em,
    body-indent: 0.5em,
    spacing: auto,
  )
  
  // ============================================================================
  // RAW/CODE BLOCKS
  // ============================================================================
  
  show raw: set text(
    // font: ("Courier New", "Courier", "monospace"),
    size: 9pt,
  )
  
  // ============================================================================
  // TITLE BLOCK (single column, centered)
  // ============================================================================
  
  align(center)[
    #v(0.1in)
    #text(size: 15pt, weight: "bold")[#title]
    #v(0.25in)
    
    // Author block
    #if show-authors [
      #set text(size: 11pt)
      #set par(first-line-indent: 0pt, leading: 0.5em)
      #for author in authors [
        #strong(author.name) \
        #if "affiliation" in author and author.affiliation != none [
          #author.affiliation \
        ]
        #if "email" in author and author.email != none [
          #text(fill: dark-blue)[#author.email]
        ]
        #v(0.05in)
        #datetime(year: 2025, month: 12, day: 18).display()
        #v(0.15in)
      ]
    ] else [
      #text(size: 11pt, weight: "bold")[Anonymous ACL submission]
      #v(0.2in)
    ]
  ]
  
  // ============================================================================
  // MAIN BODY (two columns)
  // ============================================================================
  
  columns(2, gutter: 0.6cm)[
    // Abstract as first section within columns
    #if abstract != none {
      align(center)[
        #text(size: 12pt, weight: "bold")[Abstract]
      ]
      v(0.5em)
      pad(left: 0.6cm, right: 0.6cm)[
        #set par(first-line-indent: 0pt, justify: true)
        #abstract
      ]
      v(0.8em)
    }
    
    #body
  ]
}

// ============================================================================
// APPENDIX COMMAND
// ============================================================================

#let appendix() = {
  counter(heading).update(0)
  set heading(numbering: "A.1")
}

// ============================================================================
// SPECIAL SECTIONS
// ============================================================================

#let acknowledgments(body) = {
  heading(level: 1, numbering: none)[Acknowledgments]
  body
}

#let limitations(body) = {
  heading(level: 1, numbering: none)[Limitations]
  body
}

#let ethics-statement(body) = {
  heading(level: 1, numbering: none)[Ethics Statement]
  body
}

// ============================================================================
// CITATION HELPERS
// ============================================================================

#let citet(key) = {
  cite(key, form: "prose")
}

#let citep(key) = {
  cite(key, form: "normal")
}

#let citeyear(key) = {
  cite(key, form: "year")
}

// ============================================================================
// BLOCK QUOTE ENVIRONMENT
// ============================================================================

#let blockquote(body) = {
  pad(left: 1em, right: 1em)[
    #set par(first-line-indent: 0pt)
    #body
  ]
}
