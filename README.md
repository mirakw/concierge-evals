# Concierge Evals

A test set for measuring how well an LLM judge grades AI phone calls. A fictional
hotel, The Harbor Hotel, has an AI front desk. 30 call transcripts were written
against a single source of truth, 8 of them with exactly one planted failure. A
separate session graded all 30 using only the rubric, with no access to the
answer key. Its grades were then compared to the verified labels.

Read [summary.md](summary.md) for the findings.

## Results

| | |
|---|---|
| Planted failures caught | 8 of 8, correct failure mode on each |
| Correct calls wrongly failed | 0 of 22, including all 7 tricky ones |
| Agreement with the verified labels | 30 of 30 |
| Confidence | 28 high, 2 medium, 0 wrong at either level |

Grading run: Claude Opus 5, 2026-09-17.

The judge quoted a different line than the answer key on 4 of the 8 catches. It
reached the right verdict every time, but pointed at different evidence.

## Files

| Path | What it holds |
|---|---|
| `hotel_facts.md` | The only source of truth about the hotel. Hours, policies, routing, staffing, privacy rules, emergency steps. |
| `agent_rules.md` | How the AI front desk must behave on every call. |
| `rubric.md` | The grading checklist. The five failure modes, what is explicitly not a failure, and the output format. |
| `calls/` | The 30 transcripts, `call_01.txt` to `call_30.txt`, shuffled so the numbering gives nothing away. |
| `drafts/` | The calls under their original names, `good_01` to `good_22` and `bad_01` to `bad_08`. Reveals which calls carry a planted failure. |
| `answer_key.csv` | The verified labels. Maps each call to its draft, pass or fail, the failure mode, the exact line, why it is wrong, and whether the call is tricky. |
| `judge_grades.csv` | What the grading session produced. |
| `compare.py` | Compares the judge's grades to the answer key. |
| `results.txt` | Output of `compare.py`. |
| `summary.md` | The one page writeup. |
| `grading-session/` | Exactly what the grading session could see. Nothing else was available to it. |

**The grader only saw the contents of `grading-session/`:** the 30 calls, the
facts file, the agent rules, and the rubric. It never saw the answer key, the
drafts folder, this README, or the project notes.

The answer key ships with this repo so readers can check the labels. That means a
fresh clone cannot rerun the grading blind. To repeat the test honestly, copy
grading-session/ somewhere outside this folder first.

## Rerunning the grading

1. Start a fresh session with `grading-session/` as its working directory. Do not
   give it access to the parent folder, which contains the answer key.
2. Point it at `rubric.md`. The rubric names its own inputs and output format.
3. It writes `judge_grades.csv` into that folder.
4. Copy the file up and compare:

```bash
cp grading-session/judge_grades.csv . && python3 compare.py
```

`compare.py` writes `results.txt` and prints the same report. It needs only
Python 3 and the standard library.
