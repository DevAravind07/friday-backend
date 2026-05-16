from dotenv import load_dotenv

from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    WorkerOptions,
    cli,
    room_io,
)

from livekit.plugins import (
    google,
    noise_cancellation,
)

from prompt import (
    AGENT_INSTRUCTION,
    AGENT_RESPONSE,
)

load_dotenv()


class Assistant(Agent):

    def __init__(self) -> None:
        super().__init__(
            instructions=AGENT_INSTRUCTION
        )


async def entrypoint(ctx: JobContext):

    session = AgentSession(

        llm=google.realtime.RealtimeModel(

            model="gemini-2.0-flash-exp",

            modalities=["TEXT"],

            voice="Erinome",

            temperature=0.8,

            instructions=f"""
            {AGENT_INSTRUCTION}

            {AGENT_RESPONSE}
            """,
        )
    )

    await session.start(

        room=ctx.room,

        agent=Assistant(),

        room_options=room_io.RoomOptions(

            audio_input=room_io.AudioInputOptions(

                noise_cancellation=noise_cancellation.BVC(),
            ),
        ),
    )

    await session.generate_reply(

        instructions="""
        Greet the user warmly.

        Introduce yourself as SAAM.

        Speak naturally, softly, and affectionately.

        Ask how you can help today.
        """
    )


if __name__ == "__main__":

    cli.run_app(

        WorkerOptions(
            entrypoint_fnc=entrypoint,
        )
    )