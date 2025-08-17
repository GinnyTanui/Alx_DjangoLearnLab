# Book API - Generic Views

This API handles CRUD operations for the Book model using Django REST Framework's generic views.

## Endpoints

| Method | Endpoint            | Description           | Auth Required |
|--------|---------------------|-----------------------|---------------|
| GET    | /books/             | List all books        | No            |
| GET    | /books/<id>/        | Get book by ID        | No            |
| POST   | /books/create/      | Create new book       | Yes           |
| PUT    | /books/update/<id>/ | Update book           | Yes           |
| DELETE | /books/delete/<id>/ | Delete book           | Yes           |

## Permissions
- **Public access** for `ListView` and `DetailView`
- **Authenticated users only** for `CreateView`, `UpdateView`, and `DeleteView`
- Optional: `IsAdminOrReadOnly` for stricter control

## Testing
Use Postman or curl:
```bash
curl -X GET http://localhost:8000/books/
