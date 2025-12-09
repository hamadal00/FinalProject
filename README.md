# Setup and Usage Instructions

## Backend Setup (FastAPI)

1. **Navigate to the backend folder**

```bash
cd backend
```

2. **Create a virtual environment**

```bash
python3 -m venv venv
```

3. **Activate the virtual environment**

- **Windows:**

```bash
venv\Scripts\activate
```

- **macOS / Linux:**

```bash
source venv/bin/activate
```

4. **Install dependencies**

```bash
pip install -r requirements.txt
```

5. **Run the FastAPI server**

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

6. The backend will now run on:

```
http://0.0.0.0:8000
```

Interactive API documentation is available at:

```
http://127.0.0.1:8000/docs
```

---

## Frontend Setup (Streamlit)

The frontend does **not** require a virtual environment.

1. **Navigate to the frontend folder**

```bash
cd frontend
```

2. **Install required packages**

```bash
pip install streamlit pandas requests
```

3. **Run the frontend application**

```bash
streamlit run app.py
```

4. The browser will automatically open the Streamlit interface.

Select one of the following options:
- **PARK**
- **CENTERS**
- **ACTIVITIES**

Then click the **Fetch Data** button to retrieve data from the backend.
