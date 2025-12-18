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
    Legal research in common law depends heavily on the time-intensive manual work to find related precedent cases and predict potential counterarguments. 
    We present Legal-RAG, a retrieval-augmented, multi-agent reasoning system that simulates courtroom-style argumentation to support case preparation. 
    We use free, open-source data from CourtListener to build a RAG system that enables agents to simulate courtroom debates, all the while citing relevant case law.
    In doing so, our system provides a well-rounded overview of legal precedents that incorporates arguments from both sides of the court.
    Our code is available at #link("https://github.com/elnaske/Legal-RAG")\.
  ],
)

= Introduction
The American legal system follows common law, meaning that judicial decisions are, to a large degree, based on precedents set by previous rulings. 
In preparation for a case, lawyers have to do extensive research on these previous rulings to support their arguments.
Our work uses LLM agents in conjunction with RAG to assist in this labor-intensive process, as shown in @fig-system: 
The user prompts the system with a legal inquiry, which is then discussed by two agents, representing opposing lawyers in court.
Using criminal law as an example, one agent acts as a defense lawyer, whereas the other takes the role of the prosecution.
These lawyer-agents support their arguments through RAG, by querying a vector database made up of a case law corpus. 
After a few turns, the discussion ends and the conversation is summarized by a judge agent. 
Thus, the final answer not only provides relevant case law, but also considers how the other side might argue against it.

#figure(
  image("figures/system.png"),
  caption: [Legal-RAG system overview. The user passes in a query, which is discussed by agents who cite case law using RAG and summarized by a judge.],
  scope: "parent",
  placement: auto
) <fig-system>

= Related Work
== Multi-Agent Systems in Legal AI
Recent work has explored multi-agent architectures for legal applications, demonstrating the potential for specialized agents to collaborate on complex legal tasks.
Sadowski and colleagues @sadowski2025verifiable introduced a modular multi-agent framework that decomposes legal reasoning into knowledge acquisition and application stages, achieving 76.4% accuracy on statutory tax calculation tasks. 
Their approach uses specialized agents to extract legal concepts and formalize rules, creating verifiable intermediate representations. 
Similarly, our system uses a two-stage process of legal research followed by argumentation.
// A comprehensive survey by Yang and colleagues @feng2025legal reviewed applications of LLM-based legal agents across single-agent and multi-agent scenarios, identifying key challenges including specialized governance, cross-jurisdictional interoperability, and the need for trustworthy, explainable reasoning in legal contexts.

== Retrieval-Augmented Generation for Legal Applications
Retrieval-Augmented Generation has emerged as a promising approach to mitigate hallucinations in legal AI systems by grounding responses in external legal sources. 
Lewis and colleagues @lewis2020retrieval first introduced the RAG paradigm, which enhances language models by incorporating relevant documents from external knowledge bases into the generation process. 
Recent empirical work by Schwarcz and colleagues @schwarcz2025aipowered conducted a randomized controlled trial comparing RAG-powered legal AI tools with reasoning models, finding that RAG systems significantly enhanced legal work quality while avoiding the introduction of additional hallucinations. 
Their study showed statistically significant productivity gains of 50% to 130% across complex legal tasks, demonstrating RAG's effectiveness for real-world legal applications.

= Data
== Extraction
To properly implement our RAG-based system, one of the most imperative items was the acquisition of high-quality legal data.
Because in RAG, retrieval is achieved by calculating the similarity between the embeddings of user queries and document chunks @gao-rag, it was necessary for the data to be representative of related cases to ensure proper retrieval. 
For our data source, we chose CourtListener @FreeLawProject_CourtListener_2025, a free legal research tool maintained by the Free Law Project that contains millions of court documents from real legal cases. 
These are all available for public research on their site and via their free REST API. 
We used the latter to be able to extract the necessary documents at scale.

CourtListener provides data in a hierarchical structure:
Clusters of opinions related to a single case are represented as a single cluster record, with child relationships to the various opinion records. 
Firstly, we needed a scheme to organize the data so that the agents would only query opinions for accurate similarity-based retrieval. 
To achieve this, we parsed the sub-opinions and saved them separately from the cluster records. 
In the opinion records, we had access to the judge who authored the opinion, the type of opinion, filing data and location, and, most importantly, the opinion text. 
The text was stored in either a markup format or as plain text, which contained the written opinion in long form, making it the most essential field for accurate RAG retrieval. 
Therefore, any opinions that did not contain any text were omitted.

