#!/usr/bin/env python3
"""
Mankiw Principles of Economics 6th Edition - Complete Transcription
Using PyMuPDF for lightweight, fast text extraction
"""

from pathlib import Path
import fitz  # PyMuPDF

# Absolute path (works from anywhere)
BASE_DIR = Path("/workspaces/UC-Berkeley---Economics-BA---Santiago-D.-J.-V.-G./1_Freshman Fall/1_ECON 2/Textbooks/Mankiw Principles of Economics 6th")
PDF_PATH = BASE_DIR / "PDF" / "Mankiw Principles of Economics 6th.pdf"
OUTPUT_DIR = BASE_DIR / "Transcription"
PAGE_OFFSET = 34

# All 36 chapters
CHAPTERS = [
    {"part": "Part I", "chapter": 1, "title": "Ten Principles of Economics", "start_page": 3, "end_page": 20},
    {"part": "Part I", "chapter": 2, "title": "Thinking Like an Economist", "start_page": 21, "end_page": 48},
    {"part": "Part I", "chapter": 3, "title": "Interdependence and the Gains from Trade", "start_page": 49, "end_page": 62},
    {"part": "Part II", "chapter": 4, "title": "The Market Forces of Supply and Demand", "start_page": 65, "end_page": 88},
    {"part": "Part II", "chapter": 5, "title": "Elasticity and Its Application", "start_page": 89, "end_page": 110},
    {"part": "Part II", "chapter": 6, "title": "Supply, Demand, and Government Policies", "start_page": 111, "end_page": 132},
    {"part": "Part III", "chapter": 7, "title": "Consumers, Producers, and the Efficiency of Markets", "start_page": 135, "end_page": 154},
    {"part": "Part III", "chapter": 8, "title": "Application: The Costs of Taxation", "start_page": 155, "end_page": 170},
    {"part": "Part III", "chapter": 9, "title": "Application: International Trade", "start_page": 171, "end_page": 192},
    {"part": "Part IV", "chapter": 10, "title": "Externalities", "start_page": 195, "end_page": 216},
    {"part": "Part IV", "chapter": 11, "title": "Public Goods and Common Resources", "start_page": 217, "end_page": 232},
    {"part": "Part IV", "chapter": 12, "title": "The Design of the Tax System", "start_page": 233, "end_page": 256},
    {"part": "Part V", "chapter": 13, "title": "The Costs of Production", "start_page": 259, "end_page": 278},
    {"part": "Part V", "chapter": 14, "title": "Firms in Competitive Markets", "start_page": 279, "end_page": 298},
    {"part": "Part V", "chapter": 15, "title": "Monopoly", "start_page": 299, "end_page": 328},
    {"part": "Part V", "chapter": 16, "title": "Monopolistic Competition", "start_page": 329, "end_page": 348},
    {"part": "Part V", "chapter": 17, "title": "Oligopoly", "start_page": 349, "end_page": 372},
    {"part": "Part VI", "chapter": 18, "title": "The Markets for the Factors of Production", "start_page": 375, "end_page": 396},
    {"part": "Part VI", "chapter": 19, "title": "Earnings and Discrimination", "start_page": 397, "end_page": 414},
    {"part": "Part VI", "chapter": 20, "title": "Income Inequality and Poverty", "start_page": 415, "end_page": 436},
    {"part": "Part VII", "chapter": 21, "title": "The Theory of Consumer Choice", "start_page": 439, "end_page": 466},
    {"part": "Part VII", "chapter": 22, "title": "Frontiers of Microeconomics", "start_page": 467, "end_page": 488},
    {"part": "Part VIII", "chapter": 23, "title": "Measuring a Nation's Income", "start_page": 491, "end_page": 512},
    {"part": "Part VIII", "chapter": 24, "title": "Measuring the Cost of Living", "start_page": 513, "end_page": 528},
    {"part": "Part IX", "chapter": 25, "title": "Production and Growth", "start_page": 531, "end_page": 554},
    {"part": "Part IX", "chapter": 26, "title": "Saving, Investment, and the Financial System", "start_page": 555, "end_page": 576},
    {"part": "Part IX", "chapter": 27, "title": "The Basic Tools of Finance", "start_page": 577, "end_page": 592},
    {"part": "Part IX", "chapter": 28, "title": "Unemployment", "start_page": 593, "end_page": 616},
    {"part": "Part X", "chapter": 29, "title": "The Monetary System", "start_page": 619, "end_page": 642},
    {"part": "Part X", "chapter": 30, "title": "Money Growth and Inflation", "start_page": 643, "end_page": 668},
    {"part": "Part XI", "chapter": 31, "title": "Open-Economy Macroeconomics: Basic Concepts", "start_page": 671, "end_page": 694},
    {"part": "Part XI", "chapter": 32, "title": "A Macroeconomic Theory of the Open Economy", "start_page": 695, "end_page": 716},
    {"part": "Part XII", "chapter": 33, "title": "Aggregate Demand and Aggregate Supply", "start_page": 719, "end_page": 756},
    {"part": "Part XII", "chapter": 34, "title": "The Influence of Monetary and Fiscal Policy on Aggregate Demand", "start_page": 757, "end_page": 784},
    {"part": "Part XII", "chapter": 35, "title": "The Short-Run Trade-off between Inflation and Unemployment", "start_page": 785, "end_page": 808},
    {"part": "Part XIII", "chapter": 36, "title": "Six Debates over Macroeconomic Policy", "start_page": 811, "end_page": 832},
]


