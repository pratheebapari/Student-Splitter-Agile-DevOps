# Agile plan — Student Splitter

## Product goal
Deliver a reliable application that helps event coordinators prepare year/department-wise student lists from Excel files, with a repeatable test-and-deploy process.

## Roles (adapt to team size)
- Product Owner: prioritizes user stories and accepts completed work.
- Scrum Master / coordinator: maintains the board and facilitates sprint review/retrospective.
- Developer(s): implement features, tests, and pipeline.

## Backlog with acceptance criteria
1. **Upload student list** — accepts Excel input with registration number and name columns; shows an understandable error if required columns are missing.
2. **Generate grouped workbook** — output contains a summary sheet and year/department sheets; row totals match input rows.
3. **Validate data quality** — rejects blank registration numbers, blank names, and duplicate registration numbers with a helpful message.
4. **View history** — user can see prior runs and download or delete generated files.
5. **Automated tests** — tests cover parsing, grouping, workbook generation, and invalid input.
6. **CI image build** — Jenkins runs tests before building a Docker image; failed tests stop the pipeline.

## Sprint schedule
- Sprint 1: stories 1–2; demo working upload and workbook generation.
- Sprint 2: stories 3–4; demo invalid-data handling and history.
- Sprint 3: stories 5–6; demo test results, Jenkins, Docker, and collect feedback.

## Definition of Done
- Acceptance criteria met.
- Code committed to GitHub with a descriptive commit message.
- Relevant tests pass.
- No secrets or real student data committed.
- Feature demonstrated during sprint review and board updated.
