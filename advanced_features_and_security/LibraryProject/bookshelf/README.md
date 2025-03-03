### Permissions and Groups Setup

1. **Permissions**:
   - `can_view`: Allows viewing posts.
   - `can_create`: Allows creating posts.
   - `can_edit`: Allows editing posts.
   - `can_delete`: Allows deleting posts.

2. **Groups**:
   - **Viewers**: Assigned the `can_view` permission.
   - **Editors**: Assigned the `can_create`, `can_edit`, and `can_view` permissions.
   - **Admins**: Assigned all permissions (`can_view`, `can_create`, `can_edit`, `can_delete`).

3. **Usage**:
   - Use the `@permission_required` decorator to enforce these permissions in views.
   - Example: `@permission_required('blog.can_create', raise_exception=True)` on the `create_post` view.