def extract_text(pdf_path, start_page, end_page):
    """Extract text from PDF pages"""
    pdf_start = (start_page + PAGE_OFFSET) - 1
    pdf_end = (end_page + PAGE_OFFSET)

    doc = fitz.open(str(pdf_path))
    text_by_page = []

    for page_num in range(pdf_start, min(pdf_end, len(doc))):
        page = doc[page_num]
        text = page.get_text("text")
        text_by_page.append(text)

    doc.close()
    return text_by_page


def get_output_path(ch):
    """Get output file path for a chapter"""
    part_dir = OUTPUT_DIR / ch['part'].replace(' ', '_')
    safe_title = ch['title'].replace(' ', '_').replace(':', '').replace(',', '')
    filename = f"Chapter_{ch['chapter']:02d}_{safe_title}.md"
    return part_dir / filename


def is_complete(ch):
    """Check if chapter already transcribed"""
    output_path = get_output_path(ch)
    return output_path.exists() and output_path.stat().st_size > 100


def transcribe_chapter(ch):
    """Transcribe one chapter"""
    print(f"\nChapter {ch['chapter']}: {ch['title']}")

    # Skip if done
    if is_complete(ch):
        print("  ⏩ Already complete")
        return True

    try:
        # Extract text
        print(f"  Extracting {ch['end_page'] - ch['start_page'] + 1} pages...")
        pages = extract_text(PDF_PATH, ch['start_page'], ch['end_page'])

        # Build markdown
        md = f"""# Chapter {ch['chapter']}: {ch['title']}

**{ch['part']}**

---

"""

        for i, page_text in enumerate(pages):
            page_num = ch['start_page'] + i
            md += f"## Page {page_num}\n\n{page_text}\n\n"

        # Save
        output_path = get_output_path(ch)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md)

        print(f"  ✓ Saved ({output_path.stat().st_size / 1024:.1f} KB)")
        return True

    except Exception as e:
        print(f"  ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("="*70)
    print("Mankiw Principles of Economics 6th Edition")
    print("PyMuPDF Text Extraction")
    print("="*70)

    if not PDF_PATH.exists():
        print(f"\n✗ PDF not found: {PDF_PATH}")
        return

    print(f"PDF: {PDF_PATH.stat().st_size / 1024 / 1024:.1f} MB")
    print(f"Output: {OUTPUT_DIR}")
    print(f"\nProcessing {len(CHAPTERS)} chapters...")
    print("="*70)

    success = 0
    failed = 0
    skipped = 0

    for ch in CHAPTERS:
        if transcribe_chapter(ch):
            if is_complete(ch):
                success += 1
            else:
                skipped += 1
        else:
            failed += 1

    print("\n" + "="*70)
    print("COMPLETE")
    print("="*70)
    print(f"Success: {success}/{len(CHAPTERS)}")
    if skipped > 0:
        print(f"Skipped: {skipped} (already done)")
    if failed > 0:
        print(f"Failed: {failed}")
    print(f"\nOutput: {OUTPUT_DIR}")
    print("="*70)


if __name__ == "__main__":
    main()