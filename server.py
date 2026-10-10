import socket
from mcp.server import MCPServer

mcp = MCPServer("NetLab")

@mcp.tool()
def dns_lookup(hostname: str) -> str:
    """Look up the IPv4 address of a hostname, like example.com"""
    ip = socket.gethostbyname(hostname)
    return f"{hostname} resolves to {ip}"


if __name__ == "__main__":
    mcp.run()