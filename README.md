# Problem 1 - Turing Test and CAPTCHA

Two programs that explore how we tell humans apart from machines.

## Files

- `captcha.py` - generates a CAPTCHA image for the user to solve
- `turing_test.py` - simulates the Turing Test in the terminal

---

## CAPTCHA

Install dependency:
```
pip install Pillow
```

Run:
```
python captcha.py
```

A distorted text image is saved as `captcha_sample.png`. Open it, type what you see. You get 3 tries.

---

## Turing Test

No install needed. Run:
```
python turing_test.py
```

You are the judge. Two players answer your questions - one is a human, one is a bot. After a few rounds you guess which is which.

To change number of rounds:
```
python turing_test.py --turns=10
```
