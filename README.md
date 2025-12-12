
# Arquitectura completa de la API – Blog & Projects (FastAPI + Postgres)

Este documento describe **toda la arquitectura de la API** para un blog personal con:
- Parte pública (blog, notes, projects)
- Dashboard admin (`/admin`) para gestionar contenido
- Projects como **sub‑blog versionado**, con posts ligados a commits del repositorio

Stack asumido:
- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy 2.0**
- **Alembic**
- **Pydantic v2**
- **JWT (admin)**

---

## 1. Estructura del proyecto

```text
backend/
├─ app/
│  ├─ main.py
│  ├─ core/
│  │  ├─ config.py
│  │  ├─ database.py
│  │  ├─ security.py
│  │  └─ deps.py
│  │
│  ├─ api/
│  │  ├─ v1/
│  │  │  ├─ router.py
│  │  │  ├─ health.py
│  │  │  ├─ notes.py
│  │  │  ├─ projects.py
│  │  │  ├─ project_posts.py
│  │  │  ├─ tags.py
│  │  │  └─ search.py
│  │  │
│  │  └─ admin/
│  │     ├─ router.py
│  │     ├─ auth.py
│  │     ├─ notes.py
│  │     ├─ projects.py
│  │     ├─ project_posts.py
│  │     └─ assets.py
│  │
│  ├─ models/
│  │  ├─ base.py
│  │  ├─ user.py
│  │  ├─ tag.py
│  │  ├─ note.py
│  │  ├─ project.py
│  │  └─ project_post.py
│  │
│  ├─ schemas/
│  │  ├─ common.py
│  │  ├─ auth.py
│  │  ├─ tag.py
│  │  ├─ note.py
│  │  ├─ project.py
│  │  └─ project_post.py
│  │
│  ├─ services/
│  │  ├─ notes.py
│  │  ├─ projects.py
│  │  ├─ project_posts.py
│  │  ├─ tags.py
│  │  └─ auth.py
│  │
│  ├─ utils/
│  │  ├─ slugs.py
│  │  ├─ pagination.py
│  │  └─ markdown.py
│  │
│  └─ db/
│     └─ migrations/
│
├─ alembic.ini
├─ pyproject.toml
└─ README.md
```

### Responsabilidad por capa
- **models/** → Tablas y relaciones (SQLAlchemy)
- **schemas/** → Contratos de entrada/salida (Pydantic)
- **services/** → Lógica de negocio
- **api/** → Endpoints HTTP
- **core/** → Configuración, DB, auth
- **utils/** → Helpers reutilizables

---

## 2. Rutas del API

### Público `/api/v1`
```http
GET /health

GET /notes
GET /notes/{slug}

GET /projects
GET /projects/{project_slug}

GET /projects/{project_slug}/posts
GET /projects/{project_slug}/posts/{post_slug}

GET /tags
GET /search?q=
```

### Admin `/api/admin`
```http
POST /auth/login
POST /auth/refresh

POST   /notes
PATCH  /notes/{id}
DELETE /notes/{id}
POST   /notes/{id}/publish
POST   /notes/{id}/unpublish

POST   /projects
PATCH  /projects/{id}
DELETE /projects/{id}

POST   /projects/{project_id}/posts
PATCH  /projects/{project_id}/posts/{post_id}
DELETE /projects/{project_id}/posts/{post_id}
POST   /projects/{project_id}/posts/{post_id}/publish
POST   /projects/{project_id}/posts/{post_id}/unpublish
```

---

## 3. Modelos de base de datos

### User (admin)
- id (uuid)
- email (unique)
- password_hash
- role
- is_active

### Tag
- id
- name (unique)
- slug (unique)

### Note
- id
- slug (unique)
- title
- summary
- content_md
- category
- status (draft | published)
- published_at
- timestamps

### Project
- id
- slug (unique)
- title
- summary
- repo_url
- demo_url
- status (active | archived)
- timestamps

### ProjectPost (sub‑blog versionado)
- id
- project_id (fk)
- slug (unique por project)
- title
- summary
- content_md
- version
- commit_sha
- status (draft | published)
- published_at
- timestamps

**Constraints clave**
- UNIQUE(project_id, slug)
- index(project_id, published_at desc)
- commit_sha validado (7–40 hex)

---

## 4. Schemas (Pydantic)

### Note
- NoteCreate
- NoteUpdate
- NoteOut (público)
- NoteAdminOut

### Project
- ProjectCreate
- ProjectUpdate
- ProjectOut
- ProjectAdminOut

### ProjectPost
- ProjectPostCreate
- ProjectPostUpdate
- ProjectPostOut
- ProjectPostAdminOut

Validaciones:
- slug: kebab‑case
- commit_sha: hex válido
- version: string libre (semver o fecha)

---

## 5. Services (lógica)

Ejemplos:
- list_notes(only_published=True)
- publish_note(id)
- list_project_posts(project_slug)
- publish_project_post(project_id, post_id)

Reglas:
- Público solo ve `published`
- Admin puede ver `draft`
- publish → setea `published_at`
- commit_url se construye desde `repo_url + commit_sha`

---

## 6. Auth (Admin)

- JWT access + refresh
- Hashing: argon2
- Dependencias:
  - get_current_user
  - require_admin

---

## 7. Paginación

Cursor‑based:
- limit
- cursor
- respuesta:
  - items
  - next_cursor

---

## 8. Convención de contenido

Los ProjectPost usan **Markdown libre**, con secciones recomendadas:

```md
## Qué se lanzó
## Por qué
## Cómo
## Trade‑offs
## Referencias
```

El dashboard puede ofrecer formularios guiados y generar el markdown.

---

## 9. Flujo típico

1. Crear Project
2. Crear ProjectPost (draft)
3. Asociar versión + commit
4. Publicar
5. El frontend lo muestra como timeline del proyecto

---

## 10. Resultado final

- Blog público SEO‑friendly
- Projects como sub‑blogs versionados
- Admin desacoplado
- API lista para escalar

---

Este archivo sirve como **documentación base del backend** y referencia para desarrollo.
