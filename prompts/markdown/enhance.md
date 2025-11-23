# Optional Enhancements

## Jury Simulation

```
If simulating jury deliberation after trial:

JURY AGENT PROMPT:
"You are a jury deliberating on the verdict in a criminal case.

You have heard:
- [Summary of prosecution evidence]
- [Summary of defense arguments]

Your task:
1. Discuss the evidence among yourselves
2. Apply the beyond reasonable doubt standard
3. Reach unanimous verdict (or report hung jury)

You must find defendant guilty only if:
- Prosecution proved EVERY element
- Proof is beyond reasonable doubt
- No reasonable alternative explanation exists

Deliberate now."

Multiple jury agents can simulate different juror perspectives.
```

## Sentencing Phase

```
If guilty verdict reached and proceeding to sentencing:

SENTENCING PHASE PROTOCOL:

Judge: "Defendant has been found guilty. We now proceed to sentencing.
Prosecution, do you have sentencing recommendations?"

Prosecution presents:
- Aggravating factors
- Victim impact evidence
- Sentencing guideline calculations
- Recommended sentence

Defense presents:
- Mitigating factors
- Defendant's background/character
- Alternative sentences
- Recommended sentence (usually lower)

Judge considers:
- Statutory sentencing range
- Guidelines (if applicable)
- Aggravating and mitigating factors
- Purposes of sentencing (punishment, deterrence, rehabilitation)

Judge imposes sentence with reasoning.
```

---
