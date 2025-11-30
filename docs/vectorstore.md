# VECTORSTORE
- - -
- [VECTORSTORE](#vectorstore)
    - [Accessing the vector database](#accessing-the-vector-database)
    - [Querying](#querying)
- - -

### Accessing the vector database
Use the `get_vectorstore()` function to instantiate a `VectorStore` object.
This ensures that access to the vector database is set up correctly and uniform across the repo.

```python
from src.vectorstore import get_vectorstore()

vectorstore = get_vectorstore()
```

### Querying
To get a prompt that can be passed to an LLM, use the `rag_query()` method:

```py
user_query = "What is the music of life?"
n_results = 5

prompt = vectorstore.rag_query(user_query, n_results)
```

Alternatively, you can query the database directly to only get the top matches.
```py
contexts = vectorstore.query(user_query, n_results)
```