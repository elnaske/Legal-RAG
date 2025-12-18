# Legal-RAG

A system for legal research, which simulates courtroom debates using LLM agents and RAG.

## Installation
This project uses [uv](https://docs.astral.sh/uv/) for managing Python dependency.
For a guide on how to use it to set up the project, consult the `SETUP.md` in `docs/`.

In the same directory, `pulling_data.md` provides information about pulling the necessary data.
This requires access to the CourtListener API. Go to `courtlistener.com` and create an account. Then navigate to `Account > Developer Tools > Your API Token` to find your API key.

In your local repository, create a file named `.env`, and add the following line, replacing `your api key here` with your API key:

```
COURTLISTENER_API_KEY=your_api_key_here
```

Currently, this project uses Llama via [GROQ](https://groq.com/).
To run the system, you will likewise need a GROQ API key.
Same as with CourtListener, place the key in the `.env` file:
 
```
GROQ_API_KEY=your_api_key_here
```
