# Contributing

For reproducibility problems, open an issue with the commit or tag, operating
system and architecture, commands run, and any error or result that differed.
Share aggregate results and redact private information from logs.

For a fix, fork the repository, create a branch, and run
`pixi run --locked reproduce` and `pixi run --locked check` before opening a pull request.
Describe the fix and the checks you ran. Keep the GitHub Reproduce check green.

Keep downloaded data and generated outputs out of Git. Commit changes to
`pixi.toml` and `pixi.lock` together.
