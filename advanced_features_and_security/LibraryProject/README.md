## Permissions Setup

### Roles and Groups:
- **Viewers**: Can only view books.
- **Editors**: Can view, create, and edit books.
- **Admins**: Can view, create, edit, and delete books.

### Custom Permissions (defined in Book model):
- `can_view`: Can view books.
- `can_create`: Can add new books.
- `can_edit`: Can modify books.
- `can_delete`: Can remove books.

### Setup Notes:
- Groups and permissions are created manually or via Django shell.
- Users should be added to groups using the Django Admin.
- Views are protected using `@permission_required`.
