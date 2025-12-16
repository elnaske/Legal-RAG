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

== Prompts

= Results

= Conclusion

#bibliography("bibliography.bib")