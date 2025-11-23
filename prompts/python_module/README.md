# Legal-RAG Prompts Module

A Python module providing system prompts for AI agents in our Legal-RAG courtroom simulation system. The prompts are designed to simulate prosecution, defense, and judge roles in criminal trial proceedings, based on analysis of Supreme Court oral argument transcripts.

## Features

- **Role-specific prompts** for prosecution, defense, and judge agents
- **Supreme Court-derived strategies** from analysis of real oral arguments
- **RAG integration protocols** for case law retrieval
- **Comprehensive documentation** with examples and usage guidelines
- **Quality control checklists** for each agent role
- **Error recovery protocols** for system coordination

## Installation

Copy `prompts.py` to the project directory or add it to the Python path.

```bash
cp prompts.py /path/to/project/

# Or 
export PYTHONPATH="${PYTHONPATH}:/path/to/prompts/directory"
```

## Quick Start

```python
from prompts import get_prosecution_prompt, get_defense_prompt, get_judge_prompt

# Individual agent prompts
prosecution_prompt = get_prosecution_prompt()
defense_prompt = get_defense_prompt()
judge_prompt = get_judge_prompt()

# Use with LLM framework
prosecution_agent = YourAgent(system_prompt=prosecution_prompt)
defense_agent = YourAgent(system_prompt=defense_prompt)
judge_agent = YourAgent(system_prompt=judge_prompt)
```

## Available Functions

### Core Agent Prompts

#### `get_prosecution_prompt() -> str`
Returns the complete system prompt for the prosecution agent.

**Key features:**
- Strategic priorities from Supreme Court analysis
- Evidence presentation structure
- Objection protocols
- Case law citation requirements
- Ethical constraints

```python
prosecution_prompt = get_prosecution_prompt()
```

#### `get_defense_prompt() -> str`
Returns the complete system prompt for the defense agent.

**Key features:**
- Constitutional defense strategies
- Cross-examination techniques
- Reasonable doubt emphasis
- Witness impeachment methods
- Ethical boundaries

```python
defense_prompt = get_defense_prompt()
```

#### `get_judge_prompt() -> str`
Returns the complete system prompt for the judge agent.

**Key features:**
- Ruling protocols with legal reasoning
- Common evidence issues (hearsay, relevance, etc.)
- Summary formats for trial phases
- Neutrality requirements
- Procedural management

```python
judge_prompt = get_judge_prompt()
```
