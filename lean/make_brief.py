#!/usr/bin/env python3
"""One-file brief a student can upload to ChatGPT."""

from pathlib import Path

from fpdf import FPDF

OUT = Path(__file__).resolve().parent / "lean-validation-brief.pdf"
FONT = "/usr/share/fonts/truetype/liberation/LiberationSans-{}.ttf"

NAVY = (15, 20, 25)
INK = (26, 35, 50)
MUTED = (74, 90, 106)
BLUE = (37, 99, 196)
RULE = (213, 222, 234)
WASH = (244, 247, 251)
PAPER = (255, 255, 255)


class Brief(FPDF):
    def __init__(self):
        super().__init__(format="A4", unit="mm")
        self.add_font("sans", "", FONT.format("Regular"))
        self.add_font("sans", "B", FONT.format("Bold"))
        self.add_font("sans", "I", FONT.format("Italic"))
        self.add_font("sans", "BI", FONT.format("BoldItalic"))
        self.set_auto_page_break(auto=True, margin=16)
        self.set_margins(16, 18, 16)

    def header(self):
        self.set_fill_color(*NAVY)
        self.rect(0, 0, 210, 11, "F")
        self.set_fill_color(*BLUE)
        self.rect(0, 11, 210, 1.2, "F")
        self.set_xy(16, 3.2)
        self.set_font("sans", "B", 8)
        self.set_text_color(232, 238, 246)
        self.cell(120, 5, "Lean validation exam  ·  crash-course brief", align="L")
        self.cell(0, 5, "Upload this file to ChatGPT", align="R")
        self.set_text_color(*INK)
        self.set_y(16)

    def footer(self):
        self.set_y(-12)
        self.set_draw_color(*RULE)
        self.line(16, self.get_y(), 194, self.get_y())
        self.set_y(-10)
        self.set_font("sans", "", 8)
        self.set_text_color(*MUTED)
        self.cell(0, 6, f"Ground truth for the photographed items only     {self.page_no()}", align="C")
        self.set_text_color(*INK)

    def gap(self, h=3):
        self.ln(h)

    def ensure(self, h):
        if self.get_y() + h > self.h - 16:
            self.add_page()

    def h1(self, text):
        self.ensure(32)
        self.gap(2)
        self.set_font("sans", "B", 15)
        self.set_text_color(*NAVY)
        self.multi_cell(0, 7, text)
        self.set_draw_color(*BLUE)
        y = self.get_y() + 0.6
        self.set_line_width(0.5)
        self.line(16, y, 42, y)
        self.set_line_width(0.2)
        self.ln(3.2)
        self.set_text_color(*INK)

    def h2(self, text):
        self.ensure(26)
        self.gap(1.5)
        self.set_font("sans", "B", 12)
        self.set_text_color(*BLUE)
        self.multi_cell(0, 6, text)
        self.set_text_color(*INK)
        self.ln(0.6)

    def p(self, text, size=10.5, style=""):
        self.set_font("sans", style, size)
        self.set_text_color(*INK)
        self.multi_cell(0, 5.2, text)
        self.ln(1.6)

    def bullet(self, text):
        self.ensure(8)
        x = self.l_margin
        y = self.get_y()
        self.set_text_color(*INK)
        self.set_font("sans", "B", 10.5)
        self.set_xy(x, y)
        self.cell(4, 5.2, "·")
        self.set_xy(x + 5, y)
        self.set_font("sans", "", 10.5)
        self.multi_cell(self.epw - 5, 5.2, text, markdown=True)
        self.ln(0.5)

    def note(self, label, text):
        self.ensure(12)
        self.set_font("sans", "BI", 10)
        self.set_text_color(*BLUE)
        self.write(5.2, label + "  ")
        self.set_font("sans", "I", 10)
        self.set_text_color(*INK)
        self.write(5.2, text)
        self.ln(7)

    def box(self, title, paragraphs):
        self.set_font("sans", "", 10)
        inner_w = self.epw - 8
        height = 8
        for para in paragraphs:
            height += self.multi_cell(inner_w, 4.8, para, dry_run=True, output="HEIGHT") + 1.6
        height += 4
        self.ensure(height + 2)
        x, y = self.l_margin, self.get_y()
        self.set_fill_color(*WASH)
        self.set_draw_color(*RULE)
        self.rect(x, y, self.epw, height, "FD")
        self.set_xy(x + 4, y + 3)
        self.set_font("sans", "B", 9)
        self.set_text_color(*BLUE)
        self.multi_cell(inner_w, 4.6, title)
        self.set_text_color(*INK)
        self.set_font("sans", "", 10)
        for para in paragraphs:
            self.set_x(x + 4)
            self.multi_cell(inner_w, 4.8, para)
            self.ln(1.2)
        self.set_y(y + height + 3)


