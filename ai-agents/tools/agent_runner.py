import os
from dataclasses import dataclass, field
from typing import Optional, Dict, Any

from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.events.event import types

@dataclass
class SessionConfig:
    """
    Configuration for the ADK Session.
    Use initial_state to pass 'memory' like bucket names or project IDs.
    """
    app_name: str = "DataEngineering"
    user_id: str = "ozkary"
    session_id: str = "session_001"
    initial_state: Dict[str, Any] = field(default_factory=dict)

async def setup_pipeline_runner(target_agent, config: SessionConfig):
    """
    Initializes the agnostic In-Memory session service and the ADK Runner.
    """
    session_service = InMemorySessionService()
    
    # Initialize the session with the provided configuration state
    await session_service.create_session(
        app_name=config.app_name, 
        user_id=config.user_id, 
        session_id=config.session_id, 
        state=config.initial_state
    )
    
    runner = Runner(
        agent=target_agent,
        app_name=config.app_name,
        session_service=session_service
    )
    return session_service, runner

async def run_agent_task(agent, prompt: str, config: Optional[SessionConfig] = None) -> str:
    """
    Agnostic task runner. Works for any agent (BQ, GCS, QA).
    Positions the AI as a cognitive partner using the ADK Runner pattern.
    """
    # Fallback to default config if none is passed from the notebook
    if config is None:
        config = SessionConfig()

    print(f"--- [TASK START]: {agent.name} ---")
    final_response = "No response captured."

    try:
        # Setup the local execution environment
        session_service, runner = await setup_pipeline_runner(agent, config)
        
        # Standard ADK message wrapping
        content = types.Content(role='user', parts=[types.Part(text=prompt)])

        # Stream the response for that 'real-time' feeling in the demo
        events = runner.run_async(
            user_id=config.user_id, 
            session_id=config.session_id, 
            new_message=content
        )
        
        async for event in events:
            # tool calls
            # if event.is_tool_call() and event.content and event.content.parts:
            #     print(f"--- [TOOL CALL]: {event.content.parts[0].function_call.name} ---")

            if event.is_final_response():
                for part in event.content.parts:
                        if part.text:
                            final_response += part.text
                
            # Identify the specific agent speaking in the console
            print(f"[{agent.name}]: {final_response}")
    except Exception as e:
        if "429" in str(e):
            print("Quota limit hit  RPM")
        
        final_response = f"Error: {str(e)}"

    print(f"--- [TASK COMPLETE]: {agent.name} ---\n")
    return final_response