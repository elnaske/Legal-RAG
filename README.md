# Legal-RAG

## Proposal Notes

  - - -

**a. What is the motivation for your project?**

The American legal system follows common law, that is, judicial decisions are, to a large degree, based by precedents set by previous rulings.
In preparation for a case, lawyers have to do extensive research on these previous rulings to support their arguments.
This involves a lot of manual work.
We want to use LLM agents in conjunction with RAG to aid this process:
The user prompts the system with a legal inquiry, which is then discussed by two agents, representing opposing lawyers in court (such as prosecution/defense in criminal cases).
These lawyer-agents support their arguments through RAG, by querying a vector database made up of a case law corpus.
After a few turns, the discussion ends and the conversation is summarized by another LLM.
That way, the final answer not only provides relevant case law, but also considers how the other side might try counter it.

  - - -

**b. What do you need for it?**

**Data**

Court rulings are publically available through free services like courtlistener.com.
We plan to use their API to pull the necessary data.
For the sake of scope, we will limit ourselves to one area of law for now.
  
**Code**

For the most part, we will be using existing packages and solutions, and connect them using our own code.

We currently envision our stack as follows:
- Data Extraction: CourtListener API, beautifulsoup for parsing HTML
- Data Preprocessing: Langchain, spaCy
- Vector database: Chroma
- LLM: HuggingFace transformers, potentially an API
  
**Infrastructure**

Our current plan is to mainly use IU's HPC.
We will store the vector database on Slate and do all of the data extraction and preprocessing on BigRed.
As for the running the agents, we will evaluate them on one of BigRed's GPU nodes, but for interactive use we might consider using API calls instead to avoid queue times.

  - - -

**c. Who is in the team?**

The team consists of Armando, Ben, Shusuke, and Elias.
We split up the responsibilities as follows:

- Data Extraction (Ben)
  - Pulling court rulings via API
     - Setup any scripts to unpack and places files as needed (TBA)
  - Extracting raw text from HTML
  - Setup SQLite to capture court rulings metadata tags in a relation database for further querying
- Data Preprocessing (Elias)
  - Chunking texts
  - Extracting metadata
  - Generating word embeddings
  - Uploading to vector DB
- Agent Infrastructure (Shusuke)
  - Setting up LLMs
  - Making them talk to eachother
  - Allow them to query the vector DB
- Prompt Engineering (Armando)
  - Perfecting agent behavior, modeled after real lawyers

  - - -

**d. How much time does the project consume, as estimated by subtasks?**

*There is likely to be overlap and is subject to adjust as project unfolds.*

- **Data preparation** (one-two weeks)
     - Week 1: 
        - [ ] Setup API access
        - [ ] Pull court rulings and setup scripts to organize and parse the different file types. Setup organization schema.
        - [ ] Setup pipeline to extract text from the documents. Setup SQLite to group metadata information (maybe)
     - Week 2:
        - [ ] Chunk texts and process metadata
        - [ ] Start setting up LLMs
        - [ ] Generate word embeddings 
        - [ ] Upload to Vector DB

- **Experiments** (one-two weeks)
     - Week 3: 
        - [ ] Setup LLMs to talk to each other
        - [ ] Setup LLMs to query vector db  
        - [ ] Perfect agent behavior through prompt engineering
        - [ ] Adjust any previous steps 
- **Evaluation** (one week)
     - Week 4: 
        - [ ] Evaluate results
        - [ ] Prepare presentation of results

 - - -


**e. How do you evaluate the results of your work?**

Since we aren't lawyers, and professional legal advice is outside of our budget, we have decided to evaluate the agents based on the accuracy of their citations.


## Setup Notes

### API Key

Go to `courtlistener.com` and create an account. Then navigate to `Account > Developer Tools > Your API Token` to find your API key.

In your local repository, create a file named `.env`, and add the following line, replacing `your api key here` with your API key:

```
COURTLISTENER_API_KEY=your_api_key_here
```

### Dependencies

As of now the project has the following dependencies:

- chromadb (Vector DB)
- sentence_transformers (For the embedding model)
- transformers (For the LLM)
- beatifulsoup4 (For parsing HTML)
- langchain-text-splitters (Text Chunking)
- dot-env (For reading the API key; cf. above)
- PyTorch
