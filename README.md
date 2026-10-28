# Student Splitter — Agile + DevOps Edition

A Streamlit application that reads student registration numbers and names from Excel, groups students by year and department, creates a multi-sheet Excel workbook, and keeps a history of generated outputs.

## Features
- Upload `.xlsx` or `.xls` student lists (required headers: `regno` and `name`; common header variations are accepted).
- Generate year/department-wise worksheets and a summary sheet.
- Download the output and view previous runs.
- Validation for missing required columns, blank registration numbers/names, and duplicate registration numbers.
- Automated unit/integration tests using pytest.
- Docker image and Jenkins CI pipeline for repeatable builds.

## Run locally on Windows
1. Install Python 3.10+ and make sure `python` works in Command Prompt.
2. Extract this ZIP and open Command Prompt in the extracted `Student-Splitter-Agile-DevOps` folder.
3. Create and activate a virtual environment (recommended):

   ```bat
   python -m venv .venv
   .venv\Scripts\activate
   ```
4. Install dependencies:

   ```bat
   python -m pip install -r requirements.txt
   ```
5. Run tests:

   ```bat
   python -m pytest -v
   ```
6. Start the app:

   ```bat
   python -m streamlit run app.py
   ```

The browser should open at `http://localhost:8501`.

## Run with Docker
From this folder:

```bat
docker build -t student-splitter:latest .
docker run --rm -p 8501:8501 student-splitter:latest
```

Open `http://localhost:8501`. Generated history is stored inside the container unless you configure a persistent volume; for a simple course demo, download important outputs before stopping the container.

## Jenkins setup (Windows Jenkins agent)
1. Push the project to a GitHub repository.
2. In Jenkins, create a **Pipeline** job and configure Pipeline from SCM with Git and the repository URL.
3. Ensure the Jenkins agent can run `python` and `docker` in its service account context.
4. Keep `PUSH_TO_DOCKERHUB` unchecked for the first run. The pipeline checks out code, installs requirements, runs pytest, and builds a Docker image.
5. To push to Docker Hub, create a Jenkins username/password credential with ID `dockerhub-creds-v2`, then run with `PUSH_TO_DOCKERHUB` checked. Never put Docker Hub passwords in source code.

## Agile project plan (suggested)
### Product backlog / user stories
- As an event coordinator, I want to upload a student spreadsheet so I can prepare event lists.
- As an event coordinator, I want year/department-wise output so student lists are easier to manage.
- As a user, I want clear validation errors so I can fix bad input files.
- As a user, I want to download generated workbooks and revisit prior runs.
- As a developer, I want automated tests to run for every code change.
- As a developer, I want repeatable container builds through Jenkins.

### Three-sprint plan
- **Sprint 1 — Core features:** Excel upload, event details, grouping, workbook generation, download.
- **Sprint 2 — Quality:** input validation, duplicate checks, history, automated tests, bug fixes.
- **Sprint 3 — Delivery:** GitHub workflow, Jenkins pipeline, Docker build, optional Docker Hub push, demo and review.

### Suggested Trello/Jira columns
Backlog → To Do → In Progress → Testing/Review → Done.

## Git commit examples
- `Initial commit: Student Splitter Streamlit app`
- `Add student input validation and duplicate checks`
- `Add pytest test suite`
- `Add Docker packaging`
- `Add Jenkins CI pipeline and Agile documentation`

## Evaluation demo checklist
1. Show the Agile board and one completed user story.
2. Run the application and upload a sample Excel sheet.
3. Generate and download the workbook; show its Summary and department/year sheets.
4. Demonstrate a duplicate registration number and show the validation message.
5. Run `python -m pytest -v` and show passing tests.
6. Run the Jenkins pipeline and show green test/build stages.
7. Run the Docker image and open the application at `http://localhost:8501`.

> Note: Existing personal/student history workbooks from the original project are intentionally not included in this package. Use anonymized sample data for demos and repository commits.
