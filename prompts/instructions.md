# Instructions

```
1. LOAD SYSTEM PROMPTS:
   - Initialize Prosecution Agent with full prompt
   - Initialize Defense Agent with full prompt
   - Initialize Judge Agent with full prompt

2. LOAD CASE TEMPLATE:
   - Decide if case template is needed
   - Select case template if yes
   - Customize facts as desired
   - Brief all agents with case facts

3. START DEBATE:
   - Coordinator sends: "Prosecution, your opening statement"
   - Let system run through opening statements
   - Monitor for [SEARCH: ] requests

4. PROCESS RAG REQUESTS:
   - When agent requests search, pause
   - Extract query and retrieve case law
   - Provide results to agent
   - Resume agent's turn

5. CONTINUE THROUGH PHASES:
   - Prosecution case-in-chief
   - Defense case (if any)
   - Closing arguments
   - Judge summary

6. EVALUATE:
   - Did agents stay in role?
   - Were arguments legally sound?
   - Did RAG provide helpful case law?
   - Was procedure followed correctly?
   - Were citations accurate?

7. REFINE:
   - Adjust prompts based on performance
   - Add more specific guidance where needed
   - Give up
```
