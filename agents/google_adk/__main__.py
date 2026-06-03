from server.server import A2AServer
from models.agent import AgentCard, AgentCapabilities, AgentSkill
from agents.google_adk.task_manager import AgentTaskManager
from agents.google_adk.agent import TellTimeAgent
import click
import logging

@click.command()
@click.option("--host", default="localhost", help="Host to bind the server to")
@click.option("--port", default=10002, help="Port number for the server")
def main(host, port):
    capabilities = AgentCapabilities(streaming=False)
    skill = AgentSkill(
        id="tell_time",
        name="Tell Time Tool",
        description="Replies with the current time",
        tags=["time"],
        examples=["What time is it?", "Tell me the current time"],
    )

    agent_card = AgentCard(
        name = "TellTimeAgent",
        description = "This agent replies with the current system time.",
        url = f"http://{host}:{port}",
        version = "1.0.0",
        defaultInputModes = TellTimeAgent.SUPPORTED_CONTENT_TYPES,
        defaultOutputModes = TellTimeAgent.SUPPORTED_CONTENT_TYPES,
        capabilities=capabilities,
        skills=[skill]
    )

    server = A2AServer(
        host=host,
        port=port,
        agent_card=agent_card,
        task_manager=AgentTaskManager(agent=TellTimeAgent())
    )

    server.start()

if __name__ == "__main__":
    main()