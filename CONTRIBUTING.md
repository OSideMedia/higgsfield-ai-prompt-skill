# Contributing

Contributions are welcome! This project is a Claude skill library for Higgsfield AI prompt generation.

## How to contribute

1. **Open an issue first** for major changes so we can discuss the approach.
2. Fork the repo and create a feature branch.
3. Make your changes.
4. Test by running your prompts through Claude with the Higgsfield skill loaded — there's no traditional test suite, so verification means confirming the skill produces correct, high-quality Higgsfield prompts.
5. Open a pull request with a clear description of what changed and why.

## Guidelines

- Keep sub-skill files focused on a single concern.
- Follow the existing MCSLA formula structure for prompt-related changes.
- Update `CHANGELOG.md` if your change is user-facing.
- Model information must stay accurate to current Higgsfield platform capabilities.
- Prompt examples should be production-quality and follow MCSLA structure.
- Cross-references between skill files must resolve to real paths (`python3 validate.py` catches these).

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
