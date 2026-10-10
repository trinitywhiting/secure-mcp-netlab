\# Learning Log: Secure MCP Network Lab



\## 2026-10-09



\*\*Goal:\*\*



\*\*What I did:\*\*

\-



\*\*What I learned:\*\*

\-A separate environment is necessary to remain organized and prevent projects from potentially breaking due to relying on specific dependencies.

\-It's important to verify packages before installing them to avoid compromising security. The "mcp\[cli]" comes directly from Anthropic's SDK; however it's important to note that the installation of the package also included over 30 other packages that were simply trusted (not verified). This is how a supply chain attack can occur.

\-I verified that my MCP server loaded properly by viewing the server logs in the Claude Desktop's developer settings. The logs showed me how the client communicated with the server to initialize and load the tools it contained.

\-An interesting point: When testing that the tool functioned properly, I noticed the app didn't request permission to run the tool. It executed without permission. I checked the app's connectors and navigated to my MCP server, which showed that tool permissions are set to "needs approval;" however, that particular chat was also in Claude's Auto mode, which uses a classifier that denies requests that are irreversible, destructive, or aimed outside my environment (https://code.claude.com/docs/en/auto-mode-config). Following further Anthropic documentation,  I found that using the permissions.ask mechanism can force a human-in-the loop interaction (https://code.claude.com/docs/en/auto-mode-config).

&#x20;

