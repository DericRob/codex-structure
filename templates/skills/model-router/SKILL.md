---
name: model-router
description: Classify task complexity and route to the cheapest capable LLM model. Reduces costs 40-60% on routine tasks without quality loss.
tools: []
requires:
  env: []
---

# Model Router

Intelligent routing of tasks to the most cost-effective LLM model based on complexity classification.

## When to Use

- Before every LLM call in a multi-model system
- When building cost-aware agent pipelines
- When configuring provider fallback chains

## Complexity Tiers

### Tier 1: Fast (Haiku / GPT-4o-mini / Gemini Flash)
**Cost:** ~$0.25/M tokens | **Latency:** <1s

Route here when:
- Simple lookups, formatting, extraction
- Yes/no questions with clear answers
- Template filling, data transformation
- Classification with <5 categories
- Summarizing short text (<500 words)

Keywords: "format", "extract", "list", "convert", "classify", "summarize short"

### Tier 2: Balanced (Sonnet / GPT-4o / Gemini Pro)
**Cost:** ~$3/M tokens | **Latency:** 2-5s

Route here when:
- Multi-step reasoning with 2-3 hops
- Code generation for known patterns
- Document analysis (500-5000 words)
- Creative writing with constraints
- API integration / tool use planning

Keywords: "analyze", "write code", "draft", "compare", "research", "plan"

### Tier 3: Heavy (Opus / GPT-4.5 / Gemini Ultra)
**Cost:** ~$15/M tokens | **Latency:** 5-30s

Route here when:
- Complex multi-document reasoning
- Novel architecture design
- Debugging subtle/intermittent issues
- Strategic planning with many variables
- Long-form content requiring coherence >2000 words
- Tasks where errors are expensive (financial, legal, security)

Keywords: "architect", "debug complex", "strategic", "design system", "legal review"

## Routing Algorithm

```
1. Score keywords in the prompt (0-100)
   - Tier 1 keywords: +10 each
   - Tier 2 keywords: +30 each
   - Tier 3 keywords: +60 each
2. Adjust for context length
   - <1K tokens input: -10 (simpler)
   - >10K tokens input: +20 (needs more capability)
3. Adjust for tool use
   - >3 tools needed: +15
4. Route to lowest tier that exceeds threshold
   - Score <30: Tier 1
   - Score 30-59: Tier 2
   - Score ≥60: Tier 3
5. Override: if task is in CONFIRMATION_REQUIRED set, minimum Tier 2
```

## Cost Savings Example

| Workload (1000 tasks/day) | Without Router | With Router | Savings |
|---------------------------|---------------|-------------|---------|
| 60% simple, 30% medium, 10% complex | All Tier 3: $150/day | Mixed: $52/day | 65% |

## Integration Notes

- Log every routing decision with: task_hash, score, tier_chosen, model_used
- Track quality metrics per tier to calibrate thresholds over time
- Allow manual override via user preference ("always use best model")
- Fallback chain: if chosen tier fails, escalate to next tier
