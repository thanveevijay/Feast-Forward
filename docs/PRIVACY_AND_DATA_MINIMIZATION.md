# Privacy and data minimization

Food donation coordination may involve donor, volunteer, and recipient contact details. Collect only what is necessary for a specific handoff.

## Data collection
- Explain why each personal field is needed before collecting it.
- Avoid exposing phone numbers, email addresses, or precise recipient details in public food listings.
- Use role-based access to limit who can view contact details.
- Do not collect sensitive personal details unless there is a clear, reviewed requirement.

## Retention and deletion
- Define how long inactive accounts and completed donation records are retained.
- Provide a process for correcting inaccurate information and handling deletion requests.
- Remove personal data from test fixtures, screenshots, and demonstration databases.
- Keep backups access-controlled and apply a retention schedule.

## Engineering safeguards
- Avoid logging request bodies that contain contact details.
- Use HTTPS in deployed environments.
- Restrict CORS to known frontend origins.
- Do not commit database files or populated environment files.
