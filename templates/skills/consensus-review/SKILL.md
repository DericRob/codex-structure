---
name: consensus-review
description: Multi-pass agent review with voting before committing code or sending external communications. Quality gate that catches errors before they ship.
tools: []
requires:
  env: []
---

# Consensus Review

A structured quality gate that runs multiple independent review passes and requires majority agreement before proceeding with high-stakes actions.

## When to Use

- Before committing code that touches auth, payments, or data models
- Before sending external communications (emails, Slack messages, PR comments)
- Before deploying to production
- Before executing financial transactions
- Any action that is hard to reverse

## Process

### Step 1: Define the Action
State clearly what is about to happen:
- What will change? (files, systems, communications)
- Who is affected? (users, services, stakeholders)
- What is the rollback plan?

### Step 2: Run Independent Reviews (minimum 2, recommended 3)

Each review pass evaluates independently against these criteria:

**For Code:**
- [ ] Does it do what was requested? (correctness)
- [ ] Does it break existing functionality? (regression)
- [ ] Are there security vulnerabilities? (OWASP top 10)
- [ ] Is error handling adequate at system boundaries?
- [ ] Are tests sufficient?

**For Communications:**
- [ ] Is the tone appropriate for the recipient?
- [ ] Are facts accurate and verifiable?
- [ ] Could this be misinterpreted?
- [ ] Does it commit to anything unintended?

**For Deployments:**
- [ ] Do all tests pass?
- [ ] Are environment variables configured?
- [ ] Is the rollback procedure documented?
- [ ] Are monitoring/alerts in place?

### Step 3: Voting

Each reviewer casts: APPROVE, REQUEST_CHANGES, or BLOCK.

| Result | Threshold | Action |
|--------|-----------|--------|
| All APPROVE | Unanimous | Proceed immediately |
| Majority APPROVE | ≥2 of 3 | Proceed with noted concerns logged |
| Any BLOCK | 1+ | Stop. Address blocking concern before re-review |
| Majority REQUEST_CHANGES | ≥2 of 3 | Address changes, re-run review |

### Step 4: Document Decision

Log: action, reviewers, votes, concerns raised, final decision, timestamp.

## Anti-Patterns

- **Rubber stamping**: Reviews that always approve without findings → rotate reviewers
- **Bikeshedding**: Blocking on style preferences → only BLOCK for correctness/security
- **Review fatigue**: Too many reviews → only use for high-stakes actions (see "When to Use")
- **Single reviewer**: One pass is not consensus → minimum 2 independent passes
