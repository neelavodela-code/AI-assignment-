# Problem 1 – Turing Test & CAPTCHA

> **Course:** Artificial Intelligence Lab  
> **Topic:** Human–Machine Distinction Mechanisms  
> **Language:** Python 3.10+

---

## 📌 Overview

This repository contains two independent Python implementations that explore the boundary between human and machine interaction:

| File | Purpose |
|------|---------|
| `captcha.py` | Image-based CAPTCHA generator & verifier |
| `turing_test.py` | Interactive Turing Test simulator |

---

## 🧠 Theoretical Background

### Turing Test
Proposed by Alan Turing in 1950, the **Turing Test** evaluates whether a machine can exhibit intelligent behaviour indistinguishable from that of a human. A human **Judge** interrogates two hidden participants — one human, one machine — through text only. If the Judge cannot reliably identify the machine, the machine is said to have passed the test.

**Architecture used here:**

```
TuringTestSession
├── Judge          ← human (stdin)
├── PlayerA        ← randomly assigned (Human or AI)
└── PlayerB        ← randomly assigned (AI or Human)
         │
         └── AIPlayer  ← rule-based chatbot (regex + fallbacks)
```

### CAPTCHA
**CAPTCHA** (*Completely Automated Public Turing test to tell Computers and Humans Apart*) is the inverse problem: a computer challenges a human to prove they are not a bot. The challenge exploits tasks that humans solve easily but machines (historically) cannot — such as reading distorted text in a noisy image.

**Architecture used here:**

```
CaptchaSession
├── generate_captcha_text()   ← random alphanumeric string
├── _add_noise()              ← random dots + lines
├── _draw_text()              ← per-character rotation & y-jitter
├── _distort()                ← PIL smooth filter
└── verify(user_input)        ← case-insensitive string match
```

---

## 🗂 File Structure

```
├── captcha.py          # CAPTCHA generator
├── turing_test.py      # Turing Test simulator
├── captcha_sample.png  # Generated at runtime (gitignore this)
└── README.md
```

---

## ⚙️ Requirements

```
Python >= 3.10
Pillow >= 9.0
```

Install dependencies:

```bash
pip install Pillow
```

> `turing_test.py` has **no external dependencies** — it runs on the Python standard library alone.

---

## 🚀 Usage

### CAPTCHA

```bash
python captcha.py
```

1. A CAPTCHA image is saved as `captcha_sample.png`.  
2. Open the image and type the text you see.  
3. You have **3 attempts** before access is denied.  
4. A new image is generated after every failed attempt.

**Using the API in your own code:**

```python
from captcha import CaptchaSession, captcha_to_base64

session = CaptchaSession()
img = session.new()            # PIL Image
img.save("challenge.png")

b64 = captcha_to_base64(img)   # useful for HTML <img src="data:...">

if session.verify("AB3C9"):
    print("Human verified ✅")
else:
    print("Wrong answer ❌")
```

---

### Turing Test (interactive)

```bash
python turing_test.py
```

The program will:
1. Introduce you as the **Judge**.
2. Present two anonymous players (A and B).
3. Ask you to type questions — both players respond.
4. After 5 turns, ask you to guess which player is the AI.
5. Reveal the answer and evaluate whether the AI passed.

**Options:**

```bash
# Custom number of turns
python turing_test.py --turns=10

# Run 100 automated trials and print pass-rate statistics
python turing_test.py --evaluate
```

**Using the API in your own code:**

```python
from turing_test import TuringTestSession, AIPlayer

# Stand-alone AI chatbot
bot = AIPlayer(name="Bot")
print(bot.respond("Hello!"))          # → "Hello there!"
print(bot.respond("How are you?"))    # → "I'm doing well, thanks!"

# Full session (both players are AI – useful for testing)
session = TuringTestSession(turns=3, human_plays=False)
session.run()
```

---

## 🏗 Architecture & Design Decisions

### CAPTCHA Design

| Layer | Technique | Reason |
|-------|-----------|--------|
| Text generation | Remove ambiguous chars (O, 0, I, 1) | Reduce false failures |
| Noise | Random dots + coloured lines | Confuse OCR |
| Text rendering | Per-char rotation (±25°) + y-jitter | Break segmentation attacks |
| Post-processing | PIL SMOOTH filter | Natural blur, reduces pixel artifacts |
| Verification | Case-insensitive match | Fair for humans |

### Turing Test Design

| Component | Design choice | Reason |
|-----------|--------------|--------|
| AI engine | Regex rule-base + fallbacks | Simple, offline, educational |
| Role assignment | Random at session start | Prevents Judge from guessing by turn order |
| Evaluation mode | Random-guess oracle | Provides baseline pass-rate metric |
| Extensibility | `AIPlayer.respond()` can be swapped for an LLM API | Future-proof |

---

## 📊 Sample Output

### CAPTCHA
```
==================================================
  CAPTCHA Demo
==================================================
CAPTCHA image saved → captcha_sample.png
(Open the image, then type what you see.)

Attempt 1/3 – Enter CAPTCHA text: XK7P2Q
✅  Correct! Access granted.
```

### Turing Test
```
╔══════════════════════════════════════════════╗
║          TURING TEST SIMULATION              ║
╚══════════════════════════════════════════════╝

──────────────────────────────────────────────────
  Turn 1/5
──────────────────────────────────────────────────
Judge – Ask your question: Do you have feelings?

  [Player A]: I'm not entirely sure, but I try to be empathetic.
  [Player B]: Yes, quite strongly sometimes.

══════════════════════════════════════════════════
  JUDGE'S DECISION
══════════════════════════════════════════════════
Which player is the AI? Enter A or B: A
✅  Correct! The AI was Player A.
   The machine was NOT indistinguishable → Turing Test FAILED for AI.
```

---

## 🔗 References

- Turing, A. M. (1950). *Computing Machinery and Intelligence.* Mind, 59(236), 433–460.  
- Von Ahn, L. et al. (2003). *CAPTCHA: Using Hard AI Problems for Security.* EUROCRYPT 2003.  
- Mori, G. & Malik, J. (2003). *Recognizing Objects in Adversarial Clutter.*

---

## 📝 License

MIT — free to use, modify, and distribute for educational purposes.
