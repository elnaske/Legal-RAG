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
To properly implement our Rag-based system, it goes without saying that one of the most imperative items for Legal-RAG was to extract proper data. In RAG, retrieval is achieved by calculating the similarity
(e.g. cosine similarity) between the embeddings of the question and document chunks, where the semantic representation
capability of embedding models plays a key role @Gao2023-jq. With this, given the goals of Legal-RAG, documents representative of related case law were necessary for proper retrieval. For our datasource, we went with the open source project by the Free Law Project, CourtListener @FreeLawProject_CourtListener_2025. CourtListener is a free legal research that conatains millions of real legal opinions and cases. All of these cases are available for public reserach through their site and free REST API. Therefore, for Legal-RAG's use case, accessing the legal opinions and their related case data through their REST API provided a clear path forward for generating proper documents for chunking.

While the millions of records from CourtListener would be the source of data, further data extraction was necessary. One notable aspect of how data is pulled from CourtListener is in how their data is organized. CourtListener provides data in heirarchical structure, all represented in .json format. Clusters of opinions related to one case are represented as one cluster record, with child relationships to the various opinion .json records. Firstly, we needed a scheme to organize the data so that the agents would only query the opinions for accurate similarity in retrieval. To achieve this, we parsed out and saved the sub-opinions separately from the cluster records.  


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
A critical design decision involved enabling agents to generate their own search queries rather than relying solely on user input. 
The prompts instruct agents to generate queries in the format "[SEARCH: legal doctrine + key facts + jurisdiction]" when they need legal authority. 
Agent-generated queries are optimized for the specific legal issue being argued at the moment authority is needed, contain relevant legal terminology drawn from the agent's knowledge, and support iterative research as arguments develop. 
Example queries were embedded within prompts to teach appropriate specificity, such as "[SEARCH: fourth amendment warrantless search exigent circumstances]" demonstrating the inclusion of constitutional doctrine, procedural context, and relevant exception.

The RAG loop implementation uses pattern matching to detect search requests within agent responses. 
When an agent outputs text containing "[SEARCH: query text]", the system extracts the query string, pauses the agent's turn, queries the vector database with the extracted query, formats retrieved results according to the RAG Integration Protocol presenting case names, holdings, and relevance explanations, and continues the agent's turn by providing formatted results within the conversation context. 
The agent then incorporates retrieved case law into its argument using proper citation format, with the process repeating up to a configurable maximum number of iterations to prevent infinite loops.

The RAG loop architecture was implemented using a base class pattern where shared methods handle query extraction via regular expression pattern matching, vector store querying, result formatting per protocol specifications, and RAG loop processing coordinating the entire retrieval and continuation cycle. 
The core processing method queries the vector store with the user's original question for initial context, generates the agent's initial response, then enters a loop that continues until no search requests are detected. 
Within each iteration, the method extracts search queries from the agent's response, queries the vector store using the agent's query rather than the user's question, formats results, constructs a continuation prompt providing results and requesting argument continuation, and invokes the language model to generate the continuation. 
This approach ensures agents maintain conversation context throughout retrieval, building arguments iteratively with progressively refined case law research.

== Implementation and Verification
The prompts were implemented as a Python module with getter functions for each component and as a YAML version for version control and collaborative editing. 
A comprehensive test suite validated that all agent prompts contained proper role definitions, strategic priorities from Supreme Court analysis were present, key legal doctrines appeared in appropriate prompts, search request format was properly documented, quality checklists contained role-specific validation points, and all protocols were complete and properly formatted. 
The test suite achieved full coverage with all tests passing.

The final prompt system produced eleven distinct components: three agent prompts, three quality checklists, and five supporting protocols. 
These enable Supreme Court-derived argumentation strategies, integrated RAG support with agent-generated queries, role-specific quality control mechanisms, ethical constraints, structured turn-taking and objection handling, and consistent response formatting. 
The modular architecture supports various usage patterns from single-agent deployment to complete multi-agent courtroom simulation, with each component capable of independent use, testing, and version control.

= Results

= Conclusion

#bibliography("bibliography.bib")
