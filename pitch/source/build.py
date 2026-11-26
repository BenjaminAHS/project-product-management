"""Rebuild the pitch deck: deck.html -> slide PNGs -> PPTX (notes, appendix hidden) + PDFs.

Usage: python3 pitch/source/build.py   (needs Google Chrome, python-pptx, Pillow; PyMuPDF for PDF links)
Slides 1-9 are the pitch; 10-15 are hidden appendix slides for questions.
Slide 5: clicking the app screenshot plays the demo video (embedded in the PPTX, link in the PDFs to the same video on the live site).
Speaker notes come from pitch/SPEAKER_NOTES.md (sections "## N · ...").
"""
import os, re, shutil, subprocess, sys, tempfile
from pathlib import Path
from PIL import Image
from pptx import Presentation
from pptx.util import Emu

HERE = Path(__file__).resolve().parent
PITCH = HERE.parent
CHROME = os.environ.get("CHROME") or next(
    (c for c in ("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                 r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                 shutil.which("google-chrome") or "") if c and Path(c).exists()), "chrome")
N_MAIN, N_ALL = 9, 15

# Recorded demo: embedded in the PPTX (offline, plays full screen on click) and linked from the PDFs (served by the live site at /demo.mp4).
# The zone is the app screenshot on slide 5, in 1920x1080 px.
DEMO_VIDEO = PITCH / "FlowAssist_Demo.mp4"
DEMO_URL = "https://deploy-project-product-management.vercel.app/demo.mp4"
DEMO_SLIDE, DEMO_BOX = 5, (1030, 330, 750, 640)  # left, top, width, height

APPENDIX_NOTES = {
    10: "Appendix · Architecture — Anthony. Workflow, not agent: browser previews, FastAPI server re-checks every recorded action (HTTP 422 on a refused edit), engine is the authority. Parity tests keep browser and server identical (123 cases).",
    11: "Appendix · Metrics — Benjamin. Business numbers, quality and safety guardrails, counter-metrics against Goodhart (reopens, hand-overs, edit rate), segments fixed before the test.",
    12: "Appendix · AI judge — Anthony. 53 % -> 73 % agreement after one rubric fix, below the 80 % bar, so not trusted alone. 41/41 bad drafts escalated. Found the wrong-language defect (S5-M01).",
    13: "Appendix · Experiment — Benjamin. Unit = specialist-day. ~600 per arm for time, ~2,210 for reopens, x1.54 clustering -> ~3,400 per arm, 7 weeks. MDE 13 % = below it we lose to doing nothing.",
    14: "Appendix · Build or buy — Benjamin. Orchestrate 4.35 / build 3.15 / buy 2.15. A vendor at €0.92 per resolution is ~€34k a year cheaper; we pay for data control and the ability to leave.",
    15: "Appendix · Launch gates — Lenny. Stage 0 synthetic, Stage 1 staging (the ask), Stage 2 pilot A/B, Stage 3 expansion with a 5 % holdout for 6 months. Each gate has a signer.",
}


def notes_from_script():
    text = (PITCH / "SPEAKER_NOTES.md").read_text(encoding="utf-8")
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
                        f"--screenshot={Path(out) / f's{i:02d}.png'}", f"{(HERE / 'deck.html').as_uri()}?s={i}"],
                       check=True, capture_output=True)


DEMO_TIMING = (
    '<p:timing {ns}><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst>'
    '<p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>'
    '<p:par><p:cTn id="3" fill="hold"><p:stCondLst><p:cond delay="indefinite"/></p:stCondLst><p:childTnLst>'
    '<p:par><p:cTn id="4" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>'
    '<p:par><p:cTn id="5" presetID="1" presetClass="mediacall" presetSubtype="0" fill="hold" nodeType="clickEffect">'
    '<p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst><p:cmd type="call" cmd="playFrom(0.0)"><p:cBhvr>'
    '<p:cTn id="6" dur="1" fill="hold"/><p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl></p:cBhvr></p:cmd>'
    '</p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par>'
    '</p:childTnLst></p:cTn>'
    '<p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>'
    '<p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst></p:seq>'
    '<p:video fullScrn="1"><p:cMediaNode vol="80000"><p:cTn id="7" fill="hold" display="0">'
    '<p:stCondLst><p:cond delay="indefinite"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl>'
    '</p:cMediaNode></p:video></p:childTnLst></p:cTn></p:par></p:tnLst></p:timing>'
)


def embed_demo(slide, prs, slide_png):
    """Embed the demo video over the screenshot: click it in slide show, it plays full screen.
    The poster frame is the screenshot itself, so the slide looks the same as in the PDFs."""
    from pptx.oxml import parse_xml
    from pptx.oxml.ns import nsdecls, qn
    left, top, width, height = DEMO_BOX
    poster = Path(slide_png).with_name("demo_poster.png")
    Image.open(slide_png).crop((left, top, left + width, top + height)).save(poster)
    x, y, w, h = (round(v * prs.slide_width / 1920) for v in DEMO_BOX)
    movie = slide.shapes.add_movie(str(DEMO_VIDEO), x, y, w, h, poster_frame_image=str(poster), mime_type="video/mp4")
    movie.name = "Demo video"
    # Timing as PowerPoint writes it for "play on click, full screen": the next click or the
    # clicker starts the video, the click after that goes to slide 6.
    old_timing = slide._element.find(qn("p:timing"))
    slide._element.replace(old_timing, parse_xml(DEMO_TIMING.format(ns=nsdecls("p"), spid=movie.shape_id)))


def link_pdf(path):
    """Add a URI link over the screenshot on the demo page (skipped if PyMuPDF is missing)."""
    try:
        import pymupdf
    except ImportError:
        print("PyMuPDF not installed: PDFs built without the demo link")
        return
    doc = pymupdf.open(path)
    page = doc[DEMO_SLIDE - 1]
    k = page.rect.width / 1920
    x, y, w, h = DEMO_BOX
    page.insert_link({"kind": pymupdf.LINK_URI, "from": pymupdf.Rect(x * k, y * k, (x + w) * k, (y + h) * k), "uri": DEMO_URL})
    doc.save(path, incremental=True, encryption=pymupdf.PDF_ENCRYPT_KEEP)


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
            if i == DEMO_SLIDE:
                embed_demo(s, prs, png)
        prs.save(PITCH / "FlowAssist_Final_Pitch.pptx")
        ims = [Image.open(p).convert("RGB") for p in pngs]
        ims[0].save(PITCH / "FlowAssist_Final_Pitch.pdf", save_all=True, append_images=ims[1:N_MAIN], resolution=144)
        ims[0].save(PITCH / "FlowAssist_Final_Pitch_with_appendix.pdf", save_all=True, append_images=ims[1:], resolution=144)
        for pdf in ("FlowAssist_Final_Pitch.pdf", "FlowAssist_Final_Pitch_with_appendix.pdf"):
            link_pdf(PITCH / pdf)
    print("built", PITCH / "FlowAssist_Final_Pitch.pptx")


if __name__ == "__main__":
    sys.exit(main())
