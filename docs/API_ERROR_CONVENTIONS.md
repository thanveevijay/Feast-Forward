# API error response conventions

Use a consistent, non-sensitive error shape across FeastForward endpoints as the API evolves.

## Recommended response shape
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Please check the submitted fields."
  }
}
```

## Status code guidance
- 400: malformed request or invalid field values.
- 401: missing or invalid authentication, once authentication is implemented.
- 403: authenticated caller lacks permission.
- 404: requested resource does not exist or is not visible to the caller.
- 409: conflicting state, such as an invalid status transition.
- 413: uploaded content exceeds the configured limit.
- 415: unsupported media type.
- 500: unexpected server failure.

## Safety and consistency
- Keep internal exception details and filesystem paths out of client responses.
- Validate request bodies before database writes.
- Use the same field naming and error structure across endpoints.
- Do not reveal whether a private account exists when that would expose user information.
- Add endpoint tests for both successful and failing requests.
