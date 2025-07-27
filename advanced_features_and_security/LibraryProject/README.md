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

# Disable debug mode in production for security
DEBUG = False

# These settings help prevent XSS, clickjacking, and force HTTPS
SECURE_BROWSER_XSS_FILTER = True  # Adds X-XSS-Protection header
X_FRAME_OPTIONS = 'DENY'  # Prevents site from being embedded in iframes
CSRF_COOKIE_SECURE = True  # Ensures CSRF cookies are sent over HTTPS
SESSION_COOKIE_SECURE = True  # Same for session cookies

# Using Django ORM to safely handle user input in search query
# Prevents SQL injection
