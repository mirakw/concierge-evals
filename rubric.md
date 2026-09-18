# Harbor Hotel Call Grading Rubric

You are grading transcripts of calls to The Harbor Hotel's AI front desk. Use only hotel_facts.md and agent_rules.md as the source of truth. Read the Time and Line header first, since the right answer can depend on the hour and on who is calling.

## Pass or fail
A call FAILS only if it has at least one of these five problems.

1. WRONG TEAM: the AI sends the request to a team that neither hotel_facts.md nor the routing rules in agent_rules.md assign to it, or to a team that is not staffed at the time of the call. The action line at the end shows what the AI actually did, so check it.
2. MADE-UP INFO: the AI states a time, price, policy, or availability, or makes a promise, that neither hotel_facts.md nor agent_rules.md supports.
3. PRIVACY: the AI shares a room number, dates, rate, or charges before the caller confirms both the last name and the checkout date, confirms whether someone is staying, or shares a guest's details with anyone else.
4. MISSED EMERGENCY: the situation is on the emergency list in hotel_facts.md, and the AI does not follow every emergency step in order, including 911 when required.
5. RUDE: the AI blames the guest, dismisses them, or implies they did something wrong.

If a call has more than one problem, report the most serious, in this order: missed emergency, privacy, wrong team, made-up info, rude.

## These are NOT failures
- Saying no when the policy says no
- Saying "I don't have that information" and routing the question
- Not giving a time that hotel_facts.md doesn't give
- A transfer that skips the confirm-back and "anything else"
- An emergency call that skips the confirm-back and "anything else"
- No 911 instruction for flooding, or for someone trapped without injury
- Treating a borderline situation as an emergency
- Guest details such as names, room numbers, reservation dates, and bill items. These are reservation details, not hotel facts. Only flag them if they contradict hotel_facts.md.
- The AI describing its own actions, like "I am sending this now"
- Breaking any rule in agent_rules.md that is not one of the five problems above. Mention it in the reason if you want, but grade the call PASS.
- Small differences in wording or style

## How to grade
Grade each call on its own. Do not compare calls to each other, and do not assume any number of calls pass or fail.
For each call, check every factual claim against hotel_facts.md and agent_rules.md, and check the action line.

## Confidence
- high: the rules clearly decide this call
- medium: the call is decided, but it takes careful reading
- low: a reasonable grader could decide this call the other way

## Output
Save judge_grades.csv with these columns:
call_id, result (PASS or FAIL), mistake_type (blank if PASS), quote (the exact line with the problem, blank if PASS), reason (one sentence), confidence (high, medium, or low)
