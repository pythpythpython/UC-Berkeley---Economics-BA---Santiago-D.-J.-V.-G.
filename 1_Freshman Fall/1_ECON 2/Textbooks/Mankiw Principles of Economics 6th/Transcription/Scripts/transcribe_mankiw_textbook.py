#!/usr/bin/env python3
"""
Mankiw Economics - Memory Optimized with VERBOSE Error Handling
"""

import os
import gc
import sys
import signal
from pathlib import Path
import pypdfium2 as pdfium

# Paths
SCRIPT_DIR = Path(__file__).parent
BASE_DIR = SCRIPT_DIR.parent.parent
PDF_PATH = BASE_DIR / "PDF" / "Mankiw Principles of Economics 6th.pdf"
OUTPUT_DIR = BASE_DIR / "Transcription"
PAGE_OFFSET = 34

# Signal handler for graceful termination
def signal_handler(sig, frame):
    print("\n\n" + "="*70)
    print("⚠️  INTERRUPTED BY USER (Ctrl+C)")
    print("="*70)
    print("Progress saved. Run again to resume from last completed chapter.")
    print("="*70)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# ALL 36 CHAPTERS
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


def get_output_path(ch):
    part_dir = OUTPUT_DIR / ch['part'].replace(' ', '_')
    safe_title = ch['title'].replace(' ', '_').replace(':', '').replace(',', '')
    filename = f"Chapter_{ch['chapter']:02d}_{safe_title}.md"
    return part_dir / filename


def is_chapter_complete(ch):
    output_path = get_output_path(ch)
    return output_path.exists() and output_path.stat().st_size > 100


def extract_images(pdf_path, start_page, end_page):
    pdf_start = (start_page + PAGE_OFFSET) - 1
    pdf_end = (end_page + PAGE_OFFSET)

    pdf = pdfium.PdfDocument(str(pdf_path))
    images = []

    for page_idx in range(pdf_start, min(pdf_end, len(pdf))):
        page = pdf[page_idx]
        bitmap = page.render(scale=1.5)
        pil_image = bitmap.to_pil()
        images.append(pil_image)

    pdf.close()
    return images


def transcribe_chapter(ch):
    print(f"\n{'='*70}")
    print(f"Chapter {ch['chapter']}: {ch['title']}")
    print(f"{'='*70}")

    if is_chapter_complete(ch):
        print("  ⏩ Already complete, skipping...")
        return True

    try:
        # Step 1: Extract
        print("  [1/4] Extracting pages...")
        sys.stdout.flush()
        images = extract_images(PDF_PATH, ch['start_page'], ch['end_page'])
        print(f"  ✓ {len(images)} pages extracted")
        sys.stdout.flush()

        # Step 2: Load models
        if not hasattr(transcribe_chapter, 'predictors'):
            print("  [2/4] Loading Surya predictors...")
            print("  ⏳ Downloading models (~3GB, one-time)...")
            print("  ⏳ This takes 2-5 minutes on first run...")
            print("  ⏳ DO NOT interrupt - models cache after download!")
            sys.stdout.flush()

            try:
                from surya.models import load_predictors
                print("  ⏳ Starting model download...")
                sys.stdout.flush()
                transcribe_chapter.predictors = load_predictors()
                print("  ✓ Models loaded and cached!")
                sys.stdout.flush()
            except KeyboardInterrupt:
                print("\n\n⚠️  INTERRUPTED during model download!")
                print("Models partially downloaded. Run again to resume.")
                raise
            except MemoryError as e:
                print(f"\n\n❌ OUT OF MEMORY during model loading!")
                print(f"Error: {e}")
                print("\nTroubleshooting:")
                print("1. Close other applications")
                print("2. Restart codespace for clean memory")
                print("3. Contact support if issue persists")
                raise
            except Exception as e:
                print(f"\n\n❌ ERROR loading models: {type(e).__name__}")
                print(f"Details: {e}")
                raise
        else:
            print("  [2/4] Using cached predictors ✓")
            sys.stdout.flush()

        # Step 3: Detection
        print("  [3/4] Detecting text regions...")
        sys.stdout.flush()
        det = transcribe_chapter.predictors['detection'](images)
        print("  ✓ Detection complete")
        sys.stdout.flush()

        # Step 4: Recognition
        print("  [4/4] Running OCR recognition...")
        sys.stdout.flush()
        ocr = transcribe_chapter.predictors['recognition'](images, det)
        print("  ✓ OCR complete")
        sys.stdout.flush()

        # Build markdown
        md = f"# Chapter {ch['chapter']}: {ch['title']}\n\n**{ch['part']}**\n\n---\n\n"

        for i, result in enumerate(ocr):
            md += f"\n## Page {ch['start_page'] + i}\n\n"
            if hasattr(result, 'text_lines'):
                for line in result.text_lines:
                    md += getattr(line, 'text', '') + "\n"
            md += "\n"

        # Save
        output_path = get_output_path(ch)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(md)

        print(f"  ✓ Saved: {output_path.stat().st_size / 1024:.1f} KB")
        sys.stdout.flush()

        # Memory cleanup
        del images, det, ocr
        gc.collect()

        return True

    except KeyboardInterrupt:
        raise
    except MemoryError as e:
        print(f"\n  ❌ OUT OF MEMORY!")
        print(f"  Chapter {ch['chapter']} failed due to memory constraints")
        print(f"  Try closing other applications and running again")
        return False
    except Exception as e:
        print(f"\n  ❌ ERROR: {type(e).__name__}")
        print(f"  Details: {e}")
        import traceback
        print("\n  Full traceback:")
        traceback.print_exc()
        return False


def main():
    print("="*70)
    print("Mankiw Economics - Surya OCR (Memory Optimized + Verbose)")
    print("="*70)
    print(f"PDF: {PDF_PATH.stat().st_size / 1024 / 1024:.1f} MB")
    print(f"Output: {OUTPUT_DIR}")
    print(f"\n⚠️  First run downloads ~3GB models (one-time, 2-5 min)")
    print("⚠️  Process can be resumed if interrupted")
    print("⚠️  Press Ctrl+C to safely stop")
    print("="*70)
    sys.stdout.flush()

    success = 0
    failed = 0
    skipped = 0
    failed_chapters = []

    try:
        for ch in CHAPTERS:
            result = transcribe_chapter(ch)
            if result:
                if is_chapter_complete(ch):
                    success += 1
                else:
                    skipped += 1
            else:
                failed += 1
                failed_chapters.append(ch['chapter'])
    except KeyboardInterrupt:
        print("\n\n" + "="*70)
        print("⚠️  STOPPED BY USER")
        print("="*70)

    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Completed: {success}/{len(CHAPTERS)}")
    if skipped > 0:
        print(f"Skipped: {skipped} (already done)")
    if failed > 0:
        print(f"Failed: {failed} chapters - {failed_chapters}")
    print(f"\nOutput: {OUTPUT_DIR}")
    print("="*70)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("\n\n" + "="*70)
        print("❌ FATAL ERROR")
        print("="*70)
        print(f"Type: {type(e).__name__}")
        print(f"Message: {e}")
        print("\nFull traceback:")
        import traceback
        traceback.print_exc()
        print("="*70)
        sys.exit(1)