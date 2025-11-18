# Contributing to LeetCode Learning Platform

Thank you for your interest in contributing! 🎉

## Development Guidelines

Please follow the project's [Development Guidelines](docs/DEVELOPMENT_GUIDELINES.md) for:
- Code standards
- File size limits (max 500 lines)
- Testing requirements
- Commit conventions

## How to Contribute

### 1. Fork the Repository

Click the "Fork" button at the top right of the repository page.

### 2. Clone Your Fork

```bash
git clone https://github.com/YOUR_USERNAME/leetcode-learning-platform.git
cd leetcode-learning-platform
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 4. Make Your Changes

- Write clean, readable code
- Follow existing code style
- Add comments where necessary
- Keep files under 500 lines
- Test your changes thoroughly

### 5. Commit Your Changes

```bash
git add .
git commit -m "feat: add amazing feature"
```

**Commit Message Format:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

### 6. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 7. Create a Pull Request

1. Go to the original repository
2. Click "New Pull Request"
3. Select your fork and branch
4. Describe your changes
5. Submit the PR

## Code Review Process

1. Maintainers will review your PR
2. Address any requested changes
3. Once approved, your PR will be merged

## Development Setup

See [README.md](README.md) for full setup instructions.

Quick setup:
```bash
# Backend
cd backend
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

## Testing

```bash
# Backend tests (when implemented)
cd backend
pytest

# Frontend tests (when implemented)
cd frontend
npm test
```

## Questions?

Feel free to open an issue for any questions or concerns!

Thank you for contributing! 🚀

