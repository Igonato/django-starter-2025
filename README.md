# Django Starter Template 2025

⚠ *work in progress* ⚠

A modern, minimalistic Django starter template focused on developer experience and CI/CD practices.

## Features

### Modern Development Tools
- **mise** - Environment and version management
- **uv** - Fast Python package installer and resolver
- **ruff** - Fast Python linter and formatter
- **pre-commit** - Framework for managing git hooks

### Minimalistic Django Setup
This template intentionally keeps Django dependencies minimal - no opinionated libraries (i.e. `crispy-forms`, `allauth`, etc...), or CSS frameworks are included by default. Just a few changes on top of the vanilla `django-admin startproject`:

 - Updated `settings.py` to accept environment variables
 - Custom User model (nothing is different but when you need it customized, it should be created [before creating any migrations or running manage.py migrate for the first time](https://docs.djangoproject.com/en/5.2/topics/auth/customizing/#substituting-a-custom-user-model)
 - Root `urls.py` config automatically includes urls from `INSTALLED_APPS` when the app is part of the project (see `config/urls.py` for details)
 - Django Debug Toolbar for debugging during development

### Developer Experience
- Local development with just `mise sync && mise migrate && mise dev` using local sqlite file (no Docker or DB setup is needed, until your app needs it and when it does there is a `docker-compose.yaml` waiting for you)
- Environment-based configuration via `.env` file
- Convenient development commands via mise tasks
- Code formatting and linting enforced via pre-commit hooks and GitHub Actions
- GitHub Actions for continuous integration
- (TODO) Supports pytest tests with examples (including testing async views)
- (TODO) End-to-end tests with Playwright

### Production Readiness
- Environment-based settings configuration
- (TODO) Rich deployment config and CI/CD
- (TODO) Ansible playbook for a single-instance non-containerized VPS setup
- (TODO) Yaml configs and a guide on deploying the app to a Kubernetes cluster
- (TODO) Backups, monitoring and alerts

## Getting Started

### Prerequisites
- Git
- [mise](https://github.com/jdx/mise)

### Installation

```bash
# Clone the repository
git clone https://github.com/Igonato/django-starter-2025.git
cd django-starter-2025

# Install dependencies
mise sync

# Depending on your mise config you may need to manually run
# source .venv/bin/activate  # Unix/Mac
# .venv\Scripts\activate     # Windows

# Install the pre-commit hook
pre-commit install

# Set up the devlopment environment variables
cp .env.example .env  # and edit as needed

# Run migrations
mise migrate
# (or `mise run migrate` - the `run` is optional when there are no name
# collisions with the built-in mise commands)

# Start the development server
mise dev
```

## Available Commands

- `mise sync` - Install the Python dependencies
- `mise dev` - Run the development server
- `mise test` - Run tests
- `mise format` - Format code with Ruff
- `mise check` - Lint code with Ruff
- `mise migrate` - Apply database migrations
- `mise makemigrations` - Create new migrations

## Local SSL

It's important to test your app in an environment as close to your production setup as possible, that includes TLS. Certain browser features can behave differently over https.

If you already use `mkcert` (can be installed with `mise use -g mkcert && mkcert -install`) and have its CA installed, you can use your local `mkcert`
to generate certificates by running:

```bash
mkcert \
    -cert-file devops/certs/selfsigned.crt \
    -key-file devops/certs/selfsigned.key \
    localhost 127.0.0.1
```

Otherwise the certificates will be generated for you on the first `docker compose up` and placed in `devops/certs` folder.

If you want to suppress the browser's security warning, add `rootCA.pem` (from `devops/certs` or `mkcert -CAROOT`) to trusted Authorities:

1. Open your browser settings and search for "certificates"
2. Click "Manage certificates" and go to "Authorities" tab
3. Click "Import" and select the rootCA.pem file from the certs directory
4. Check "Trust this certificate for identifying websites"
5. Click OK and restart your browser


## TODO

- [x] Add basic Docker and docker-compose configurations
- [ ] Add a dedicated container for development?
- [x] SSL support for local development?
- [ ] Set up Ansible playbooks for a VPS deployment with a GitHub Action
- [ ] Add example of DRF API setup
- [ ] Add example of Celery worker configuration
- [ ] Add example of Channels setup
- [ ] Implement a deployment guide for VPS
- [ ] Implement a deployment guide for Kubernetes
- [ ] Implement a guide for adding an SPA to the mix
- [ ] Describe files and folder structure
- [ ] Double check Django settings

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

The template is licensed under either of

- [Apache License, Version 2.0](LICENSE-APACHE)
- [MIT license](LICENSE-MIT)

at your option.
