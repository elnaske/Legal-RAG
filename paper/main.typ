// Example ACL paper using the Typst template
// Compile with: typst compile example.typ

#import "acl.typ": *

#show: acl-paper.with(
  title: [Legal-RAG: Multi-Agent Legal Reasoning with RAG],
  
  // Set mode to "review" for anonymous submission with line numbers,
  // "final" for camera-ready, or "preprint" for non-anonymous with page numbers
  mode: "preprint",
  
  // Authors (hidden in review mode)
  authors: (
    (
      name: "Benjamin Glidden, Shusuke Hashimoto, Armando Hull, Elias Naske",
      affiliation: "Indiana University Bloomington",
    ),
  ),
  
  abstract: [
    #lorem(50)
  ],
)

= Introduction
The American legal system follows common law, that is, judicial decisions are, to a large degree, based by precedents set by previous rulings. 
In preparation for a case, lawyers have to do extensive research on these previous rulings to support their arguments. 
This involves a lot of manual work. 
Our work uses LLM agents in conjunction with RAG to aid this process: 
The user prompts the system with a legal inquiry, which is then discussed by two agents, representing opposing lawyers in court (such as prosecution/defense in criminal cases). 
These lawyer-agents support their arguments through RAG, by querying a vector database made up of a case law corpus. 
After a few turns, the discussion ends and the conversation is summarized by another LLM. 
That way, the final answer not only provides relevant case law, but also considers how the other side might try counter it.

= Data
== Extraction

== Preprocessing

= Agents
== Infrastructure

== Case Selection and Analysis
Three Supreme Court criminal cases were selected to represent diverse legal domains: 
Samia v. United States (2023) addressing Confrontation Clause issues, Betterman v. Montana (2016) concerning Sixth Amendment speedy trial rights, and Glossip v. Oklahoma (2024) involving death penalty procedures and prosecutorial misconduct. 
Oral argument transcripts from these cases were systematically analyzed to identify recurring patterns in advocate behavior, judicial intervention styles, citation formats, cross-examination techniques, and objection handling protocols. 
This analysis revealed distinct strategic priorities employed by prosecution and defense counsel, with prosecution consistently leading with strongest evidence and framing issues narrowly, while defense led with constitutional violations and framed issues broadly to expand protective precedents.

== Prompt Architecture
The initial prompt development phase produced structured prompts for three primary agent roles: prosecution, defense, and judge. 
Each agent prompt contained role definitions specifying primary objectives, strategic priorities derived from Supreme Court transcript analysis, a four-phase argumentation structure covering opening statements through closing arguments, case law citation requirements with triggers for requesting legal research, objection protocols specifying proper format and grounds, and ethical constraints reflecting professional responsibility rules. 
Strategic priorities were deliberately grounded in observed advocate behavior rather than theoretical legal strategy, ensuring realistic courtroom argumentation patterns.

Supporting protocols were developed to govern multi-agent interaction, including a turn-taking protocol establishing structured courtroom procedure, a RAG Integration Protocol defining a seven-step process for handling agent-generated search requests, response format guidelines providing structural templates, citation format examples demonstrating proper legal citation styles, and an error recovery protocol providing coordinator intervention procedures. 
Quality checklists were developed for each agent role with pre-submission verification points and red flag warnings for common errors.

== RAG Integration Design

== Implementation and Verification
= Results

= Conclusion

#bibliography("bibliography.bib")
