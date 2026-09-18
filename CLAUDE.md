# Concierge Evals

## What this is
A small portfolio project for an AI product manager job application. The company builds AI phone agents for healthcare and needs someone to define what a good call looks like, grade calls at scale, find where agents fail, and prove fixes work. This project shows that skill using a hotel instead of a hospital.

## The idea
A fictional hotel, The Harbor Hotel, has an AI front desk that answers guest phone calls. We write 30 realistic call transcripts. Some are good, some are tricky but still good, and some contain one planted mistake. Mira writes a checklist of what a good call looks like. Then a separate, fresh grader uses only that checklist to grade every call. We compare its grades to the answer key to see what it caught, what it missed, and what it wrongly flagged.

## The hotel's teams
Front desk, housekeeping, maintenance, security, concierge (restaurants, spa, cars), room service, and a duty manager.

## Types of mistakes the AI can make
- Wrong team: sends a problem to a team that doesn't handle it
- Made-up info: states a fact, time, price, staffing detail, or policy that isn't in hotel_facts.md
- Privacy: shares a guest's room number or confirms someone is staying without verifying who's asking
- Missed emergency: doesn't escalate a safety or medical situation right away
- Rude: dismissive, cold, or blames the guest. Politely saying no is not rude.

## Files
- hotel_facts.md: the only source of truth about the hotel
- agent_rules.md: how the AI front desk must behave on every call
- calls/call_01.txt to calls/call_30.txt: call transcripts
- rubric.md: Mira's grading checklist. Mira writes this herself.
- my_grades.csv: Mira's hand grades
- judge_grades.csv: the grader's results
- summary.md: Mira's one-page findings

## The plan
1. Hotel facts file
2. Front desk AI rules
3. Write 5 good calls
4. Write 17 more good calls, including tricky calls where the AI does the right thing but it could look wrong
5. Write 8 calls with one planted mistake each, plus a private answer key
6. Fact-check every call against hotel_facts.md
7. Mira writes the checklist
8. Mira grades 10 calls by hand
9. Mira moves the answer key out of the folder
10. A fresh session grades all 30 calls
11. Compare grades to the answer key
12. Find patterns, and Mira writes the one-page summary
13. Put it on GitHub

## Rules for you
- Only do the one step Mira asks for. When it's done, show the result and stop. Never start the next step on your own.
- Every fact in a call must come from hotel_facts.md. Before calling any call "good," check every claim in it against that file. If something isn't in the file, remove it from the call or ask Mira before adding it to the file.
- In good calls, state facts only in the facts file's own terms. No inferences, summaries, or reasonable readings.
- Plain text, markdown, and CSV only. No API calls, no web app.
- Mira makes the product decisions. If anything is unclear, ask her instead of guessing.
- Never write the answer key or mistake details into this file or any file the grader will read, except the answer key itself.
- Keep writing simple and readable. No em dashes.
