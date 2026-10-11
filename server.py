import socket #for dns_lookup
import subprocess #for ping_host_unsafe
from mcp.server import MCPServer

mcp = MCPServer("NetLab")

@mcp.tool()
def dns_lookup(hostname: str) -> str:
    """Look up the IPv4 address of a hostname, like example.com"""
    ip = socket.gethostbyname(hostname)
    return f"{hostname} resolves to {ip}"

@mcp.tool()
def ping_host_unsafe(host: str) -> str:
    """Ping a host to check if it is reachable (insecure version)"""
    command = "ping -n 1 " + host #the glued host string is the vulnerability
    #using shell=True within the subprocess module exposes the application to OS Command Injection vulnerabilities
    result = subprocess.run(command, shell=True, capture_output=True, text=True) #capture the output as text
    return result.stdout

if __name__ == "__main__":
    mcp.run()