def build():
    pdf = Brief()
    pdf.add_page()
    pdf.set_font("sans", "B", 22)
    pdf.set_text_color(*NAVY)
    pdf.multi_cell(0, 9, "Brief for a crash course")
    pdf.ln(1)
    pdf.set_font("sans", "", 11)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(
        0,
        5.4,
        "Customer Development, the Validation Board, Scrum of Scrums, Large Scale Scrum, Kanban, and test-driven development. Written from the photographed exam, not from a full 60-item key.",
    )
    pdf.ln(2)
    pdf.set_text_color(*INK)

    pdf.box(
        "PASTE THIS WITH THE PDF",
        [
            "Build me a crash course from the attached brief. Teach the ideas in the concept sections. Treat the answer key as ground truth.",
            "Do not invent the missing exam questions, and do not present practice items as the original 60-item exam. The only known item numbers are 11, 14, 15, 16, 17, 18, 21, 22, 23, 24, 25, 27, 29, and 30.",
            "For each known item, show why the right choice is right and why every wrong choice fails. Write for an IT student who needs to pass the exam and also understand the ideas.",
            "Produce, in this order: a one-page map, five short lessons with one worked example each, an exam-phrase card, a drill of the 14 known items, and a separate 15-question practice set labeled PRACTICE. Plain language. No filler.",
            "If the user only says \"make the crash course\" or \"follow the brief,\" follow these rules and do not ask them to restate the material.",
        ],
    )

    pdf.h1("1. What the exam is testing")
    pdf.p(
        "The photographed paper has 60 items. These photos captured 14 of them. Every captured item asks the same kind of question: can you tell learning from building, an opinion from evidence, and one scaling rule from another?"
    )
    pdf.p(
        "The crash course should teach the frameworks those 14 items sit in. It should not pretend the other 46 items are known. Practice questions are allowed only when they are labeled PRACTICE and can be defended from this brief."
    )
    pdf.bullet("Score opinions, page views, and compliments as weak evidence.")
    pdf.bullet("Score access, money, time, and a real commitment as customer currency.")
    pdf.bullet("When an experiment fails, change the hypothesis. Keep the team.")
    pdf.bullet("Do not start with the solution, the architecture, or the model.")

    pdf.h1("2. The ideas, in the order to teach them")

    pdf.h2("A. Search first, then execute")
    pdf.p(
        "Steve Blank splits a new product into two modes. Search mode is hypothesis testing: who the customer is, what problem they have, and whether a solution is worth building. You expect to be wrong. Execution mode is scaling production software for a model that already has evidence."
    )
    pdf.note(
        "Exam 23 is true.",
        "IT startups and innovative teams should search before they transition into execution.",
    )

    pdf.h2("B. Get out of the building")
    pdf.p(
        "Get Out of the Building (GOOTB) is a Customer Development rule associated with Steve Blank. Leave the lab. Talk to real users. Watch what they do. Evidence collected in a meeting room, from the team’s own guesses, does not count."
    )
    pdf.note(
        "Exam 30 is true.",
        "The paper calls GOOTB a core Customer Development directive associated with Steve Blank, and it contrasts real users with sitting in the lab. Mark it true. Do not argue with the wording \"co-founded.\"",
    )

    pdf.h2("C. Fire the plan, not the team")
    pdf.p(
        "When an experiment invalidates a core technical or problem assumption, Lean and Customer Discovery discard the hypothesis. They do not discard the engineers. A pivot changes at least one core hypothesis: customer, problem, or solution. Replacing the student lead is not the method."
    )
    pdf.note(
        "Exam 14 is true.",
        "Fire the hypothesis or the plan. Do not fire the engineering team.",
    )

    pdf.h2("D. The Validation Board")
    pdf.p(
        "The Validation Board is the canvas from the Lean Startup Machine tradition. It tracks learning, not lines of code. Use one short sticky per box."
    )
    pdf.p("The three primary hypothesis stickies are Customer, Problem, and Solution.")
    pdf.bullet("**Customer.** A specific group that shares a pain, described so you could recognize them. Not a broad demographic.")
    pdf.bullet("**Problem.** That group’s pain, in their words. Not a societal trend.")
    pdf.bullet("**Solution.** What you believe will remove the pain. Write it late.")
    pdf.p(
        "A core assumption is any belief that would break the business if it were false. List several. Test only the single riskiest one. One failed core assumption is enough to drop the concept."
    )
    pdf.p(
        "The riskiest assumption is the core unproven belief with the least evidence, whose failure would make the entire software concept fail. It is not the hardest SQL query, the button color people argue about, or the largest cloud bill."
    )
    pdf.p(
        "The minimum success criterion is the weakest result the team will still accept as validation. Set it before the experiment, with the stakeholders in the room."
    )
    pdf.p(
        "After the experiment: if the result misses the criterion, pivot at least one core hypothesis. If it meets the criterion, pick the next riskiest assumption and test that. Track the pivots across the top of the board."
    )
    pdf.note(
        "Exam 27.",
        "The three sticky types are Customer, Problem, Solution. Agile/Scrum/Kanban, test stages, and frontend/backend/database are not the stickies.",
    )
    pdf.note(
        "Exam 24.",
        "Riskiest assumption: least evidence, and invalidating it kills the whole concept.",
    )
    pdf.note(
        "Exam 16, the order the paper scores.",
        "Customer Segment, then Problem Hypothesis, then Riskiest Assumption, then Solution Hypothesis. Do not start with the solution, the architecture, a Docker pipeline, or unit tests. The board’s own warning is: do not define a solution until the problem is validated.",
    )

    pdf.h2("E. Three methods, in rising cost")
    pdf.p("The board names exactly three experiment methods. Run the cheapest one that can answer the riskiest assumption. For this exam, Concierge and Wizard of Oz are the same move.")
    pdf.bullet("**Exploration.** Interviews and observation. Collect stories of real behavior. Learn the problem. Do not sell yet.")
    pdf.bullet("**Pitch.** Ask the customer to give something up in exchange for a solution: money, an email, time, access, or a signed commitment. That gift is currency. It tests whether the problem is a must-have.")
    pdf.bullet("**Concierge.** Also called Wizard of Oz on this paper. Deliver the service by hand to a few customers, with as little technology as possible. Build the system only after they value the result and act on it.")
    pdf.note(
        "Exam 17.",
        "Static code inspection is not one of the three. Exploration, Pitch, and Concierge are.",
    )

    pdf.h2("F. Opinions are not evidence")
    pdf.p(
        "Exam 11 is the worked case. A student team interviews 10 DevOps engineers about a cloud cost optimizer. Eight say AWS bill reduction is extremely important. Only one agrees to grant read-only IAM access so a sandbox script can audit a real cluster."
    )
    pdf.p(
        "The right reading: stated interest did not become customer currency. Pivot, or re-evaluate the customer and problem hypothesis. Do not persevere because 80 percent sounded keen. Do not fire the student lead and hire a consultant. Do not answer a failed commitment test by demanding administrative IAM. A bigger ask is not new evidence."
    )
    pdf.p(
        "Exam 25 is the vanity-metric case. One thousand unique page views on an open-source tool’s documentation do not prove that enterprise teams will pay a monthly license. The statement is false. Payment, or another real commitment, is the evidence. Traffic is not."
    )

    pdf.h2("G. Concierge, in the AI example")
    pdf.p(
        "Exam 21. A team reviews pull requests by hand and emails the feedback to 10 beta teams every evening. They postpone the machine-learning parser on purpose."
    )
    pdf.p(
        "The reason is to learn whether developers value the feedback and act on it before anyone invests in the model. It is not about AES-256 being stronger than an automated pipeline. It is not a Waterfall document gate. It is not a trick about patent protection."
    )

    pdf.h2("H. Scrum of Scrums is not LeSS")
    pdf.p("Both names show up in multi-team Scrum. They are not the same framework, and neither one is Waterfall or Kanban.")
    pdf.bullet("**Scrum of Scrums.** A coordination meeting. Representatives of the teams meet, often like a scaled daily standup, and surface dependencies and blockers. It is a technique. It does not require 1,000 developers.")
    pdf.bullet("**LeSS.** A framework for several teams building one product: one Product Owner, one Product Backlog, one shared sprint, feature teams, one Definition of Done.")
    pdf.note(
        "Exam 15 is false.",
        "LeSS does not give every feature team its own isolated Product Backlog.",
    )
    pdf.note(
        "Exam 22.",
        "SoS uses team representatives at a scaled standup. LeSS shares one Product Backlog and one sprint cadence. They are not identical. SoS is not Waterfall, LeSS is not Kanban, and the head-count options (1,000 developers, or a cap of 3) are not the difference.",
    )

    pdf.h2("I. Kanban does not run on sprints")
    pdf.p(
        "Scrum schedules work in fixed-length, timeboxed iterations called sprints. Kanban schedules by flow. People pull work when capacity frees up. A limit on work in progress is the control, not a sprint calendar."
    )
    pdf.note(
        "Exam 29 is false.",
        "Kanban does not rely on sprints to schedule releases.",
    )

    pdf.h2("J. Test-driven development writes the test first")
    pdf.p(
        "In Extreme Programming, test-driven development follows red, green, refactor. Red: write a unit test that fails because the behavior does not exist yet. Green: write the smallest production change that makes the test pass. Refactor: clean the code while the test stays green."
    )
    pdf.note(
        "Exam 18 is false.",
        "TDD does not say write the production code first and add the unit tests afterwards.",
    )

    pdf.h1("3. Answer key")
    pdf.p("Use these verdicts even if another source phrases the framework differently. This is the paper that was photographed.")

    key = [
        (
            "11",
            "Pivot or re-evaluate the problem and customer hypothesis. Eight engineers called bill reduction extremely important, and only one granted read-only IAM access. Verbal interest is not currency.",
            "Do not persevere on the 80 percent. Do not replace the student lead. Do not escalate the IAM request to admin.",
        ),
        (
            "14",
            "True. Fire the hypothesis or the plan, not the engineering team.",
            "A failed experiment is evidence about the assumption.",
        ),
        (
            "15",
            "False. LeSS uses one shared Product Backlog, not an isolated backlog per feature team.",
            "One Product Owner, one backlog, one sprint.",
        ),
        (
            "16",
            "Customer Segment, then Problem Hypothesis, then Riskiest Assumption, then Solution Hypothesis.",
            "Do not start from the riskiest assumption, a Docker pipeline, or the solution architecture.",
        ),
        (
            "17",
            "Static Code Inspection is not a validation method.",
            "The three methods are Exploration, Pitch, and Concierge.",
        ),
        (
            "18",
            "False. TDD writes the failing test before the production code.",
            "The cycle is red, green, refactor.",
        ),
        (
            "21",
            "The manual review checks that developers value and act on the feedback before the team builds the machine-learning pipeline.",
            "Not encryption, not a Waterfall gate, not a patent story.",
        ),
        (
            "22",
            "SoS is a meeting of team representatives. LeSS shares one Product Backlog and one sprint cadence.",
            "Not identical. Not Waterfall versus Kanban. Not a 1,000-person rule versus a 3-person cap.",
        ),
        (
            "23",
            "True. Search (hypothesis testing) comes before execution (scaling production software).",
            "Skipping search is how a team scales something nobody wants.",
        ),
        (
            "24",
            "The riskiest assumption is the unproven belief with the least evidence, whose failure kills the whole concept.",
            "Not the hardest query, the disputed button color, or the largest invoice.",
        ),
        (
            "25",
            "False. A thousand documentation page views do not prove enterprises will pay a license fee.",
            "Page views are a vanity metric. Payment is evidence.",
        ),
        (
            "27",
            "Customer, Problem, Solution.",
            "Not Agile/Scrum/Kanban, not the test pyramid, not frontend/backend/database.",
        ),
        (
            "29",
            "False. Kanban does not schedule releases with fixed sprints.",
            "Sprints belong to Scrum. Kanban is a flow with a work-in-progress limit.",
        ),
        (
            "30",
            "True. Get Out of the Building means collect evidence from real users instead of staying in the lab.",
            "Mark the statement true, including its attribution to Steve Blank.",
        ),
    ]
    for num, verdict, wrong in key:
        pdf.ensure(22)
        y = pdf.get_y()
        pdf.set_fill_color(*NAVY)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("sans", "B", 9)
        pdf.set_xy(16, y)
        pdf.cell(12, 6, num, align="C", fill=True)
        pdf.set_text_color(*INK)
        pdf.set_xy(30, y)
        pdf.set_font("sans", "B", 10.5)
        pdf.multi_cell(0, 5.1, verdict)
        pdf.set_x(30)
        pdf.set_font("sans", "", 10)
        pdf.set_text_color(*MUTED)
        pdf.multi_cell(0, 4.8, wrong)
        pdf.set_text_color(*INK)
        pdf.ln(2.2)

    pdf.h1("4. What the crash course must not do")
    pdf.bullet("Do not fabricate items 1–10, 12, 13, 19, 20, 26, 28, or 31–60, and do not number a practice item with one of those slots.")
    pdf.bullet("Do not teach SAFe, Nexus, or the Spotify model as if this paper used them. They were not in the photos.")
    pdf.bullet("Do not teach LeSS as \"each team owns a private backlog.\" The tested rule is one Product Backlog.")
    pdf.bullet("Do not split Concierge and Wizard of Oz into two methods. This paper uses them as one method.")
    pdf.bullet("Do not treat praise, a survey score, or page views as customer currency. Currency is something the customer gives up.")
    pdf.bullet("Do not start a lesson with the solution, the model, or the deployment pipeline.")

    pdf.h1("5. Shape of the crash course")
    pdf.p("Five lessons, then two drills. Each lesson gets one worked example and three sentences the student can say in an exam.")
    pdf.bullet("**Lesson 1.** Evidence before building. Search versus execution, GOOTB, and firing the plan. Example: a team that stays in the lab.")
    pdf.bullet("**Lesson 2.** The Validation Board, in the exam’s order, including how to pick the riskiest assumption and how to set a minimum success criterion.")
    pdf.bullet("**Lesson 3.** Exploration, Pitch, and Concierge. Work the cost-optimizer case and the handwritten code-review case.")
    pdf.bullet("**Lesson 4.** Scrum of Scrums versus LeSS, then Kanban versus sprints. One comparison table is enough.")
    pdf.bullet("**Lesson 5.** Test-driven development: red, green, refactor, with one tiny code example.")
    pdf.p(
        "After the lessons, print an exam-phrase card: one line per known item, in the words of the answer key. Then drill the 14 known items in a shuffled order, with the wrong choices explained. Finish with 15 new PRACTICE questions drawn only from sections 2 and 3, each marked PRACTICE, each with an answer and a one-line reason."
    )

    pdf.output(str(OUT))
    print(OUT, "pages", pdf.page)


if __name__ == "__main__":
    build()