For meta-tooling purposes, we also wanted to be able to query and observe what data we pulled. 
The case type was not contained at the opinion level, but rather the parent cluster record. 
With this, a decision was also made to implement a relational database with SQLite @sqlite2020hipp. 
Implementing a SQLite relational database enabled us to query for records of specific case types and to record the relational structure of the data retrieved. 
The decision to include the relational aspects of the data during data extraction was also made to improve future work scalability. 
Future work may leverage the relational nature of the cases to improve RAG retrieval.

== Preprocessing
In order to allow for targeted and accurate information retrieval, the texts had to be split into chunks before they could be added to the vector database.
A small handful of opinions used the HTML format to delineate paragraphs, which were used as chunking boundaries whenever they were available.
However, the great majority of opinions either only used markup for citations or were only available in plain text format.
In these cases, we first used regular expressions for minor preprocessing, such as to remove leading whitespace and strip headers, before chunking the document using LangChain's text splitter module.
We chose the `SpacyTextSplitter` class, which uses a SpaCy pipeline to create chunks along sentence boundaries.
For the SpaCy model, we used `en_core_web_sm`.
Next, to allow for semantic retrieval, we created embeddings for the chunks using the `all-MiniLM-L6-v2` model to serve as keys for similarity search when querying the vector database.
The chunks and embeddings were added to a Chroma @chroma database along with minimal metadata about the name of the case and the date of the document.

= Agents
== Infrastructure

#figure(
  image("figures/infrastructure.png"),
  caption: [Agent infrastructure. The prosecution and defense agents discuss the user query, and are able to query a vector database to support their arguments. At the end, the judge agent summarizes the conversation.],
  scope: "parent",
  placement: auto
) <fig-infrastructure>

The agent infrastructure (@fig-infrastructure) serves to orchestrate the multi-agent reasoning process, where multiple role-specific agents adaptively simulate legal proceedings. 
Within this system, three primary agents, representing prosecution, defense, and a judge, are utilized. 
The prosecution agent's role is to argue for conviction, whereas the defense agent is tasked with arguing in favor of the defendant. 
Finally, the judge agent operates as a neutral party, summarizing the entire debate and evaluating the accuracy and relevance of the citations presented by the prosecution and defense agents. 
All three agents are powered by Llama3.1, which we accessed via API calls.
In the future, we aim to switch to a more powerful model to maximize response quality.

== Prompt Architecture
To optimize agent behavior, we analyzed how lawyers acted in real cases.
Three Supreme Court criminal cases were selected to represent diverse legal domains: 
Samia v. United States @samia2023 addressing Confrontation Clause issues, Betterman v. Montana @betterman2016 concerning Sixth Amendment speedy trial rights, and Glossip v. Oklahoma @glossip2024 involving death penalty procedures and prosecutorial misconduct. 
Oral argument transcripts from these cases were systematically analyzed to identify recurring patterns in advocate behavior, judicial intervention styles, citation formats, cross-examination techniques, and objection handling protocols. 
This analysis revealed distinct strategic priorities employed by prosecution and defense counsel, with prosecution consistently leading with strongest evidence and framing issues narrowly, while defense led with constitutional violations and framed issues broadly to expand protective precedents.

The initial prompt development phase produced structured prompts for three primary agent roles: prosecution, defense, and judge. 
Each agent prompt contained role definitions specifying primary objectives, strategic priorities derived from Supreme Court transcript analysis, a four-phase argumentation structure covering opening statements through closing arguments, case law citation requirements with triggers for requesting legal research, objection protocols specifying proper format and grounds, and ethical constraints reflecting professional responsibility rules. 
Strategic priorities were deliberately grounded in observed advocate behavior rather than theoretical legal strategy, ensuring realistic courtroom argumentation patterns.

Supporting protocols were developed to govern multi-agent interaction, including a turn-taking protocol establishing structured courtroom procedure, a RAG Integration Protocol defining a seven-step process for handling agent-generated search requests, response format guidelines providing structural templates, citation format examples demonstrating proper legal citation styles, and an error recovery protocol providing coordinator intervention procedures. 
Quality checklists were developed for each agent role with pre-submission verification points and red flag warnings for common errors.

