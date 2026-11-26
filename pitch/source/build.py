"""Rebuild the pitch deck: deck.html -> slide PNGs -> PPTX (notes, appendix hidden) + PDFs.

Usage: python3 pitch/source/build.py   (needs Google Chrome, python-pptx, Pillow)
Slides 1-9 are the pitch; 10-15 are hidden appendix slides for questions.
Speaker notes come from pitch/SPEAKER_NOTES.md (sections "## N · ...").
"""
import re, subprocess, sys, tempfile
from pathlib import Path
from PIL import Image
from pptx import Presentation
from pptx.util import Emu

HERE = Path(__file__).resolve().parent
PITCH = HERE.parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
N_MAIN, N_ALL = 9, 15

APPENDIX_NOTES = {
    10: "Appendix · Architecture — Anthony. Workflow, not agent: browser previews, FastAPI server re-checks every recorded action (HTTP 422 on a refused edit), engine is the authority. Parity tests keep browser and server identical (123 cases).",
    11: "Appendix · Metrics — Colin. Business numbers, quality and safety guardrails, counter-metrics against Goodhart (reopens, hand-overs, edit rate), segments fixed before the test.",
    12: "Appendix · AI judge — Anthony. 53 % -> 73 % agreement after one rubric fix, below the 80 % bar, so not trusted alone. 41/41 bad drafts escalated. Found the wrong-language defect (S5-M01).",
    13: "Appendix · Experiment — Colin. Unit = specialist-day. ~600 per arm for time, ~2,210 for reopens, x1.54 clustering -> ~3,400 per arm, 7 weeks. MDE 13 % = below it we lose to doing nothing.",
    14: "Appendix · Build or buy — Benjamin. Orchestrate 4.35 / build 3.15 / buy 2.15. A vendor at €0.92 per resolution is ~€34k a year cheaper; we pay for data control and the ability to leave.",
    15: "Appendix · Launch gates — Lenny. Stage 0 synthetic, Stage 1 staging (the ask), Stage 2 pilot A/B, Stage 3 expansion with a 5 % holdout for 6 months. Each gate has a signer.",
}


def notes_from_script():
    text = (PITCH / "SPEAKER_NOTES.md").read_text()
    notes = {}
    for m in re.finditer(r"^## (\d+) · (.+?)\n(.*?)(?=^## |^---)", text, re.S | re.M):
        body = re.sub(r"^> ?", "", m.group(3), flags=re.M)
        body = body.replace("**", "").replace("*", "").replace("`", "")
        notes[int(m.group(1))] = f"{m.group(2)}\n\n{body.strip()}"
    return notes


def render(out):
    for i in range(1, N_ALL + 1):
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        "--window-size=1920,1080", "--virtual-time-budget=6000",
                        f"--screenshot={out}/s{i:02d}.png", f"file://{HERE}/deck.html?s={i}"],
                       check=True, capture_output=True)


def main():
    notes = notes_from_script() | APPENDIX_NOTES
    with tempfile.TemporaryDirectory() as tmp:
        render(tmp)
        pngs = [Path(tmp) / f"s{i:02d}.png" for i in range(1, N_ALL + 1)]
        prs = Presentation()
        prs.slide_width, prs.slide_height = Emu(12192000), Emu(6858000)
        for i, png in enumerate(pngs, 1):
            s = prs.slides.add_slide(prs.slide_layouts[6])
            s.shapes.add_picture(str(png), 0, 0, prs.slide_width, prs.slide_height)
            s.notes_slide.notes_text_frame.text = notes.get(i, "")
            if i > N_MAIN:
                s._element.set("show", "0")
        prs.save(PITCH / "FlowAssist_Final_Pitch.pptx")
        ims = [Image.open(p).convert("RGB") for p in pngs]
        ims[0].save(PITCH / "FlowAssist_Final_Pitch.pdf", save_all=True, append_images=ims[1:N_MAIN], resolution=144)
        ims[0].save(PITCH / "FlowAssist_Final_Pitch_with_appendix.pdf", save_all=True, append_images=ims[1:], resolution=144)
    print("built", PITCH / "FlowAssist_Final_Pitch.pptx")


if __name__ == "__main__":
    sys.exit(main())
