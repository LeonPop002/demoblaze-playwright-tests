# Demoblaze – Playwright Test Automation

End-to-end UI test automation for [Demoblaze](https://www.demoblaze.com), a demo e-commerce site, built with **Python**, **Playwright** and **Pytest** using the **Page Object Model** design pattern.

Alongside the automated UI tests, the site's backend API was explored manually with **Postman**. Several bugs found that way are documented below, including the root cause of one of the UI bugs.

---

## Project Structure

- `Pages/` – Page Objects, one class per page (home, signup, login, product feed, product, cart, purchase)
- `Tests/` – test files, from registration through a full E2E purchase flow
- `conftest.py` – shared fixtures, including `cart_with_product`, which prepares a cart with a product and returns its feed price for later checks

---

## Getting Started

**Prerequisites:** Python 3 and Git.

```bash
git clone https://github.com/LeonPop002/demoblaze-playwright-tests.git
cd demoblaze-playwright-tests

python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux

pip install -r requirements.txt
playwright install
```

### Running the tests

```bash
pytest -v                              # all tests, headless
pytest Tests/test_smoke.py -v --headed # smoke test with a visible browser
pytest Tests/test_E2E.py -v --headed   # full end-to-end flow
```

---

## Test Approach

- **E2E price validation:** the product price is checked at every step: in the feed, on the product page, in the cart row, in the cart total, and in the final order amount.
- **Negative testing:** the tests cover invalid logins, missing order-form fields, invalid card data and expired dates.
- **Known bugs are marked `xfail`:** a test that fails because of a confirmed site bug is marked as an expected failure. The suite stays green, and each known bug is still documented in the code.

---

## Bugs Found

### UI

| ID | Description |
|----|-------------|
| BUG-123 | Sign-up accepts a 1-character password |
| BUG-124 | The order completes with **Amount: 0 USD** if Place Order is clicked before the cart total loads (timing-dependent) |
| BUG-125 | The purchase completes without a country or city |
| BUG-126 | The purchase completes with an expired year (1990) |
| BUG-127 | The purchase completes with an invalid card number (`ABC456`) |
| — | Inconsistent alert text: "Product added." when logged in vs. "Product added" as a guest |

### API (explored with Postman)

| Endpoint | Finding |
|----------|---------|
| `POST /login` | A wrong password returns **200 OK** with an error message in the body instead of **401** |
| `POST /login` | **Security:** the password is only Base64-encoded, which is encoding, not encryption. The auth token is just Base64 of the username plus an expiration number, so it is predictable and could be forged. |
| `POST /signup` | An existing user returns 200 with "This user already exist." The server also accepts a 1-character, non-Base64 password. |
| `POST /addtocart` | A non-existent `prod_id` (e.g. 999) is accepted with 200, which creates a "ghost" cart item with no name or price |
| `POST /addtocart` | An empty `cookie` value returns **500** (server error); a missing `cookie` field returns 400 |
| `POST /addtocart` | **Root cause of BUG-124:** the request carries no price, so the cart total is computed client-side. Clicking Place Order before that calculation finishes sends an order for 0 USD. |
| `GET /entries` | Data issue: "Samsung galaxy s7" (id 4) uses the image `galaxy_s6.jpg` |
| `GET /entries` | Data issue: the title of "Sony vaio i7" (id 9) has a trailing `\n`. It is invisible in the UI but present in the data (low severity). |

---

## Author

**Leon Popytaev**: QA Automation student at HackerU
GitHub: [@LeonPop002](https://github.com/LeonPop002)
