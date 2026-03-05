"""
CAPTCHA Implementation
======================
Generates image-based CAPTCHAs using PIL/Pillow with:
  - Random alphanumeric text
  - Noise pixels
  - Distorted lines
  - Skewed characters
"""

import random
import string
import io
import base64
from PIL import Image, ImageDraw, ImageFont, ImageFilter


# ─────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────
WIDTH       = 200
HEIGHT      = 80
TEXT_LEN    = 6
NOISE_DOTS  = 200
NOISE_LINES = 8
BG_COLOR    = (255, 255, 255)


# ─────────────────────────────────────────────
# HELPER: random colour
# ─────────────────────────────────────────────
def _rand_color(dark: bool = True):
    if dark:
        return tuple(random.randint(0, 120) for _ in range(3))
    return tuple(random.randint(180, 255) for _ in range(3))


# ─────────────────────────────────────────────
# STEP 1 – Generate random text
# ─────────────────────────────────────────────
def generate_captcha_text(length: int = TEXT_LEN) -> str:
    """Return a random alphanumeric string (ambiguous chars removed)."""
    chars = (
        string.ascii_uppercase.replace("O", "").replace("I", "")
        + string.digits.replace("0", "").replace("1", "")
    )
    return "".join(random.choices(chars, k=length))


# ─────────────────────────────────────────────
# STEP 2 – Draw background noise
# ─────────────────────────────────────────────
def _add_noise(draw: ImageDraw.Draw):
    # Random dots
    for _ in range(NOISE_DOTS):
        x = random.randint(0, WIDTH - 1)
        y = random.randint(0, HEIGHT - 1)
        draw.point((x, y), fill=_rand_color(dark=False))

    # Random lines
    for _ in range(NOISE_LINES):
        x1, y1 = random.randint(0, WIDTH), random.randint(0, HEIGHT)
        x2, y2 = random.randint(0, WIDTH), random.randint(0, HEIGHT)
        draw.line([(x1, y1), (x2, y2)], fill=_rand_color(dark=False), width=1)


# ─────────────────────────────────────────────
# STEP 3 – Render text with individual offsets
# ─────────────────────────────────────────────
def _draw_text(draw: ImageDraw.Draw, text: str):
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", size=40)
    except IOError:
        font = ImageFont.load_default()

    x = 10
    for ch in text:
        y_offset = random.randint(-8, 8)
        angle    = random.randint(-25, 25)

        # Render each character onto a tiny temp image and rotate it
        char_img = Image.new("RGBA", (40, 60), (255, 255, 255, 0))
        char_draw = ImageDraw.Draw(char_img)
        char_draw.text((5, 8), ch, font=font, fill=_rand_color())
        rotated = char_img.rotate(angle, expand=True)

        # Paste onto the main canvas
        paste_y = max(0, (HEIGHT // 2) - rotated.height // 2 + y_offset)
        draw._image.paste(rotated, (x, paste_y), rotated)
        x += 28


# ─────────────────────────────────────────────
# STEP 4 – Apply subtle blur / distortion
# ─────────────────────────────────────────────
def _distort(img: Image.Image) -> Image.Image:
    return img.filter(ImageFilter.SMOOTH)


# ─────────────────────────────────────────────
# PUBLIC API
# ─────────────────────────────────────────────
def create_captcha() -> tuple[str, Image.Image]:
    """
    Create a CAPTCHA.

    Returns
    -------
    (text, image)
        text  – the correct answer
        image – PIL Image object
    """
    text = generate_captcha_text()
    img  = Image.new("RGB", (WIDTH, HEIGHT), color=BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw._image = img          # back-reference so _draw_text can paste sub-images

    _add_noise(draw)
    _draw_text(draw, text)
    img = _distort(img)
    return text, img


def captcha_to_base64(img: Image.Image) -> str:
    """Encode a PIL Image to a base-64 PNG string (useful for web embedding)."""
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()


# ─────────────────────────────────────────────
# CAPTCHA SESSION (simple in-memory store)
# ─────────────────────────────────────────────
class CaptchaSession:
    """
    Lightweight session wrapper.

    Usage
    -----
    session = CaptchaSession()
    session.new()          → generates & stores a new challenge
    session.verify(guess)  → True / False, then auto-refreshes
    """

    def __init__(self):
        self._answer: str | None = None
        self._image:  Image.Image | None = None

    def new(self) -> Image.Image:
        """Generate a fresh CAPTCHA and store the answer."""
        self._answer, self._image = create_captcha()
        return self._image

    def verify(self, user_input: str) -> bool:
        """Check the user's answer (case-insensitive)."""
        if self._answer is None:
            raise RuntimeError("No active CAPTCHA – call new() first.")
        result = user_input.strip().upper() == self._answer.upper()
        self.new()          # always refresh after an attempt
        return result

    @property
    def image(self) -> Image.Image | None:
        return self._image


# ─────────────────────────────────────────────
# DEMO / CLI
# ─────────────────────────────────────────────
def main():
    print("=" * 50)
    print("  CAPTCHA Demo")
    print("=" * 50)

    session = CaptchaSession()
    session.new()

    # Save to file for inspection
    out_path = "captcha_sample.png"
    session.image.save(out_path)
    print(f"CAPTCHA image saved → {out_path}")
    print("(Open the image, then type what you see.)\n")

    for attempt in range(1, 4):
        guess = input(f"Attempt {attempt}/3 – Enter CAPTCHA text: ").strip()
        if session.verify(guess):
            print("✅  Correct! Access granted.\n")
            break
        else:
            print("❌  Wrong. A new CAPTCHA has been generated.")
            session.image.save(out_path)
            print(f"    New image saved → {out_path}\n")
    else:
        print("🚫  Too many failed attempts. Access denied.")


if __name__ == "__main__":
    main()
