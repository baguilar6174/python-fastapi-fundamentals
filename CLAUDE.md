# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a FastAPI learning project that implements a REST API for managing customers, transactions, and invoices using SQLite database with SQLModel ORM.

## Common Commands

```bash
# Run the development server
fastapi dev app/main.py

# Install dependencies
pip install -r requirements.txt

# Check library versions
pip freeze | grep <library-name>
```

## Architecture

### Core Structure
- **app/main.py**: Main FastAPI application entry point with lifespan management for database table creation
- **models.py**: SQLModel data models defining Customer, Transaction, and Invoice entities with relationships
- **db.py**: Database configuration with SQLite engine, session management, and dependency injection
- **app/routers/**: API route modules organized by domain (customers, transactions, invoices)

### Database Design
- Uses SQLModel (Pydantic + SQLAlchemy) for type-safe database operations
- SQLite database (`db.sqlite3`) with automatic table creation on startup
- Customer-Transaction one-to-many relationship via foreign key
- Session dependency injection pattern (`SessionDependency`) for database operations

### Key Patterns
- Router-based organization with APIRouter instances included in main app
- Separate Create/Update/Base model classes for request validation
- Database session management through dependency injection
- Standard CRUD operations with proper HTTP status codes and error handling

### Dependencies
- FastAPI with standard extras for web framework
- SQLModel for database ORM and validation
- Pydantic for data validation and serialization