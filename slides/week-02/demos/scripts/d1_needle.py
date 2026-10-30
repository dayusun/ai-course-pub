"""Demo 1: lost in the middle. ~30k tokens of generated trial-operations prose, one needle at 5/50/95% depth,
5 filler seeds per position per model. The filler never contains the word "outcome" or the number 37."""
import json
import random
import re
from concurrent.futures import ThreadPoolExecutor

from nrp import ROOT, answer_text, chat, save_prompt, usage

NEEDLE = "The trial's primary outcome was measured at week 37."
QUESTION = "At which week was the primary outcome measured? Answer with the number."
DEPTHS = [0.05, 0.50, 0.95]
SEEDS = [1, 2, 3, 4, 5]
MODELS = ["qwen3-small", "glm-5"]
TARGET_WORDS = 21500

SITES = ["Riverside", "Northgate", "Lakeview", "Hillcrest", "Eastbrook", "Westfield", "Pinehurst", "Cedar Valley",
         "Maple Grove", "Stonebridge", "Fairhaven", "Brookside"]
ROLES = ["the study coordinator", "the site pharmacist", "the clinical monitor", "the data manager",
         "the research nurse", "the principal investigator", "the regulatory officer", "the laboratory lead"]
TOPICS = ["site initiation", "drug accountability", "source data verification", "consent documentation",
          "sample shipping", "temperature logging", "protocol training", "query resolution", "visit scheduling",
          "device calibration", "staff delegation", "archiving"]
WEEKS = [w for w in range(1, 53) if w != 37]
COUNTS = [n for n in range(2, 49) if n != 37]
T = [
    "At the {site} site, {role} reviewed {topic} records and found {n} minor discrepancies, all corrected within {d} days.",
    "The steering committee met in month {m} and discussed {topic}; no changes to the schedule were adopted.",
    "{Role} at {site} completed refresher training on {topic} for {n} staff members.",
    "Screening visits at {site} were held on weekday mornings, and participants returned for a safety visit at week {w}.",
    "Laboratory samples from {site} were shipped on dry ice in batches of {n}, with a median transit time of {d} days.",
    "A monitoring visit at {site} in month {m} covered {topic} and closed {n} open queries.",
    "The electronic data capture system was updated to version {v}.{n}, which changed the layout of the {topic} forms.",
    "{Role} noted that {n} participants at {site} rescheduled their week {w} visit because of public holidays.",
    "Temperature excursions in the {site} pharmacy refrigerator lasted less than {d} hours and required no product quarantine.",
    "The data safety monitoring board received a blinded report on {topic} in month {m} and recommended continuation.",
    "Recruitment at {site} averaged {n} participants per month during the second quarter.",
    "Consent forms at {site} were re-signed by {n} participants after the version {v} amendment was approved.",
    "{Role} audited {topic} at {site} and recorded the findings in the trial master file.",
    "Blood pressure cuffs at {site} were recalibrated every {d} weeks according to the manufacturer's instructions.",
    "The week {w} questionnaire took a median of {d} minutes to complete at {site}.",
    "Courier delays affected {n} shipments from {site}, none of which exceeded the permitted window.",
    "A newsletter describing progress on {topic} was sent to all {n} site staff in month {m}.",
    "At {site}, {role} reconciled {n} returned medication bottles against dispensing logs.",
    "Protocol deviations related to {topic} at {site} were classified as minor and reported in month {m}.",
    "Participants at {site} were reminded of their week {w} appointment by telephone two days in advance.",
]


def filler(seed):
    rnd = random.Random(seed)
    words, paras = 0, []
    while words < TARGET_WORDS:
        para = []
        for _ in range(rnd.randint(4, 8)):
            role = rnd.choice(ROLES)
            s = rnd.choice(T).format(site=rnd.choice(SITES), role=role, Role=role[0].upper() + role[1:],
                                     topic=rnd.choice(TOPICS), n=rnd.choice(COUNTS), d=rnd.randint(1, 14),
                                     m=rnd.randint(1, 30), w=rnd.choice(WEEKS), v=rnd.randint(2, 9))
            para.append(s)
        p = " ".join(para)
        paras.append(p)
        words += len(p.split())
    text = "\n\n".join(paras)
    assert "outcome" not in text.lower() and not re.search(r"\b37\b", text)
    return text


def with_needle(text, depth):
    sentences = re.split(r"(?<=\.) ", text)
    k = round(depth * len(sentences))
    return " ".join(sentences[:k] + [NEEDLE] + sentences[k:])


def run(job):
    model, depth, seed = job
    doc = with_needle(filler(seed), depth)
    msg = f"{doc}\n\nQuestion: {QUESTION}"
    rec = chat(model, [{"role": "user", "content": msg}], f"d1_{model}_d{int(depth*100):02d}_s{seed}",
               max_tokens=2048, reasoning_effort="low")
    ans = answer_text(rec).strip()
    return {"model": model, "depth": depth, "seed": seed, "http": rec["http_status"], "answer": ans[:60],
            "correct": bool(re.search(r"\b37\b", ans)), "latency_s": rec["latency_s"], **usage(rec)}


if __name__ == "__main__":
    save_prompt("d1_question.txt", QUESTION)
    save_prompt("d1_needle.txt", NEEDLE)
    save_prompt("d1_example_doc_seed1_depth50.txt", with_needle(filler(1), 0.50) + f"\n\nQuestion: {QUESTION}")
    jobs = [(m, d, s) for m in MODELS for d in DEPTHS for s in SEEDS]
    with ThreadPoolExecutor(max_workers=6) as ex:
        rows = list(ex.map(run, jobs))
    (ROOT / "raw" / "d1_summary.json").write_text(json.dumps(rows, indent=1))
    for r in rows:
        print(f"{r['model']:12} depth={r['depth']:.2f} seed={r['seed']} http={r['http']} correct={r['correct']} "
              f"ans={r['answer']!r} prompt_tok={r['prompt_tokens']} lat={r['latency_s']}s")
