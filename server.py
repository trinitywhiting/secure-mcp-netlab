import socket #for dns_lookup
import subprocess #for ping_host_unsafe
from mcp.server import MCPServer
from datetime import datetime

mcp = MCPServer("NetLab")


def audit_log(tool_name: str, user_input: str, result: str) -> None:
    timestamp = datetime.now().isoformat()
    line = f"{timestamp} | tool={tool_name} | input={user_input!r} | result={result}\n"
    with open("audit.log", "a", encoding="utf-8") as f: #utf-8 for consistency / universality
        f.write(line)

@mcp.tool()
def dns_lookup(hostname: str) -> str:
    """Look up the IPv4 address of a hostname, like example.com"""
    ip = socket.gethostbyname(hostname)
    return f"{hostname} resolves to {ip}"

@mcp.tool()
def ping_host_unsafe(host: str) -> str: #Python hands the string to the shell
    """Ping a host to check if it is reachable (insecure version)"""
    command = "ping -n 1 " + host #the glued host string is the vulnerability
    #using shell=True within the subprocess module exposes the application to OS Command Injection vulnerabilities
    result = subprocess.run(command, shell=True, capture_output=True, text=True) #capture the output as text
    return result.stdout

allowed_hosts = {"127.0.0.1", "localhost"}
@mcp.tool()
def ping_host(host:str) -> str: #python runs the ping program directly; no shell/ no injection opportunity
    """Ping a host to check if it is reachable"""
    #allowlist
    if not host or not all(c.isalnum() or c in ".-" for c in host): #if the host is empty or if any char is not a letter, digit, dot, or hyphen, then reject it 
        result = f"Rejected: '{host}' is not a valid hostname."
        audit_log("ping_host", host, result)
        return result
    if host not in allowed_hosts:
        result = f"Rejected: '{host}' is not on the allowlist of permitted targets."
        audit_log("ping_host", host, result)
        return result
    output = subprocess.run(
        ["ping", "-n", "1", host], #list method prevents injection
        capture_output=True, text=True
    )
    audit_log("ping_host", host, "pinged successfully")
    return output.stdout


if __name__ == "__main__":
    mcp.run()