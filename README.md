# Boston House Pricing

Simple Flask app and model for predicting Boston house prices.

## Contents

- `app.py` — Flask application that serves a web UI and a `/predict_api` endpoint.
- `reg_model.pkl` — pickled scikit-learn regression model (trained offline).
- `scaling.pkl` — pickled scikit-learn scaler used to transform inputs.
- `templates/home.html` — web UI (form) for entering features and getting a prediction.
- `static/` — CSS and JS used by the UI.
- `Boston.csv`, `bos_1.ipynb` — dataset and notebook used for model development.

## Features / Notes

- The deployed model expects 12 features in the following order: `CRIM, ZN, INDUS, CHAS, NOX, RM, AGE, DIS, RAD, TAX, PTRATIO, LSTAT`.
- The UI collects these features, posts JSON to `/predict_api`, and displays the numeric prediction.
- The app will return structured JSON errors (400/500) on invalid input or server errors.

## Local setup

1. Create a virtual environment (recommended) and install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
# or `source .venv/bin/activate` on macOS/Linux
pip install -r requirements.txt
```

2. Run the app:

```bash
python app.py
```

3. Open the UI in your browser:

http://127.0.0.1:5000/

Or call the API directly (JSON payload):

```json
{ "data": [CRIM, ZN, INDUS, CHAS, NOX, RM, AGE, DIS, RAD, TAX, PTRATIO, LSTAT] }
```

## Git / Deployment

- To commit and push changes to `main`:

```bash
git add README.md requirements.txt
git commit -m "Add project README and requirements"
git push -u origin main
```

If you get `error: src refspec ... does not match any`, ensure your local branch exists and is named `main` (check with `git branch --show-current`). If your branch is `master`, either rename it or push `master:main`.

## Dependencies

- Flask
- scikit-learn
- pandas
- numpy

See `requirements.txt` for exact versions.

## License

See LICENSE file in the repo.

---
If you'd like, I can also add a minimal `requirements.txt` and push these changes to GitHub now.