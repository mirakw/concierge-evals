"""Compare judge_grades.csv to answer_key.csv and write results.txt.

The answer key is the ground truth. The judge never saw it.
Run: python3 compare.py
"""

import csv
import io
import sys
from collections import Counter

KEY_FILE = "answer_key.csv"
JUDGE_FILE = "judge_grades.csv"
OUT_FILE = "results.txt"


def read_csv(path):
    with io.open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def norm_type(value):
    """Mistake types differ in case and spacing between the two files."""
    return " ".join(value.strip().lower().replace("-", " ").split())


def norm_line(value):
    """Judge quotes sometimes drop the speaker prefix."""
    text = " ".join(value.strip().lower().split())
    if text.startswith("ai:"):
        text = text[3:].strip()
    return text


def main():
    key_rows = read_csv(KEY_FILE)
    judge_rows = read_csv(JUDGE_FILE)

    key = {r["call_id"]: r for r in key_rows}
    judge = {r["call_id"]: r for r in judge_rows}

    missing = sorted(set(key) - set(judge))
    extra = sorted(set(judge) - set(key))

    out = []
    w = out.append

    w("HARBOR HOTEL EVAL: JUDGE VERSUS ANSWER KEY")
    w("=" * 60)
    w("")
    w("Calls in answer key: %d" % len(key))
    w("Calls graded by judge: %d" % len(judge))
    if missing:
        w("NOT GRADED: %s" % ", ".join(missing))
    if extra:
        w("GRADED BUT NOT IN KEY: %s" % ", ".join(extra))
    w("")

    shared = [r for r in key_rows if r["call_id"] in judge]
    planted = [r for r in shared if r["result"] == "fail"]
    clean = [r for r in shared if r["result"] == "pass"]

    # 1 and 2. Catches, and whether the mistake type matched.
    caught, missed, type_right = [], [], 0
    w("1. PLANTED MISTAKES CAUGHT")
    w("-" * 60)
    for r in planted:
        j = judge[r["call_id"]]
        if j["result"].strip().upper() == "FAIL":
            caught.append(r)
            same_type = norm_type(j["mistake_type"]) == norm_type(r["mistake_type"])
            type_right += same_type
            same_line = norm_line(j["quote"]) == norm_line(r["mistake_line"])
            w("  CAUGHT   %s  (%s)" % (r["call_id"], r["draft_file"]))
            w("           key type:   %s" % r["mistake_type"])
            w("           judge type: %s   %s"
              % (j["mistake_type"], "MATCH" if same_type else "DIFFERENT"))
            w("           quoted line: %s"
              % ("same line as key" if same_line else "different line than key"))
        else:
            missed.append(r)
            w("  MISSED   %s  (%s)  key type: %s"
              % (r["call_id"], r["draft_file"], r["mistake_type"]))
        w("")
    w("  Caught %d of %d planted mistakes." % (len(caught), len(planted)))
    w("  Mistake type matched on %d of %d catches." % (type_right, len(caught)))
    w("")

    # 3. Clean calls wrongly failed.
    false_fails = [r for r in clean
                   if judge[r["call_id"]]["result"].strip().upper() == "FAIL"]
    w("2. CLEAN CALLS WRONGLY FAILED")
    w("-" * 60)
    if false_fails:
        for r in false_fails:
            j = judge[r["call_id"]]
            w("  %s  (%s)  judge said: %s" % (r["call_id"], r["draft_file"], j["mistake_type"]))
            w("      judge reason: %s" % j["reason"])
    else:
        w("  None. All %d clean calls were passed." % len(clean))
    w("")
    w("  Wrongly failed %d of %d clean calls." % (len(false_fails), len(clean)))
    w("")

    # 4. Tricky calls.
    tricky = [r for r in shared if r["tricky"].strip().lower() == "yes"]
    tricky_right = 0
    w("3. TRICKY CALLS")
    w("-" * 60)
    for r in tricky:
        j = judge[r["call_id"]]
        ok = j["result"].strip().upper() == r["result"].strip().upper()
        tricky_right += ok
        w("  %s  %s  (%s)  judge: %s, confidence %s"
          % ("CORRECT  " if ok else "WRONG    ", r["call_id"], r["draft_file"],
             j["result"], j["confidence"]))
        w("      why it looks wrong: %s" % r["why"])
    w("")
    w("  Graded correctly: %d of %d tricky calls." % (tricky_right, len(tricky)))
    w("")

    # 5. Confidence.
    w("4. CONFIDENCE")
    w("-" * 60)
    counts = Counter(judge[r["call_id"]]["confidence"].strip().lower() for r in shared)
    wrong_by_conf = Counter()
    wrong_rows = []
    for r in shared:
        j = judge[r["call_id"]]
        if j["result"].strip().upper() != r["result"].strip().upper():
            conf = j["confidence"].strip().lower()
            wrong_by_conf[conf] += 1
            wrong_rows.append((r, j))
    for level in ("high", "medium", "low"):
        if counts.get(level):
            w("  %-7s %2d calls, %d graded wrong" % (level, counts[level], wrong_by_conf.get(level, 0)))
    other = set(counts) - {"high", "medium", "low"}
    for level in sorted(other):
        w("  %-7s %2d calls, %d graded wrong" % (level, counts[level], wrong_by_conf.get(level, 0)))
    w("")
    flagged = [(r, j) for r, j in ((r, judge[r["call_id"]]) for r in shared)
               if j["confidence"].strip().lower() in ("low", "medium")]
    if flagged:
        w("  Calls the judge was not fully confident about:")
        for r, j in flagged:
            ok = j["result"].strip().upper() == r["result"].strip().upper()
            w("    %s  (%s)  %s, confidence %s  -> %s"
              % (r["call_id"], r["draft_file"], j["result"], j["confidence"],
                 "correct" if ok else "WRONG"))
    else:
        w("  The judge reported high confidence on every call.")
    w("")
    low_med_wrong = wrong_by_conf.get("low", 0) + wrong_by_conf.get("medium", 0)
    w("  Low or medium confidence calls graded wrong: %d" % low_med_wrong)
    w("")

    # Overall.
    agree = sum(1 for r in shared
                if judge[r["call_id"]]["result"].strip().upper() == r["result"].strip().upper())
    w("5. OVERALL")
    w("-" * 60)
    w("  Agreed with the key on %d of %d calls." % (agree, len(shared)))
    w("  Missed mistakes (false pass): %d" % len(missed))
    w("  Wrong flags (false fail):     %d" % len(false_fails))
    if wrong_rows:
        w("  Calls graded wrong: %s" % ", ".join(r["call_id"] for r, _ in wrong_rows))
    w("")

    text = "\n".join(out) + "\n"
    with io.open(OUT_FILE, "w", encoding="utf-8") as f:
        f.write(text)
    sys.stdout.write(text)


if __name__ == "__main__":
    main()
