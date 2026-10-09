# Monolithic Context Dump (Anti-Pattern Starter)

This starter file demonstrates what happens when a team dumps 500+ lines of raw API schemas, stale debugging transcripts, and contradicting style rules directly into a single root context file without `@path` progressive references or cross-session memory separation.

- Raw inline SQL schema dumps consume thousands of startup tokens on every turn.
- Ephemeral debugging notes ("tried fixing port 8081 on Tuesday") are mixed with permanent project architecture rules.
- Build and test commands are buried on line 412 instead of at the top of the file.
- Worktree subdirectories write to separate ad-hoc notes files instead of sharing the git-repo-scoped auto-memory directory (`~/.claude/projects/<project>/memory/`).
