# Contributing to Virtual Gamepad

Thank you for your interest in contributing to Virtual Gamepad! This document provides guidelines and instructions for contributing.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue on GitHub with:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior vs actual behavior
- Your environment (OS, Python version, browser)
- Any relevant log files or error messages

### Suggesting Enhancements

We welcome feature suggestions! Please create an issue with:
- A clear description of the feature
- Why you think it would be useful
- Any implementation ideas you have

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** following our coding standards
3. **Test your changes** thoroughly
4. **Update documentation** if needed
5. **Commit your changes** with clear, descriptive commit messages
6. **Push to your fork** and submit a pull request

### Coding Standards

#### Python Code
- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Add docstrings to functions and classes
- Keep functions focused and modular
- Add logging for debugging purposes

#### JavaScript Code
- Use meaningful variable names
- Comment complex logic
- Maintain consistent indentation (2 spaces)
- Test on both desktop and mobile browsers

#### HTML/CSS
- Use semantic HTML elements
- Keep styles organized and commented
- Ensure responsive design works on various screen sizes
- Test on iOS Safari (iPad), Chrome, and Firefox

### Commit Message Guidelines

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

### Testing

Before submitting a pull request:
- Test on Windows with vJoy installed
- Test the web interface on multiple browsers
- Test touch functionality on an actual mobile device
- Verify WebSocket connections work properly
- Check that button configurations save correctly

### Development Setup

1. Clone your fork:
   ```bash
   git clone https://github.com/your-username/virtual-gamepad.git
   cd virtual-gamepad
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

5. Make your changes and test

6. Commit and push:
   ```bash
   git add .
   git commit -m "Add your feature description"
   git push origin feature/your-feature-name
   ```

### Areas for Contribution

Here are some areas where contributions would be particularly welcome:

- **Cross-platform support**: Make the input mapper work on macOS and Linux
- **Additional input types**: Support for analog sticks, sliders, or D-pads
- **Themes**: Create different UI themes or layouts
- **Mobile app**: Native iOS/Android app version
- **Configuration UI**: Improve the button editor interface
- **Documentation**: Tutorials, videos, or additional examples
- **Testing**: Unit tests and integration tests
- **Performance**: Optimize WebSocket communication or rendering
- **Accessibility**: Improve keyboard navigation and screen reader support

### Code Review Process

- All pull requests require review before merging
- Reviewers will check for:
  - Code quality and adherence to standards
  - Proper testing
  - Documentation updates
  - No breaking changes without discussion

### Questions?

If you have questions, feel free to:
- Open an issue for discussion
- Comment on existing issues or pull requests
- Reach out to the maintainers

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all. Please be respectful and considerate in all interactions.

### Our Standards

- Be kind and courteous
- Respect differing viewpoints and experiences
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members

Thank you for contributing! 🎮

