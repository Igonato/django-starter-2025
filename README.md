# Django Starter Template 2025

A modern, minimalistic Django starter template focused on developer experience and CI/CD practices.

## Features

### Modern Development Tools
- **mise** - Environment and version management
- **uv** - Fast Python package installer and resolver
- **ruff** - Fast Python linter and formatter
- **pre-commit** - Framework for managing git hooks

### Minimalistic Django Setup
This template intentionally keeps Django dependencies minimal - no opinionated libraries (i.e. `crispy-forms`, `allauth`), or CSS frameworks are included by default.

### Development Experience
- Environment-based configuration via `.env` files
- Convenient development commands via mise tasks
- Code formatting and linting enforced via pre-commit hooks and GitHub Actions
- GitHub Actions for continuous integration

### Production Readiness
- Environment-based settings configuration
- (TODO) Rich deployment config and CI/CD

## Getting Started

### Prerequisites
- Git
- [mise](https://github.com/jdx/mise)
- [uv](https://github.com/astral-sh/uv) `mise install uv`

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/django-starter-2025.git
cd django-starter-2025

# Install dependencies
uv sync

# Depending on your mise config you may need to run
source .venv/bin/activate

# Install the pre-commit hook
pre-commit install

# Set up the environment
cp .env.example .env

# Start the development server
mise run dev
```

## Available Commands

- `mise dev` - Run the development server
- `mise test` - Run tests
- `mise format` - Format code with Ruff
- `mise check` - Lint code with Ruff
- `mise migrate` - Apply database migrations
- `mise makemigrations` - Create new migrations

## TODO

- [ ] Add Docker and docker-compose configurations
- [ ] Set up Ansible playbooks for deployment
- [ ] Add Terraform configurations for infrastructure provisioning
- [ ] Add example of DRF API setup
- [ ] Add example of background worker configuration
- [ ] Add example of Channels
- [ ] Implement a deployment guide for various hosting providers

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

The template is licensed under either of

- [Apache License, Version 2.0](LICENSE-APACHE)
- [MIT license](LICENSE-MIT)

at your option.
