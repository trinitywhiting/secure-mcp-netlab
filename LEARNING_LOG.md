# Learning Log: Secure MCP Network Lab



## 2026-10-09



**Goal:**

* Understand how AI clients accessing MCP servers can be vulnerable to command injection and prompt injection.



**What I did:**

* Command injection: Created an MCP server (netlab) and used the Claude Desktop App as the client for connection. The server included networking ping and DNS tools. The client was used in the Claude Code tab, with permissions for tools set to "needs approval" and "auto" mode within the chat. Local MCP server logs were viewed to show successful initialization of the server and tool access, and the DNS tool was tested directly in the client. Both unsafe and safe versions of the ping tool were created to conduct isolated tests of command injection.

  * The tool tests went as expected, with the unsafe version following injected instructions directly and the safe version preventing injection with validation checks.
* Tool poisoning: Created an MCP server (FileHelper) with the same settings from the netlab sever, with the exception of "auto" mode. Manual mode was used after connecting the client to the server and viewing the logs. The client was tested to see if it would follow malicious instructions from the tool's description using three payload variations:
1. Inserting the <IMPORTANT> tag into the tool's description; result: the client resisted, flagged it, and pointed it out to the user as prompt injection 
2. Removing the tag and injecting tool description directly; result: the client resisted, flagged it, and pointed it out to the user
3. Manipulating the output



*What I learned - Command Injection:**

* A separate environment is necessary to remain organized and prevent projects from potentially breaking due to relying on specific dependencies.



* It's important to verify packages before installing them to avoid compromising security. The "mcp\[cli]" comes directly from Anthropic's SDK; however it's important to note that the installation of the package also included over 30 other packages that were simply trusted (not verified). This is how a supply chain attack can occur.



* I verified that my MCP server loaded properly by viewing the server logs in the Claude Desktop's developer settings. The logs showed me how the client communicated with the server to initialize and load the tools it contained.



* An interesting point: When testing that the tool functioned properly, I noticed the app didn't request permission to run the tool. It executed without permission. I checked the app's connectors and navigated to my MCP server, which showed that tool permissions are set to "needs approval;" however, that particular chat was also in Claude's Auto mode, which uses a classifier that denies requests that are irreversible, destructive, or aimed outside my environment (https://code.claude.com/docs/en/auto-mode-config). Following further Anthropic documentation,  I found that using the permissions.ask mechanism can force a human-in-the loop interaction (https://code.claude.com/docs/en/auto-mode-config).



* After creating the unsafe ping tool, I checked for command injection by passing in the loopback address and "\& whoami" (using shell=True vulnerability). Both sides of the command ran, demonstrating how the command line simply follows syntax. This matters because Claude chooses the host value, which is sometimes read from text, so injected text could run commands on my machine.



* Removing shell=true and using a list means a bad input cannot trigger a second command, and the validation check returns a rejection message.



**What I learned - Prompt Injection:**

* The AI Client uses the docstring description of the tool to determine when and how to use it. Attackers use tags such as <IMPORTANT>, <CRITICAL>, <URGENT>, etc. to draw focus. My testing with the used client shows that the tags made no difference.
* The defenses against prompt injection within a malicious server rely mostly on the client and the user.
