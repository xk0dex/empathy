# Contributing to Empathy

¡Gracias por tu interés en contribuir a Empathy! 🚀 This project analyzes team health through Git commit patterns, and we welcome contributors from all backgrounds.

## Quick Start

1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/YOUR_USERNAME/empathy.git`
3. **Install** dependencies: `pip install -r requirements.txt`
4. **Run** tests: `pytest tests/`
5. **Create** a branch: `git checkout -b feature/your-feature-name`

## Ways to Contribute

### 🐛 Report Bugs
Found a bug? Please check existing issues first, then create a new one with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version)

### 💡 Suggest Features
Have an idea? We'd love to hear it! For feature requests:
- Check the [roadmap](ROADMAP.md) first
- Describe the use case and motivation
- Consider implementation complexity
- Be open to discussion and iteration

### 📝 Improve Documentation
Documentation improvements are always welcome:
- Fix typos or unclear explanations
- Add code examples
- Translate content to Spanish
- Create tutorials or guides

### 🔧 Code Contributions
Ready to code? Great! Here's how:

#### Good First Issues
Look for issues labeled `good first issue` - these are designed for newcomers:
- UI improvements (tooltips, styling)
- Documentation updates
- Small feature additions
- Test coverage improvements

#### Development Workflow
1. **Check existing issues** or create one for discussion
2. **Fork and clone** the repository
3. **Create a feature branch** with descriptive name
4. **Write tests** for your changes
5. **Follow code style** (we use Black for formatting)
6. **Update documentation** if needed
7. **Submit a PR** with clear description

## Development Setup

### Prerequisites
- Python 3.8+
- Git access to analyze repositories
- GitHub Personal Access Token (for API access)

### Installation
```bash
# Clone the repository
git clone https://github.com/xk0dex/empathy.git
cd empathy

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests to verify setup
pytest tests/
```

### Running Empathy
```bash
# Analyze a repository
python src/main.py --repo https://github.com/user/repo --token YOUR_GITHUB_TOKEN

# Start dashboard
python src/dashboard/app.py
```

## Code Style & Standards

### Python Style
- **Black** for code formatting: `black src/ tests/`
- **isort** for import sorting: `isort src/ tests/`
- **flake8** for linting: `flake8 src/ tests/`
- **Type hints** encouraged for new code

### Testing
- Write tests for new features
- Maintain test coverage above 80%
- Use meaningful test names
- Test both happy path and edge cases

### Documentation
- Docstrings for all public functions
- Clear commit messages
- Update README if needed
- Add examples for new features

## Pull Request Process

### Before Submitting
- [ ] Tests pass locally (`pytest tests/`)
- [ ] Code is formatted (`black src/ tests/`)
- [ ] Documentation updated if needed
- [ ] Commit messages are clear

### PR Description Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Refactoring

## Testing
- [ ] Tests added/updated
- [ ] Manual testing completed
- [ ] No regression in existing functionality

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests pass
```

### Review Process
1. **Automated checks** must pass (CI/CD pipeline)
2. **Maintainer review** (we aim for 48h response time)
3. **Address feedback** promptly and respectfully
4. **Merge** once approved (squash and merge preferred)

## Community Guidelines

### Code of Conduct
We follow the [Contributor Covenant](https://www.contributor-covenant.org/). In summary:
- Be respectful and inclusive
- Welcome newcomers and different perspectives
- Focus on constructive feedback
- Report inappropriate behavior

### Communication
- **GitHub Issues**: Bug reports, feature requests
- **GitHub Discussions**: General questions, ideas
- **Pull Requests**: Code contributions and reviews
- **Email**: security@empathy-project.com for security issues

### Recognition
Contributors are recognized in:
- Release notes
- CONTRIBUTORS.md file
- GitHub contribution graph
- Special mentions for significant contributions

## Areas Needing Help

### High Priority
- 🌍 **Spanish localization** for UI and documentation
- ⚡ **Performance optimization** for large repositories
- 📊 **Historical trend visualization** implementation
- 🔧 **GitLab support** development

### Medium Priority
- 🎨 **UI/UX improvements** for better user experience
- 📚 **Documentation expansion** with more examples
- 🧪 **Test coverage** improvement
- 🔌 **Integration development** (Slack, Discord)

### Ongoing
- 🐛 **Bug fixes** and stability improvements
- 🔍 **Code review** and quality assurance
- 💬 **Community support** and issue triage
- 📝 **Content creation** (blogs, tutorials)

## Questions?

Don't hesitate to ask! We're here to help:
- 📋 **Create an issue** for specific questions
- 💬 **Start a discussion** for general topics
- 📧 **Email maintainers** for sensitive matters

**Remember**: No contribution is too small. Whether it's fixing a typo, adding a feature, or helping other contributors, every effort matters! 🙌

---

*Thank you for helping make Empathy better for teams worldwide!* ❤️