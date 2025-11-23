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

### Procedural Protocols

#### `get_turn_taking_protocol() -> str`
Returns instructions for managing conversational turns and Supreme Court-style interruptions.

```python
turn_protocol = get_turn_taking_protocol()
# Append to agent context or use in system coordinator
```

#### `get_rag_integration_protocol() -> str`
Returns the protocol for handling case law search requests and integrating retrieval results.

**Covers:**
- Search request format: `[SEARCH: query text]`
- Query optimization strategies
- Result formatting
- Citation incorporation

```python
rag_protocol = get_rag_integration_protocol()
```

### Guidelines and Formats

#### `get_response_format_guidelines() -> str`
Returns general response structure and argumentation techniques applicable to all agents.

#### `get_citation_format_examples() -> str`
Returns examples of proper legal citation formats for cases, statutes, and constitutional provisions.

```python
citation_guide = get_citation_format_examples()
# Use as reference for citation generation
```

### Quality Control

#### `get_quality_checklist(agent_role: str) -> str`
Returns a role-specific pre-submission checklist.

**Parameters:**
- `agent_role`: One of `"prosecution"`, `"defense"`, or `"judge"`

**Raises:**
- `ValueError`: If agent_role is invalid

```python
# Get checklists for each role
prosecution_checklist = get_quality_checklist("prosecution")
defense_checklist = get_quality_checklist("defense")
judge_checklist = get_quality_checklist("judge")
```

### System Management

#### `get_error_recovery_protocol() -> str`
Returns protocols for handling off-topic responses, stalled debates, and other system issues.

```python
recovery_protocol = get_error_recovery_protocol()
# Use in system coordinator/orchestrator
```

### Convenience Function

#### `get_all_prompts() -> Dict[str, str]`
Returns all available prompts in a single dictionary.

```python
all_prompts = get_all_prompts()

# Access individual prompts
prosecution = all_prompts['prosecution']
defense = all_prompts['defense']
judge = all_prompts['judge']
rag_protocol = all_prompts['rag_integration']

# Available keys:
# - 'prosecution'
# - 'defense'
# - 'judge'
# - 'turn_taking'
# - 'rag_integration'
# - 'response_format'
# - 'citation_format'
# - 'prosecution_checklist'
# - 'defense_checklist'
# - 'judge_checklist'
# - 'error_recovery'
```

## Module Constants

```python
from prompts import AGENT_ROLES, AVAILABLE_PROMPTS

print(AGENT_ROLES)  # ['prosecution', 'defense', 'judge']
print(AVAILABLE_PROMPTS)  # List of all available prompt keys
```
