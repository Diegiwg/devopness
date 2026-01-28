from typing import Any
from fastmcp.mcp_config import MCPConfig, RemoteMCPServer
from fastmcp.server.proxy import ProxyClient
from fastmcp import FastMCP


def exec_proxy() -> None:
    transport = MCPConfig(
        mcpServers={
            "devopness": RemoteMCPServer(
                url="https://dev-mcp.devopness.com/mcp/",
                transport="streamable-http",
                auth="devopness_pat_1768952148qQJCffqnnNe6tQKaOQWIOmJp7k4GDIxb7NKvIPyt0uhJWF9vtjOoW74SV7aAFF8o3HBdti4mBDcp",
            ),
        }
    )

    proxy_client: ProxyClient[Any] = ProxyClient(
        transport,
        elicitation_handler=None,
    )

    proxy = FastMCP.as_proxy(proxy_client)

    proxy.run(
        transport="stdio",
        show_banner=False,
    )


def run() -> None:
    # Here, should get any cli args if needed
    exec_proxy()


if __name__ == "__main__":
    run()
