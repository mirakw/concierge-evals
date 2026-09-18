# Concierge Evals

## Why I built this
AI phone agents handle thousands of calls. Teams grade those calls with another
AI. I wanted to know how well that grader actually works, so I built a test set
where every label was human-verified and measured what the grader caught.

The approach follows the eval process Hamel Husain and Shreya Shankar lay out:
define failure modes, build an LLM judge, and validate the judge against human
labels instead of trusting its output. One departure, noted below.

## Setup
The Harbor Hotel has an AI front desk. I wrote:
- A facts file: hours, policies, team routing, overnight staffing, privacy
  rules, emergency steps. The only source of truth.
- Agent rules: how the AI must behave on every call.
- A failure taxonomy of five modes: wrong team, made-up info, privacy, missed
  emergency, rude.
- 30 transcripts. 22 correct, 8 with exactly one planted failure.
- 7 of the 22 are tricky. The AI says no, refuses to guess, or escalates
  something the guest downplays. They look like failures and are not.
- A rubric: binary pass/fail, the failure mode, a quoted line, a one-sentence
  critique, and a confidence rating.

I generated the calls with an LLM and then verified every one line by line
against the facts file before accepting its label. I shuffled and renamed the
calls so the numbering gave nothing away. A separate session graded them with
no access to the answer key, the drafts, or my notes.

## Departure from the standard process
The usual path is error analysis on real traces: read them, open code the
failures, then axial code those notes into a taxonomy. I had no real traces, so
I specified the taxonomy up front and generated calls against it. That means
this set tests a judge against known failure modes. It cannot surface failure
modes I didn't think of, which is what error analysis on production data is for.

## Results
- 8 of 8 planted failures caught, correct mode on each
- 0 of 22 correct calls wrongly failed, including all 7 tricky ones
- 30 of 30 agreement with the verified labels
- 28 high confidence, 2 medium. Both medium calls were the two hardest in the
  set, and both were graded right.

## Findings

**A perfect score says more about the test than the judge.**
This set doesn't separate a strong judge from a weak one. It shows judging
works when the rules are precise. Next round: harder cases and a deliberately
vague rubric, to find where it breaks.

**The judge got every call right and still reported the wrong total.**
It said 21 pass, 9 fail. Its own file said 22 and 8. On another call it wrote
a critique that contradicted its own grade, then corrected itself. That's the
failure that costs you in production. A dashboard says 9 failures this week, a
team acts on it, nobody reads the rows. Aggregates need their own check.

**Most of the work was writing precise rules, not building the judge.**
Every ambiguity became a call where the judge and I could both be right. Water
on the floor: leak or flood? Does a gas smell need 911? Until each was pinned
down, the eval measured my rules instead of the judge. Same tradeoff as human
review. Vague criteria produce disagreement, and you fix it upstream.

**An AI-written answer key can't be trusted.**
On my first attempt, the model that wrote the calls also wrote the labels, and
marked a call containing made-up information as clean. If I had graded against
that key, a judge that correctly caught the error would have looked wrong.
Every label in the final set is human-verified.

**Verdict agreement is easy to measure. Evidence agreement isn't.**
On 4 of 8 catches the judge quoted a different line than my key. Twice it
quoted the dispatch line instead of the routing line, which is arguably the
better citation. Anyone reading the judge's reasoning cares about that, and a
pass/fail comparison never shows it.

## Next
- Harder cases: failures buried mid-call, two failures in one call, guests who
  are wrong about the policy
- Weaken the rubric on purpose and find where judging breaks
- Voice: run calls through speech and back, and see what misheard room numbers
  and dates do to grading
- Route low confidence calls to human review and measure what that catches
- Run error analysis on real traces, where the taxonomy is discovered rather
  than specified
