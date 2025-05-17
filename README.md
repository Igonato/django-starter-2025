# Django Starter Template 2025

> [!WARNING]
> *work in progress*

A modern, minimalistic Django starter template focused on developer experience and CI/CD practices.

## Quickstart

### Setup the Project Files

To use the template you can click on the `Use this template` button at the top right and then clone your newly created repo, or do the same using GitHub CLI:

```
gh repo create my-project --template Igonato/django-starter-2025 --private # or --public
gh repo clone my-project

# Alternatively, you can just clone the template:
# git clone https://github.com/Igonato/django-starter-2025.git my-project

cd my-project
```

This template comes with a few examples that are used to test the setup and to showcase the features. Keep them if you're learning but in a real-life project, remove the examples folder and remove 'examples' from the `INSTALLED_APPS` in the `config/settings.py`:

```bash
rm -rf examples
sed -i '/^\s*"examples",$/d' config/settings.py
```

### Option 1: Using Mise

Assuming [mise] is installed.

```bash
# Copy the .env from the provided example:
cp .env.example .env

# Trust the mise.toml config (feel free to inspect it beforehand)
# and install the runtime dependencies (Python, uv, watchexec, ...).
# If your project needs NodeJS or anything else from what is available at
# https://mise.jdx.dev/registry.html, you can add those to mise.toml by
# running `mise use node@22` and the next `mise install` will install
# the appropriate tools for any other person working on your project
mise trust && mise install

# Create virtual environment and install Python dependencies
uv venv && uv sync --locked

# Install pre-commit
pre-commit install

# Create the (SQlite by default) database
mise migrate

# Start the development server
mise dev
```

### Option 2: Using Docker

Assuming [docker] is installed.

TODO

### Option 3: Mise + Docker

Both [mise] and [docker] need to be present.

Run Django development server locally and use Docker compose for Postgres, Redis, etc...

TODO

[mise]: https://github.com/jdx/mise
[docker]: https://www.docker.com/

## Features

### Modern Development Tools
- **mise** - Environment and version management
- **uv** - Fast Python package installer and resolver
- **ruff** - Fast Python linter and formatter
- **pre-commit** - Framework for managing git hooks

### Minimalistic Django Setup
This template intentionally keeps Django dependencies minimal - no CSS frameworks or opinionated libraries (i.e. `crispy-forms`, `allauth`, etc...) are included by default. Just a few changes on top of the vanilla `django-admin startproject`:

- Updated `settings.py` to accept environment variables
- Custom User model (nothing is different but when you need it customized, it should be created [before creating any migrations or running manage.py migrate for the first time](https://docs.djangoproject.com/en/5.2/topics/auth/customizing/#substituting-a-custom-user-model)
- Root `urls.py` config automatically includes urls from `INSTALLED_APPS` when the app is part of the project (see `config/urls.py` for details)
- Channels setup for WebSockets and background tasks (see `examples`)

And some developer tools:

- Django Debug Toolbar for debugging during development
- `django-browser-reload` for automatically reloading browser on file change

<!--
TODO: Kubernetes with minikube. Describe the dns setup:
Try ingress-dns addon and if doesn't work, just add a
loopback to the hosts and use minikube tunnel:
sudo sh -c 'echo \"127.0.0.1       $PROJECT_NAME.internal\" >> /etc/hosts'


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

# Install tools
mise trust
mise install

# Install dependencies
uv sync

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

-->

## License

The template is licensed under either of

- [Apache License, Version 2.0](LICENSE-APACHE)
- [MIT license](LICENSE-MIT)

at your option.
