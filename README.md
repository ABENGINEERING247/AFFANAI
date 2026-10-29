# AFFAN AI — Kids' Bilingual Companion 🇵🇰

AFFAN AI is a child-focused Streamlit prototype for discovering cartoons, Urdu stories, educational videos, books, science activities, art ideas and learning resources in **English, Urdu and Roman Urdu**.

## Features

- Friendly AFFAN AI landing page
- English / Urdu / Roman Urdu interface text
- Task-based resource suggestions
- Curated starting links for Urdu cartoons, books, science, reading and early learning
- Basic keyword screening for adult/graphic requests and some personal-information patterns
- Parent safety guidance and Pakistan child-safety resources
- No API key required for the included prototype

## Project files

- `app.py` — Streamlit application
- `requirements.txt` — Python dependencies

## Run locally

Python 3.10+ recommended.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

Open the local URL Streamlit prints in your terminal.

## Deploy to Streamlit Community Cloud

1. Upload `app.py` and `requirements.txt` to a GitHub repository.
2. In Streamlit Community Cloud, create an app from that repository.
3. Select `app.py` as the main file.
4. Deploy.

## Important safety limitations

This is a **prototype, not a certified child-safety system**.

- Keyword screening is basic and can miss unsafe requests or incorrectly flag harmless ones.
- A link to a video platform does not guarantee every video or recommendation is suitable.
- The optional parent PIN field is only a UI placeholder and does not authenticate a parent.
- External links may change. A parent or caregiver should review individual videos, movies and books.
- The prototype does not store chat history in a database and does not call an LLM by default.
- Do not collect children's personal details. For production, use privacy-by-design, a reviewed allowlist, robust moderation, age-appropriate design, secure parental authentication, and a documented data-retention policy.

## Suggested production upgrades

1. Integrate an LLM behind server-side secrets with strict child-safe instructions and moderation.
2. Use a reviewed catalogue/allowlist instead of unrestricted search results.
3. Add parent authentication, age settings, daily screen-time reminders and reporting.
4. Add audio input/output only with consent and clear privacy disclosures.
5. Test Urdu, Roman Urdu, English, code-switching, spelling variations and adversarial prompts.
6. Review legal and platform requirements before collecting or processing children's data.

## Pakistan-focused resources

- KidsLand Pakistan: https://kidsland.com.pk/
- Pakistan National CERT — Cyber Care for Children: https://pkcert.gov.pk/ccc-program.asp
- NCCIA Cyber Safety: https://www.nccia.gov.pk/cyber-safety.php
- National Commission on the Rights of Child parent guide: https://ncrc.gov.pk/wp-content/uploads/2025/03/A-Guide-to-Parental-Control-by-PTA-A5.pdf

---
**AFFAN AI — Learn, Explore, and Grow Safely.**
