from .prompts import *

AGENT_ROLES = ['prosecution', 'defense', 'judge']
AVAILABLE_PROMPTS = [
    'prosecution', 'defense', 'judge', 'turn_taking', 'rag_integration',
    'response_format', 'citation_format', 'prosecution_checklist',
    'defense_checklist', 'judge_checklist', 'error_recovery'
]