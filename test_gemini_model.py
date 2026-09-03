import argparse
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env", override=True)


def build_test_image(text: str = "OCR TEST 123") -> bytes:
    img = Image.new("RGB", (900, 220), "white")
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 72)
    except OSError:
        font = ImageFont.load_default()

    draw.text((50, 60), text, fill="black", font=font)
    png_bytes = __import__("io").BytesIO()
    img.save(png_bytes, format="PNG")
    return png_bytes.getvalue()


def try_text_call(client: genai.Client, model: str) -> str:
    response = client.models.generate_content(
        model=model,
        contents="Reply with exactly: OK"
    )
    return str(response.text).strip()


def try_ocr_call(client: genai.Client, model: str) -> str:
    image_bytes = build_test_image()
    image_part = types.Part.from_bytes(
        data=image_bytes,
        mime_type="image/png",
    )
    response = client.models.generate_content(
        model=model,
        contents=[
            image_part,
            "Return only the exact text visible in the image. No explanation."
        ]
    )
    return str(response.text).strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a Gemini API key and test model compatibility for OCR/image input.")
    parser.add_argument("--model", help="Gemini model to test, e.g. gemini-2.0-flash")
    args = parser.parse_args()

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise SystemExit("GOOGLE_API_KEY is not set. Add it to .env or export it before running this script.")

    candidate_models = []
    if args.model:
        candidate_models.append(args.model)
    env_model = os.getenv("GEMINI_MODEL")
    if env_model:
        candidate_models.append(env_model)
    candidate_models.extend([
        "gemini-2.0-flash",
        "gemini-2.5-flash",
        "gemini-2.0-flash-lite",
    ])

    seen = set()
    candidate_models = [m for m in candidate_models if m and m not in seen and not seen.add(m)]

    print(f"Using API key: {api_key[:6]}...{api_key[-4:]} (length={len(api_key)})")
    print(f"Working directory: {ROOT}")

    client = genai.Client(api_key=api_key)

    for model in candidate_models:
        print(f"\nTesting model: {model}")
        try:
            text_response = try_text_call(client, model)
            print(f"  text call result: {text_response}")
        except Exception as e:
            print(f"  text call failed: {type(e).__name__}: {e}")
            continue

        try:
            ocr_response = try_ocr_call(client, model)
            print(f"  OCR smoke test result: {ocr_response}")
            print(f"  => MODEL WORKS: {model}")
            return
        except Exception as e:
            print(f"  OCR smoke test failed: {type(e).__name__}: {e}")

    print("\nNo tested model succeeded for both text and OCR/image input.")
    print("Try another Gemini model available in your Google AI Studio account.")


if __name__ == "__main__":
    main()