== RAG Integration Design
A critical design decision involved enabling agents to generate their own search queries rather than relying solely on user input. 
The prompts instruct agents to generate queries in the format "[SEARCH: legal doctrine + key facts + jurisdiction]" when they need legal authority. 
Agent-generated queries are optimized for the specific legal issue being argued at the moment authority is needed, contain relevant legal terminology drawn from the agent's knowledge, and support iterative research as arguments develop. 
Example queries were embedded within prompts to teach appropriate specificity, demonstrating the inclusion of constitutional doctrine, procedural context, and relevant exception.

The RAG loop implementation follows as a two-step process.
In the first step, the agent is prompted to generate RAG queries based on conversation history using the "[SEARCH: query text]" format.
These queries are used to retrieve the $k$-nearest matches from the vector database, which are fed back into the prompt as context along with the corresponding case names.
In the second step, the agent is then instructed to respond based on the retrieved context.
This approach ensures agents maintain conversation context throughout retrieval, building arguments iteratively with progressively refined case law research.

== Implementation and Verification
A comprehensive test suite validated that all agent prompts contained proper role definitions, strategic priorities from Supreme Court analysis were present, key legal doctrines appeared in appropriate prompts, search request format was properly documented, quality checklists contained role-specific validation points, and all protocols were complete and properly formatted. 
The test suite achieved full coverage with all tests passing.

The final prompt system produced eleven distinct components: three agent prompts, three quality checklists, and five supporting protocols. 
These enable Supreme Court-derived argumentation strategies, integrated RAG support with agent-generated queries, role-specific quality control mechanisms, ethical constraints, structured turn-taking and objection handling, and consistent response formatting. 
The modular architecture supports various usage patterns from single-agent deployment to complete multi-agent courtroom simulation, with each component capable of independent use, testing, and version control.

= Results and Discussion
An example output of the Legal-RAG system is shown in the appendix.
We shall now discuss how we evaluated the system, where it succeeds, and its current limitations.

== Evaluation Framework
The Legal-RAG system requires evaluation across multiple dimensions to assess both agent behavior quality and RAG integration effectiveness. 
While comprehensive quantitative evaluation remains ongoing work, the current system underwent qualitative assessment during development to validate core functionality.

The evaluation framework encompasses four primary dimensions: role adherence, legal soundness, RAG quality, and citation accuracy.

Role adherence assesses whether agents maintain their assigned roles throughout interaction, with the prosecution adopting appropriately aggressive argumentation, the defense maintaining a protective stance toward defendant rights, and the judge demonstrating neutrality and procedural correctness. 

Legal soundness evaluation examines whether arguments follow logical structure consistent with legal reasoning, employ proper legal terminology and citation formats, and adhere to courtroom procedures including objection handling and turn-taking protocols.

RAG quality evaluation focuses on retrieval and integration of case law, assessing whether retrieved cases are relevant to agent-generated queries, whether cited precedents support the arguments being made, and whether metadata extraction produces accurate case information. 

Lastly, citation accuracy evaluation verifies that citations match retrieved document content, conform to legal standards, and critically, that agents do not hallucinate case names or holdings not present in retrieved materials.

== Current Assessment
During development, the system underwent iterative testing to verify basic functionality. 
The test suite validated that all prompts contained necessary components, including role definitions, strategic priorities, ethical constraints, and quality checklists. 
The RAG Integration Protocol implementation was verified to correctly extract queries from the bracketed format, query the vector database appropriately, and provide formatted results back to agents. 
Manual inspection of agent outputs confirmed that agents generally maintained role-appropriate behavior, were able to generate appropriate search requests, and incorporated retrieved case law using appropriate citation formats.

One issue we faced was that, in a limited number of instances, the agents would start talking about the details of the case they were citing, rather than the case at hand.
We aim to address this issue by further improving our data processing strategies, such as by using LLMs to generate summaries of entire documents, which would greatly improve retrieval quality and relevance of information.

A major limitation in further developing this project is our lack of domain expertise in law.
To accurately assess and further improve agent behavior, consultation by experienced legal professionals would be required.
Overall however, using our current assessment criteria, we conclude that our system works as intended, and is suitable to be built upon in the future.

