# StarLink Personalized Customer Homepage

A Streamlit prototype for a telecom self-service homepage. Customers can sign in, view their plan and data usage, see remaining data, and receive personalized data-plan recommendations directly on the homepage.

## Features

- Customer sign-in using a profile and four-digit PIN.
- Customer-specific allocated, used, and remaining data.
- Current StarLink plan and billing summary.
- Inline recommendations based on remaining data.
- Add-on selection when the customer reaches their data limit.
- Persistent plan updates stored in `customer_usage.csv`.
- Sign-out flow so another customer can use the app safely.
- Product requirements document in `PRD_StarLink_Personalized_Homepage.md`.

## Demo customers

All demo customers use PIN `1234`.

| Customer | Allocated | Used | Remaining |
|---|---:|---:|---:|
| Neha | 10 GB | 10 GB | 0 GB |
| Rahul | 20 GB | 8 GB | 12 GB |
| Vivaan | 5 GB | 4.5 GB | 0.5 GB |

Neha starts at the data limit and receives a recommendation for a larger plan. Selecting the add-on updates her allocated data in the CSV. On the next sign-in, the updated allocation is displayed.

## Project files

```text
streamlit_app.py                       Streamlit application
customer_usage.csv                     Customer data and demo PINs
requirements.txt                       Python dependency list
PRD_StarLink_Personalized_Homepage.md  Product requirements document
```

The `client/` and `server/` folders contain the earlier React/Node prototype and are not required to run the current Streamlit application.

## Run locally

Install Python 3.10 or newer, then open a terminal in the project folder:

```bash
py -m pip install -r requirements.txt
py -m streamlit run streamlit_app.py
```

If `py` is unavailable, use:

```bash
python -m pip install -r requirements.txt
python -m streamlit run streamlit_app.py
```

Streamlit will open the app in your browser, usually at `http://localhost:8501`.

## GitHub

The project repository is available at:

https://github.com/nehabagwariupraity-ux/starlink-customer-homepage1

## Important note

The PINs and CSV storage are for demonstration only. A production application should use secure authentication, hashed credentials, authorization controls, and a database instead of storing customer PINs in a plain CSV file.
