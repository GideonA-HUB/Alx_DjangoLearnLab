# Authentication

This API uses token authentication. To access the endpoints, users must provide a valid token in the `Authorization` header.

### Obtain a Token:
- Send a POST request to `/api/auth/token/` with your username and password.

### Permissions:
- All views require authentication (`IsAuthenticated`).
- Only authenticated users can create, update, or delete books. 
- The `BookViewSet` view uses the `IsAuthenticated` permission class, restricting access to authorized users only.
