# Secure MCP Server



Two MCP servers built with basic tools that were tested upon connection to an AI client (Claude Desktop). 



## Overview

* This project's purpose is to explore command line injection and prompt injection alongside implementing the defenses against them. Course concepts of access control, logging, and software integrity were considered during execution and learning documentation.
* An MCP server is similar to a toolbox that different clients can connect to for access to the tools within it.
* The servers in this project provide the following tools: dns_lookup, ping_host, and get_file_info. These tools are used to demonstrate how an MCP server and its tools can be attacked.

* See LEARNING_LOG.md for learning findings.

## Threats & Defenses



### 1. Command Injection (`ping_host`)



The command line is made to simply follow instructions, so when commands are passed without being verified, the command line has been injected. 



**Before (vulnerable):**

```

> ping_host_unsafe("127.0.0.1 & echo You were hacked > hacked.txt")

> dir hacked.txt

hacked.txt   <-- file created on disk without user permission

```



**After:**

```

> ping_host("127.0.0.1 & echo You were hacked > hacked.txt")

Rejected: '...' is not a valid hostname.

> dir hacked.txt

File Not Found   <-- blocked, no file created

```



**Fixes:** A character allowlist was included to reject the host input if it is empty or if any character is not a letter, digit, dot, or hyphen. This rejects the input before any command runs.



### 2. Least Privilege (`ping_host` target allowlist)



A second allowlist/ validation check was created for only pinging 127.0.0.1 and localhost. Another defense removed the shell and passes the command as a list.

```

> ping_host("127.0.0.1")        -> pings (on allowlist)

> ping_host("trinitywhiting.com") -> Rejected: not on the allowlist of permitted targets

```



### 3. Prompt Injection / Tool Poisoning (`filehelper` server)



This attack lies within the tool's description, which is what the client uses to determine when and how to deploy the tool. The three methods used involved inserting a common tag used by attackers, removing that tag, and inserting instructions in the output.



**Result:** The client detected and refused to deploy the injected instructions across all three variations. 



### 4. Audit Logging



A log was added to document every call of the ping tool. Some results are as follows:



```

2026-10-17T... | tool=ping_host | input='trinitywhiting.com' | result=Rejected: not on allowlist

2026-10-17T... | tool=ping_host | input='127.0.0.1 & echo hi' | result=Rejected: not a valid hostname

```



## Architecture:



The MCP client (Claude Desktop) decides which tool to call and sends the request to the server over stdio. server.py ("netlab") provides network tools, and poisoned_server.py ("filehelper") exists only to demonstrate prompt injection.



## How to Run: (This runs as a local MCP server connected to an MCP client such as Claude Desktop.)



```bash

# 1. Create an isolated environment

conda create -n mcp-project python=3.12

conda activate mcp-project



# 2. Install the MCP SDK

pip install "mcp[cli]"



# 3. Register the server with an MCP client (e.g., Claude Desktop) by

#    adding it to the client's config file, pointing at server.py.

#    Then restart the client and the tools appear.

```



All tests of this project were tested only against my machine and the loopback address using harmless payloads (creating a file, printing a username).



