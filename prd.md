# PRD - Vibe Coding Base App (Module 2)

## Problem Statement
The rapid rise of AI-assisted development ("Vibe Coding") allows for unprecedented speed in application prototyping. However, this speed often comes at the cost of security rigor and architectural structure. This application serves as a baseline to demonstrate these tradeoffs in a controlled lab environment.

## Personas
- **Lab Student**: Learning to identify and mitigate security risks in AI-generated code.
- **Security Engineer**: Reviewing vibe-coded applications for common vulnerabilities.
- **Platform Engineer**: Deploying containerized workloads to vK8s environments.

## Non-Goals (Module 2)
- **No Authentication**: No login, sessions, or user registration.
- **No API**: No programmatic endpoints (reserved for Module 3).
- **No Forms**: No data submission or user-generated content storage.
- **No Database**: Static or in-memory data only.

## User Stories
- As a user, I want to learn about the definition and history of Vibe Coding.
- As a user, I want to understand the benefits and risks associated with AI-assisted development.
- As a user, I want to see clear citations for the information provided.

## MVP Scope
- Read-only web interface with Home, About, and Docs pages.
- Health check endpoint (`/healthz`).
- Containerized deployment configuration.
- Basic unit tests for route availability.

## Success Metrics
- Application deploys successfully to vK8s on port 5000.
- Application passes basic security scans (highlighting intentional gaps).
- All informational content is accurately cited.

## Constraints
- Must use Flask (Python).
- Must be "lab-safe" (vulnerabilities must not be destructive).
- Must bind to 0.0.0.0:5000.
