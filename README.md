# abstract_security

**Env-driven secrets loading and security primitives: `.env` resolution,
password hashing, token utilities, and a library of type/path/ssh helpers.**

`abstract_security` is the foundation layer of the **Abstract Secure Backend**
stack. Everything else builds on it for locating `.env` files, reading secrets,
hashing passwords, and issuing/validating tokens.

---

## Where this fits

```
abstract-securefiles   React/TypeScript UI components
abstract_logins        Flask blueprints: auth + secure files
abstract_queries       Domain query managers (users, uploads, ...)
abstract_database      Lazy PostgreSQL connection + helpers
abstract_security  <-- you are here: env loading, hashing, tokens, utilities
```

Dependencies flow downward; this layer depends only on `abstract_utilities` and
`python-dotenv`.

---

## Install

```bash
pip install abstract_security
```

Requires Python ≥ 3.6.

---

## Usage

```python
from abstract_security import get_env_value, get_env_path

# Resolve a value from a .env file, searching sensible default locations
# (cwd, home, and ~/.envy_all) unless an explicit path is given.
db_url = get_env_value("ABSTRACT_DATABASE_URL")
env_file = get_env_path()            # where the .env was found
```

It also exposes password/token helpers (bcrypt hashing, JWT) and a broad set of
utility modules (`type_utils`, `path_utils`, `ssh_utils`, `string_utils`,
`compare_utils`, …) shared across the stack.

---

## Design notes

- **Flexible `.env` discovery** — looks in the current working directory, the
  home directory, and a dedicated `~/.envy_all` directory, or an explicit path.
- **One definition per symbol** — shared primitives like `SingletonMeta` are
  defined once, so behaviour is predictable across the stack.

---

## License

MIT.
