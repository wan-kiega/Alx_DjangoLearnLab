# Book API Documentation

This document provides an overview of the configuration and operation of the views in the Book API, implemented using Django REST Framework (DRF). The API manages book resources with endpoints for listing, retrieving, creating, updating, and deleting books. Each view is configured with specific permissions and custom logic to handle requests appropriately.

## Project Structure
- **File**: `api/views.py`
  - Defines the view classes for handling HTTP requests.
- **File**: `api/urls.py`
  - Maps URL patterns to the corresponding views.
- **Dependencies**:
  - Django REST Framework (`rest_framework`)
  - Models: `Book` (assumed to be defined in `api/models.py`)
  - Serializers: `BookSerializer` (assumed to be defined in `api/serializers.py`)

## URL Endpoints
The following endpoints are defined in `api/urls.py`:

| Endpoint                | HTTP Method | View                  | Name             | Description                              |
|-------------------------|-------------|-----------------------|------------------|------------------------------------------|
| `books/`                | GET         | `BookListView`        | `book-list`      | List all books                           |
| `books/<int:pk>/`       | GET         | `BookDetailView`      | `book-detail`    | Retrieve a single book by ID             |
| `books/create/`         | POST        | `BookCreateView`      | `book-create`    | Create a new book                        |
| `books/update/`         | PUT         | `BookUpdateView`      | `book-update`    | Update an existing book                  |
| `books/delete/`         | DELETE      | `BookDeleteView`      | `book-delete`    | Delete a book                            |

## Views Configuration and Operation

Below is a detailed explanation of each view, its configuration, intended operation, and any custom settings or hooks.

### 1. `BookListView`
- **Purpose**: Lists all books in the database.
- **Class**: `generics.ListAPIView` (DRF generic view for read-only list operations)
- **Configuration**:
  - **Queryset**: `Book.objects.all()` - Retrieves all `Book` instances from the database.
  - **Serializer**: `BookSerializer` - Serializes `Book` objects into JSON format.
  - **Permission**: `IsAuthenticatedOrReadOnly` - Allows unauthenticated users to perform GET requests (read-only) and authenticated users to perform any safe methods.
- **Operation**:
  - Handles GET requests to `/api/books/`.
  - Returns a JSON array of all books, serialized using `BookSerializer`.
- **Custom Settings/Hooks**: None. Uses default DRF behavior for listing resources.

### 2. `BookDetailView`
- **Purpose**: Retrieves details of a single book by its ID.
- **Class**: `generics.RetrieveAPIView` (DRF generic view for read-only retrieval)
- **Configuration**:
  - **Queryset**: `Book.objects.all()` - Base queryset for retrieving books.
  - **Serializer**: `BookSerializer` - Serializes a single `Book` object into JSON.
  - **Permission**: `IsAuthenticatedOrReadOnly` - Allows unauthenticated users to perform GET requests (read-only).
- **Operation**:
  - Handles GET requests to `/api/books/<int:pk>/`, where `<pk>` is the book's ID.
  - Returns a JSON object representing the book with the specified ID.
- **Custom Settings/Hooks**: None. Uses default DRF behavior for retrieving a single resource.

### 3. `BookCreateView`
- **Purpose**: Creates a new book in the database.
- **Class**: `generics.CreateAPIView` (DRF generic view for creating resources)
- **Configuration**:
  - **Queryset**: `Book.objects.all()` - Used for validation and serialization context.
  - **Serializer**: `BookSerializer` - Validates and serializes incoming data to create a `Book` instance.
  - **Permission**: `IsAuthenticated` - Only authenticated users can create books.
- **Operation**:
  - Handles POST requests to `/api/books/create/`.
  - Expects a JSON payload with book details (e.g., `{"title": "Book Title", "author": "Author Name"}`).
  - Creates and saves a new `Book` instance if the data is valid.
- **Custom Settings/Hooks**:
  - **Hook**: `perform_create(self, serializer)` - Overrides the default save behavior. Currently, it simply calls `serializer.save()` but can be extended to add custom logic (e.g., setting a `created_by` field to the authenticated user).

### 4. `BookUpdateView`
- **Purpose**: Updates an existing book identified by an ID provided in the request body.
- **Class**: `generics.UpdateAPIView` (DRF generic view for updating resources)
- **Configuration**:
  - **Queryset**: `Book.objects.all()` - Base queryset for retrieving the book to update.
  - **Serializer**: `BookSerializer` - Validates and serializes the updated book data.
  - **Permission**: `IsAuthenticated` - Only authenticated users can update books.
- **Operation**:
  - Handles PUT requests to `/api/books/update/`.
  - Expects a JSON payload with the book ID and updated fields (e.g., `{"id": 1, "title": "Updated Title"}`).
  - Updates the specified book if it exists and the data is valid.
- **Custom Settings/Hooks**:
  - **Hook**: `get_object(self)` - Overrides the default method to retrieve the book based on the `id` field in the request body (`self.request.data.get('id')`) instead of a URL parameter. Raises:
    - `ValidationError` if `id` is not provided.
    - `NotFound` if the book with the specified ID does not exist.
  - **Hook**: `perform_update(self, serializer)` - Adds custom validation to ensure the `title` field is not empty. Raises `ValidationError` if the title is blank.

### 5. `BookDeleteView`
- **Purpose**: Deletes a book identified by an ID provided in the request body.
- **Class**: `generics.DestroyAPIView` (DRF generic view for deleting resources)
- **Configuration**:
  - **Queryset**: `Book.objects.all()` - Base queryset for retrieving the book to delete.
  - **Serializer**: `BookSerializer` - Used for validation and serialization context.
  - **Permission**: `IsAuthenticated` - Only authenticated users can delete books.
- **Operation**:
  - Handles DELETE requests to `/api/books/delete/`.
  - Expects a JSON payload with the book ID (e.g., `{"id": 1}`).
  - Deletes the specified book if it exists.
- **Custom Settings/Hooks**:
  - **Hook**: `get_object(self)` - Overrides the default method to retrieve the book based on the `id` field in the request body (`self.request.data.get('id')`) instead of a URL parameter. Raises:
    - `ValidationError` if `id` is not provided.
    - `NotFound` if the book with the specified ID does not exist.

## Custom Settings and Hooks Summary
- **Custom URL Design**:
  - The update (`/api/books/update/`) and delete (`/api/books/delete/`) endpoints use the request body to specify the book ID instead of including it in the URL (e.g., `/books/<pk>/update/`).
  - This is implemented via the `get_object` method in `BookUpdateView` and `BookDeleteView`.
- **Custom Validation**:
  - `BookUpdateView` includes a check in `perform_update` to prevent updating a book with an empty title.
- **Permissions**:
  - Read-only endpoints (`BookListView`, `BookDetailView`) use `IsAuthenticatedOrReadOnly` to allow unauthenticated GET requests.
  - Write endpoints (`BookCreateView`, `BookUpdateView`, `BookDeleteView`) use `IsAuthenticated` to restrict access to authenticated users.

## Example Requests
Below are example HTTP requests for each endpoint:

### List Books
```bash
curl -X GET http://your-api/api/books/