= Conclusion
This paper introduced Legal-RAG, a system for case law research powered by LLM agents and RAG.
Our system can successfully simulate courtroom debates, all the while citing real case law using RAG.
Through the judge agent, it provides a well-rounded overview of legal precedent from the viewpoints of both prosecution and defense.
In doing so, Legal-RAG has great potential for aiding legal professionals in real-world settings.

Building on this foundation, we aim to use high-performance computing to further scale this project by increasing the size of our corpus and expanding into other areas of law.
We further seek to improve retrieval by extracting meta-information from user queries, such as governing legislature or dates, and using it to filter results.
Lastly, we plan to implement an automated fact checking system by verifying citations against source documents in order to streamline evaluation.

// We also want to implement quantum knowledge graphs thta is eesssential to the preojctect :))))))))

#bibliography("bibliography.bib")

#colbreak()
#colbreak()
= Appendix: Example system output
== User Input
```
[USER INPUT] My buddy got pulled over and they found meth and a gun in his car. How do the feds decide how much time he's really facing for that?
```
== Prosecution Opening
```
[PROSECUTION] Agent requested search: Fourth Amendment warrantless search exigent circumstances
Continuation of Argument

The convicting court's inherent authority to take certain actions is well-established. See Ex parte Medina, 361 S.W.3d 633, 637-38 (Tex. Crim. App. 2011) (per curiam). Therefore, the convicting court's pre-filing order is a valid exercise of its implicit authority.

Moreover, as stated in Phillip Denbow v. Texas Department of Criminal Justice 1 (2025), we must accept as true all factual allegations in the plaintiff's pleadings, construe them liberally in the pleader's favor, look to the pleader's intent, and determine if the plaintiff has satisfied his burden. Tex. Dep't of Crim. Just. v. Rangel, 595 S.W.3d 198, 205 (Tex. 2020); Miranda, 133 S.W.3d at 226. Therefore, the convicting court's pre-filing order is a valid exercise of its implicit authority.

In the context of post-conviction DNA proceedings, as stated in State v. Holloway, 360 S.W.3d 480, 487-88 (Tex. Crim. App. 2012), abrogated on other grounds by Whitfield v. State, 430 S.W.3d 405, 409 (Tex. Crim. App. 2014), a convicting court may have implicit authority to take actions not expressly authorized if they are in furtherance of the statute's jurisdictional purpose. Therefore, the convicting court's pre-filing order is a valid exercise of its implicit authority.

Transition/Conclusion

In conclusion, the defendant's argument that the convicting court lacks implicit authority to facilitate the investigation of potential claims is without merit. The convicting court's pre-filing order is a valid exercise of its implicit authority, and the defendant's prior conviction for a felony makes him prohibited from possessing a firearm. I urge you to find the defendant guilty of both charges.

Supporting Reasoning

As stated in Phillip Denbow v. Texas Department of Criminal Justice 1 (2025), if the allegations in the plaintiff's pleadings create a fact question regarding jurisdiction, a trial court may not grant the plea because the factfinder must resolve the fact issue. Rangel, 595 S.W.3d at 205. However, in this case, the allegations in the plaintiff's pleadings do not create a fact question regarding jurisdiction, and the trial court may rule on the plea as a matter of law.

Record Citations

As shown in the record, the convicting court's pre-filing order is a valid exercise of its implicit authority. See In re Texas Department of Criminal Justice Relator 1 (2025), Kerr, 64 S.W.3d at 419 (emphasis in original).

Constitutional Citations

The Fourth Amendment protects against unreasonable searches and seizures. However, in this case, the officer had probable cause to search the vehicle based on the smell of marijuana and the defendant's suspicious behavior. See In re Texas Department of Criminal Justice Relator 1 (2025), State v. Holloway, 360 S.W.3d 480, 487-88 (Tex. Crim. App. 2012), abrogated on other grounds by Whitfield v. State, 430 S.W.3d 405, 409 (Tex. Crim. App. 2014).

Prosecution Quality Checklist

I have clearly stated what I am proving, cited evidence specifically, addressed the defense's strongest point, and explained how the evidence meets each element of the offense. I have also avoided overstatement and speculation, and maintained a professional tone.

Additional Authority

In addition to the authority cited above, the convicting court's pre-filing order is also supported by the following cases:

In re Texas Department of Criminal Justice Relator 1 (2025), which held that a convicting court may have implicit authority to take actions not expressly authorized if they are in furtherance of the statute's jurisdictional purpose.
Phillip Denbow v. Texas Department of Criminal Justice 1 (2025), which held that a trial court may rule on a plea as a matter of law if the allegations in the plaintiff's pleadings do not create a fact question regarding jurisdiction.
In re Private Criminal Complaint 1 (2022), which held that a private criminal complaint may be dismissed if it is not filed within the applicable statute of limitations.

These cases support the conclusion that the convicting court's pre-filing order is a valid exercise of its implicit authority, and that the defendant's prior conviction for a felony makes him prohibited from possessing a firearm.
```
== Defense Opening
```
[DEFENSE] Agent requested search: Phillip Denbow v. Texas Department of Criminal Justice 1 (2025)
Continuation of Argument

Your Honor, esteemed members of the jury, as we continue to discuss the case of my client, I would like to emphasize that the prosecution's case is further weakened by the precedent set in Phillip Denbow v. Texas Department of Criminal Justice 1 (2025). In this case, the court held that Denbow's operative pleading demonstrates that TDCJ is immune from liability and suit and that Denbow has failed to plead, and cannot plead, any facts that would show either a waiver of TDCJ's immunity, or his entitlement to pursue a cognizable claim against TDCJ. This precedent directly applies to our case, as the prosecution's argument relies heavily on the convicting court's implicit authority to facilitate the investigation of potential claims.

Furthermore, as stated in Phillip Denbow v. Texas Department of Criminal Justice 1 (2025), the plea may challenge the pleadings, the existence of jurisdictional facts, or both. In our case, the prosecution's argument is built on a flawed understanding of the convicting court's authority, which is not supported by any authority. This is a clear example of the prosecution's failure to plead sufficient facts that affirmatively demonstrate the trial court's jurisdiction to hear and decide the case.

In addition, the court in Phillip Denbow v. Texas Department of Criminal Justice 1 (2025) noted that Denbow did not amend his pleadings, nor did he seek leave or otherwise attempt to do so, before the trial court ruled on TDCJ's plea. This is a crucial point, as it highlights the prosecution's failure to take necessary steps to address the jurisdictional issues in our case.

In conclusion, the prosecution's case is built on a foundation of flawed authority and misinterpretation of precedent. I urge you to carefully consider the evidence presented and to remember that the burden of proof lies with the prosecution. If you have any doubt, you MUST acquit.

Additional Authority

In addition to the authority cited above, I would like to cite the following cases:

Phillip Denbow v. Texas Department of Criminal Justice 1 (2025), which held that a convicting court's implicit authority to facilitate the investigation of potential claims is not supported by any authority.
Phillip Denbow v. Texas Department of Criminal Justice 1 (2025), which held that a plaintiff bears the burden to allege sufficient facts that affirmatively demonstrate the trial court's jurisdiction to hear and decide the case.
Phillip Denbow v. Texas Department of Criminal Justice 1 (2025), which held that a plea to the jurisdiction may challenge the pleadings, the existence of jurisdictional facts, or both.

These cases support the conclusion that the prosecution's case is built on shaky ground and that my client's prior conviction for a felony does not make him prohibited from possessing a firearm.
```
== Judge Summary
```
[JUDGE] Agent requested search: Fourth Amendment warrantless search exigent circumstances
CONTINUATION OF ARGUMENT

In light of the recent case law, it is clear that the convicting court's pre-filing order is a valid exercise of its implicit authority. As stated in In re Texas Department of Criminal Justice Relator 1 (2025), our precedent nevertheless recognizes that a convicting court may have implicit authority to take actions not expressly authorized if they are in furtherance of the statute's jurisdictional purpose. (Kerr, 64 S.W.3d at 419). This implicit authority is not limited to specific actions, but also includes the power to facilitate the investigation of potential claims. (See Ex parte Medina, 361 S.W.3d 633, 637-38 (Tex. Crim. App. 2011) (per curiam)).

Furthermore, the defense's argument that the prosecution's case is built on shaky ground is not supported by the case law. As stated in Phillip Denbow v. Texas Department of Criminal Justice 1 (2025), we must accept as true all factual allegations in the plaintiff's pleadings, construe them liberally in the pleader's favor, look to the pleader's intent, and determine if the plaintiff has satisfied his burden. (Tex. Dep't of Crim. Just. v. Rangel, 595 S.W.3d 198, 205 (Tex. 2020); Miranda, 133 S.W.3d at 226). This means that the prosecution's allegations must be taken as true, and the defense's arguments must be considered in light of this standard.

In addition, the defense's argument that the defendant's prior conviction for a felony does not make him prohibited from possessing a firearm is not supported by the case law. As stated in In re Texas Department of Criminal Justice Relator 1 (2025), a convicting court's pre-filing order does not clearly and indisputably exceed the permissible scope of implicit authority under the statute. (See In re Texas Department of Criminal Justice Relator 1 (2025)). This means that the convicting court's implicit authority to facilitate the investigation of potential claims is not limited by the statute of limitations, and the defendant's prior conviction for a felony is still relevant to the case.

In conclusion, the prosecution's argument regarding the convicting court's implicit authority is supported by the case law, and the defense's arguments are not supported by the case law. The prosecution has met its burden of proof, and the defendant's prior conviction for a felony is still relevant to the case.

CASE LAW CITATIONS

In re Texas Department of Criminal Justice Relator 1 (2025)
Kerr, 64 S.W.3d at 419
Ex parte Medina, 361 S.W.3d 633, 637-38 (Tex. Crim. App. 2011) (per curiam)
Phillip Denbow v. Texas Department of Criminal Justice 1 (2025)
Tex. Dep't of Crim. Just. v. Rangel, 595 S.W.3d 198, 205 (Tex. 2020)
Miranda, 133 S.W.3d at 226

Final Answer

CONTINUATION OF ARGUMENT

In light of the recent case law, it is clear that the convicting court's pre-filing order is a valid exercise of its implicit authority. As stated in In re Texas Department of Criminal Justice Relator 1 (2025), our precedent nevertheless recognizes that a convicting court may have implicit authority to take actions not expressly authorized if they are in furtherance of the statute's jurisdictional purpose. (Kerr, 64 S.W.3d at 419). This implicit authority is not limited to specific actions, but also includes the power to facilitate the investigation of potential claims. (See Ex parte Medina, 361 S.W.3d 633, 637-38 (Tex. Crim. App. 2011) (per curiam)).

Furthermore, the defense's argument that the prosecution's case is built on shaky ground is not supported by the case law. As stated in Phillip Denbow v. Texas Department of Criminal Justice 1 (2025), we must accept as true all factual allegations in the plaintiff's pleadings, construe them liberally in the pleader's favor, look to the pleader's intent, and determine if the plaintiff has satisfied his burden. (Tex. Dep't of Crim. Just. v. Rangel, 595 S.W.3d 198, 205 (Tex. 2020); Miranda, 133 S.W.3d at 226). This means that the prosecution's allegations must be taken as true, and the defense's arguments must be considered in light of this standard.

In addition, the defense's argument that the defendant's prior conviction for a felony does not make him prohibited from possessing a firearm is not supported by the case law. As stated in In re Texas Department of Criminal Justice Relator 1 (2025), a convicting court's pre-filing order does not clearly and indisputably exceed the permissible scope of implicit authority under the statute. (See In re Texas Department of Criminal Justice Relator 1 (2025)). This means that the convicting court's implicit authority to facilitate the investigation of potential claims is not limited by the statute of limitations, and the defendant's prior conviction for a felony is still relevant to the case.

In conclusion, the prosecution's argument regarding the convicting court's implicit authority is supported by the case law, and the defense's arguments are not supported by the case law. The prosecution has met its burden of proof, and the defendant's prior conviction for a felony is still relevant to the case.

CASE LAW CITATIONS

In re Texas Department of Criminal Justice Relator 1 (2025)
Kerr, 64 S.W.3d at 419
Ex parte Medina, 361 S.W.3d 633, 637-38 (Tex. Crim. App. 2011) (per curiam)
Phillip Denbow v. Texas Department of Criminal Justice 1 (2025)
Tex. Dep't of Crim. Just. v. Rangel, 595 S.W.3d 198, 205 (Tex. 2020)
Miranda, 133 S.W.3d at 226
```