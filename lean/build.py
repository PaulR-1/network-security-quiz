#!/usr/bin/env python3
"""Quiz from the Lean / Validation Board exam photos."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "appdev"))
import build as appdev  # noqa: E402

OUT = Path(__file__).resolve().parent


def single(exam, q, right, wrongs, explain):
    options = [right[0]] + [w[0] for w in wrongs]
    why = {right[0]: right[1]}
    why.update({t: w for t, w in wrongs})
    return {
        "exam": exam,
        "type": "single",
        "q": q,
        "options": options,
        "answer": [right[0]],
        "why": why,
        "explain": explain,
    }


def tf(exam, q, answer_true, why_true, why_false, explain):
    right = "True" if answer_true else "False"
    wrong = "False" if answer_true else "True"
    why = {"True": why_true, "False": why_false}
    return {
        "exam": exam,
        "type": "single",
        "q": q,
        "options": ["True", "False"],
        "answer": [right],
        "why": why,
        "explain": explain,
    }


def questions():
    return [
        single(
            11,
            "An IT student team developing a Cloud Microservices Cost Optimizer conducts 10 user discovery interviews with DevOps engineers. 8 out of 10 engineers state that AWS bill reduction is 'extremely important,' but when asked to grant read-only IAM access to a sandbox script to audit their actual cluster cost usage, only 1 engineer consents. How should the IT team interpret this outcome according to the Validation Board framework?",
            (
                "Pivot or re-evaluate the Problem/Customer hypothesis because verbal statements failed to translate into customer currency (granting IAM access/behavioral commitment).",
                "The Validation Board treats currency and behavior as evidence. Eight people saying the problem is important is a pitch; only one granting access is the commitment. The hypothesis is not validated.",
            ),
            [
                (
                    "Persevere with the current product pitch because 80% expressed verbal interest in AWS bill reduction.",
                    "Verbal interest is not customer currency. The board asks whether people give up something, and here almost nobody did.",
                ),
                (
                    "Terminate the project immediately and replace the student lead with a senior DevOps consultant.",
                    "An invalidated experiment calls for a pivot of the hypothesis, not for firing the team.",
                ),
                (
                    "Increase the permissions requested in the IAM policy to require administrative control.",
                    "Asking for more access raises the cost of the ask. It does not explain why stated interest failed to become a commitment.",
                ),
            ],
            "Opinions are not validation. Only one engineer paid the currency of granting access, so the team should pivot or re-test the customer and problem hypothesis.",
        ),
        tf(
            14,
            "In Lean Software Development and Customer Discovery, when an experiment invalidates a core technical or problem assumption, the methodology requires 'firing the hypothesis/plan' rather than 'firing the engineering team'.",
            True,
            "A failed experiment kills the assumption, not the people who ran it. The next step is to pivot the plan.",
            "Firing the team is the opposite of the rule. The hypothesis is what gets discarded.",
            "Invalidate the plan. Keep the team and change the hypothesis.",
        ),
        tf(
            15,
            "Large Scale Scrum (LeSS) requires every individual feature team to maintain its own completely separate, isolated Product Backlog.",
            False,
            "LeSS uses one Product Backlog for the product, shared by the feature teams.",
            "Separate backlogs would split the product. LeSS keeps a single Product Backlog and one Product Owner.",
            "LeSS does not give each team its own backlog. There is one Product Backlog.",
        ),
        single(
            16,
            "An IT team is setting up their initial Validation Board canvas for an automated container orchestration monitoring tool. In what precise order must the canvas components be populated and tested?",
            (
                "Customer Segment -> Problem Hypothesis -> Riskiest Assumption -> Solution Hypothesis.",
                "The board starts with who the customer is and what problem they have. You name the riskiest assumption before you commit to a solution. The board's own tip is not to define a solution until the problem is validated.",
            ),
            [
                (
                    "Riskiest Assumption -> Solution Hypothesis -> Customer Segment.",
                    "The riskiest assumption is chosen from the customer and problem hypotheses. It is not the first sticky, and the customer is not last.",
                ),
                (
                    "Docker Deployment Pipeline -> Unit Tests -> Customer Segment.",
                    "A deployment pipeline and unit tests are engineering work. They are not the order of the Validation Board canvas.",
                ),
                (
                    "Solution Architecture -> Customer Segment -> Problem Hypothesis.",
                    "Starting with the solution is the mistake the board warns against. Customer and problem come first.",
                ),
            ],
            "Fill customer, then problem, then the riskiest assumption. Do not lock the solution until the problem has evidence.",
        ),
        single(
            17,
            "Which of the following is NOT one of the three core Validation Methods defined in the Lean Customer Development framework?",
            (
                "Static Code Inspection Method",
                "The Validation Board names three experiment methods: Exploration, Pitch, and Concierge. Static code inspection is a code-quality practice, not one of those methods.",
            ),
            [
                (
                    "Pitching Method",
                    "Pitch is one of the three. You ask the customer for currency in exchange for solving the problem.",
                ),
                (
                    "Concierge Method",
                    "Concierge is one of the three. You deliver the service by hand to a few customers before building the product.",
                ),
                (
                    "Exploration Method",
                    "Exploration is one of the three. You interview and observe to learn the problem before you pitch a solution.",
                ),
            ],
            "Exploration, Pitch, and Concierge are the three methods. Static code inspection is not.",
        ),
        tf(
            18,
            "Test-Driven Development (TDD) in XP requires software engineers to write production code first and then generate unit tests afterwards.",
            False,
            "TDD writes the failing test first, then the production code that makes it pass, then refactors.",
            "Production code first is the reverse of TDD. The test comes before the code.",
            "TDD is test first: red, green, refactor. Production code does not come first.",
        ),
        single(
            21,
            "A team building an AI-powered code review assistant manually inspects pull requests and emails handwritten feedback to 10 beta developer teams every evening, intentionally postponing the development of Machine Learning parsing models. What is the strategic engineering rationale for using this Concierge (Wizard of Oz) approach?",
            (
                "To validate that developers value and act on the feedback before investing heavy engineering effort into complex AI/ML backend automation.",
                "Concierge delivers the service manually so you learn whether customers want it before you build the expensive system. That is the Wizard of Oz pattern.",
            ),
            [
                (
                    "Because manual code reviews provide higher AES-256 data encryption than automated AI pipelines.",
                    "Encryption strength is not why the team is doing the work by hand.",
                ),
                (
                    "To fulfill Waterfall documentation requirements before starting the software design phase.",
                    "Concierge is a learning experiment, not a Waterfall document gate.",
                ),
                (
                    "To trick users into believing the student team has already secured patent protection for their AI model.",
                    "The point is to test value, not to fake a patent.",
                ),
            ],
            "Do the job by hand first. Build the model only after developers show they value the feedback.",
        ),
        single(
            22,
            "What is the functional difference between Scrum of Scrums (SoS) and Large Scale Scrum (LeSS) for multi-team coordination?",
            (
                "SoS uses team representatives meeting at scaled daily standups; LeSS scales Scrum by sharing a single Product Backlog and sprint cadence across teams.",
                "Scrum of Scrums is a coordination meeting of team representatives. LeSS is a framework: one Product Owner, one Product Backlog, and teams in the same sprint.",
            ),
            [
                (
                    "There is no difference; they are identical frameworks.",
                    "SoS is a meeting technique. LeSS is a full scaling framework with one backlog.",
                ),
                (
                    "SoS is for Waterfall; LeSS is for Kanban.",
                    "Both sit in the Scrum family. Neither one is Waterfall, and LeSS is not Kanban.",
                ),
                (
                    "SoS requires 1,000 developers; LeSS is limited to 3 developers.",
                    "Those head-count limits are not the difference. LeSS is typically a handful of feature teams, not a three-person cap.",
                ),
            ],
            "SoS coordinates through representatives. LeSS shares one Product Backlog and one sprint cadence.",
        ),
        tf(
            23,
            "IT startups and innovative software project teams should operate in 'Search Mode' (hypotheses testing) before transitioning into 'Execution Mode' (scaling production software).",
            True,
            "Customer Development separates search, where you test hypotheses, from execution, where you scale a model that has evidence.",
            "Skipping search and scaling production first is how teams build something nobody wants.",
            "Search first, then execute. Test the hypotheses before you scale the software.",
        ),
        single(
            24,
            "How does the Validation Board define the 'Riskiest Assumption' in a software project hypothesis?",
            (
                "The core unproven assumption that has the least evidence and whose invalidation would cause the entire software concept to fail.",
                "A core assumption is anything that breaks the business if it is false. The riskiest one is the least certain of those.",
            ),
            [
                (
                    "The technical feature that requires the most complex SQL query optimization.",
                    "Implementation difficulty is not what makes an assumption the riskiest. Failure of the business is.",
                ),
                (
                    "The UI button color that developers disagree on during sprint planning.",
                    "A color debate is not a core assumption. Invalidating it would not kill the concept.",
                ),
                (
                    "The cloud hosting provider with the highest monthly invoice.",
                    "The largest bill is a cost, not the assumption whose failure collapses the hypothesis.",
                ),
            ],
            "The riskiest assumption is the unproven belief that would sink the whole concept if it is wrong.",
        ),
        tf(
            25,
            "Achieving 1,000 unique page views on a documentation website for an open-source software tool definitively proves that enterprise IT teams will pay monthly license fees for an enterprise edition.",
            False,
            "Page views are not payment. The board wants currency, such as a purchase or a commitment, before you treat willingness to pay as proven.",
            "Traffic does not prove that an enterprise team will pay a license fee.",
            "A thousand page views do not prove anyone will pay for an enterprise edition.",
        ),
        single(
            27,
            "What are the three primary hypothesis sticky types placed on the Validation Board canvas?",
            (
                "Customer, Problem, Solution.",
                "The board's core hypotheses are the Customer Hypothesis, the Problem Hypothesis, and the Solution Hypothesis.",
            ),
            [
                (
                    "Agile, Scrum, Kanban.",
                    "Those are delivery methods, not the three hypothesis stickies.",
                ),
                (
                    "Unit Test, Integration Test, Deployment.",
                    "Those are engineering stages, not the canvas hypotheses.",
                ),
                (
                    "Frontend, Backend, Database.",
                    "Those are system layers, not Customer, Problem, and Solution.",
                ),
            ],
            "The three hypothesis stickies are Customer, Problem, and Solution.",
        ),
        tf(
            29,
            "Kanban relies on fixed-length, timeboxed iterations (sprints) to schedule software releases.",
            False,
            "Kanban is a continuous flow with a limit on work in progress. Fixed-length sprints belong to Scrum.",
            "Timeboxed sprints are a Scrum practice, not a Kanban requirement.",
            "Kanban does not schedule work in sprints. Scrum does.",
        ),
        tf(
            30,
            "'Get Out Of The Building' (GOOTB) is a core Customer Development directive co-founded by Steve Blank that urges builders to gather direct evidence from real users rather than sitting in the lab.",
            True,
            "Steve Blank's Customer Development rule is to leave the building and learn from real customers instead of debating inside the lab.",
            "Staying in the lab is what GOOTB tells you not to do.",
            "Get out of the building. Evidence comes from real users, not from the lab.",
        ),
    ]


def main():
    bank = questions()
    engine = appdev.ENGINE.replace(
        'count.textContent = "Question " + (i + 1) + " of " + deck.length;',
        'count.textContent = "Question " + (i + 1) + " of " + deck.length + (q.exam ? "  ·  Exam #" + q.exam : "");',
    )
    payload = json.dumps(bank, ensure_ascii=False).replace("<", "\\u003c")
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Lean validation exam</title>
  <link rel="stylesheet" href="../theme.css" />
  <style>
    .row {{ grid-template-columns: 1fr minmax(9.5rem, 15rem); }}
  </style>
</head>
<body>
  <div class="wrap">
    <a class="exit" href="../index.html">All reviewers</a>
    <h1>Lean validation exam</h1>
    <p class="sub">Fourteen questions from the exam photos, numbered the way they appeared. Validation Board, Customer Development, Scrum of Scrums, LeSS, Kanban, and TDD. A miss shows why.</p>
    <div class="bar"><i id="prog"></i></div>
    <div class="meta">
      <span id="count"></span>
      <span id="scoreline"></span>
    </div>
    <div class="card" id="panel"></div>
  </div>
  <script>
    const BANK = {payload};
{engine}
  </script>
</body>
</html>
"""
    (OUT / "index.html").write_text(html, encoding="utf-8")
    print(len(bank), "questions")


if __name__ == "__main__":
    main()
