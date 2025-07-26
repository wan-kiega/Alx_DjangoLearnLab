Define Complex Models in relationship_app/models.py:

Author Model:
name: CharField.

Book Model:
title: CharField.
author: ForeignKey to Author.

Library Model:
name: CharField.
books: ManyToManyField to Book.

Librarian Model:
name: CharField.
library: OneToOneField to Library.

Apply Database Migrations:

Run migrations to create your model tables: 
python manage.py makemigrations relationship_app 
python manage.py migrate.

Implement Sample Queries:

Prepare a Python script query_samples.py in the relationship_app directory. This script should contain the query for each of the following of relationship:
Query all books by a specific author.
List all books in a library.
Retrieve the librarian for a library.