from datetime import datetime
from google.adk.sessions import InMemorySessionService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.artifacts import InMemoryArtifactService
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.agents.llm_agent import LlmAgent
from google.genai import types
import asyncio
from dotenv import load_dotenv
load_dotenv()

''' # in the same shell where Ollama is running  
setx OLLAMA_API_BASE "http://localhost:11434" '''

class TellTimeAgent:

    SUPPORTED_CONTENT_TYPES = ["text","text/plain"]


    def __init__(self):
        self._agent = self.__build_agent()
        self._user_id = "time_agent_user"

        self._runner = Runner(
            app_name = self._agent.name,
            agent = self._agent,
            artifact_service = InMemoryArtifactService(),
            session_service = InMemorySessionService(),
            memory_service = InMemoryMemoryService(),
        )

    def __build_agent(self) -> LlmAgent:
        return LlmAgent(
            model=LiteLlm(model="ollama_chat/llama3.2:1B"),
            name="tell_time_agent",
            description="Tells the current time",
            instruction="Reply with the current time in the format YYYY-MM-DD HH:MM:SS",
        )

    def invoke(self, query: str, session_id: str) -> str:
        session = self._runner.session_service.get_session(
            app_name=self._agent.name,
            user_id=self._user_id,
            session_id=session_id
        )

        if session is None:
            session = self._runner.session_service.create_session(
                app_name=self._agent.name,
                user_id=self._user_id,
                session_id=session_id,
                state={}
            )

        content = types.Content(
            role="user",
            parts=[types.Part.from_text(text=query)]
        )   

        events = list(self._runner.run(
            user_id=self._user_id,
            session_id=session_id,
            new_message=content
        ))

        if not events or not events[-1].content or not events[-1].content.parts:
            return ""
        
        return "\n".join([part.text for part in events[-1].content.parts if part.text])
    
    async def stream(self, query: str, session_id: str):
        yield {
            "is_task_complete": True,
            "content": f"The current time is : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        }