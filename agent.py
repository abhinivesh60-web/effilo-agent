import logging
from dotenv import load_dotenv
from livekit.agents import JobContext, WorkerOptions, cli
from livekit.agents.voice import Agent, AgentSession
from livekit.plugins import anthropic, sarvam

load_dotenv()
logger = logging.getLogger("effilo-cart-agent")
logger.setLevel(logging.INFO)

AGENT_PROMPT = """You are Ananya, a warm friendly customer care agent for Effilo, a premium clothing brand. A customer abandoned their cart. Remind them gently and help them complete their purchase. Greet them by name, mention items left in cart. Be conversational not salesy. Keep responses under 3 sentences. If Tamil speak Tamil, if Hindi speak Hindi, match Tanglish/Hinglish naturally. Delivery 3-5 days free above Rs999, returns 7-day free pickup, payment UPI cards COD."""

class EffiloCartAgent(Agent):
    def __init__(self, customer_name="there", product_name="some beautiful items", cart_value=""):
        cart_display = f"worth Rs {cart_value}" if cart_value else ""
        super().__init__(
            instructions=AGENT_PROMPT + f"\nCustomer: {customer_name}, Cart: {product_name} {cart_display}",
            stt=sarvam.STT(language="unknown", model="saaras:v3", mode="transcribe", flush_signal=True),
            llm=anthropic.LLM(model="claude-haiku-4-5-20251001"),
            tts=sarvam.TTS(target_language_code="ta-IN", model="bulbul:v3", speaker="kavya"),
        )
    async def on_enter(self):
        self.session.generate_reply()

async def entrypoint(ctx: JobContext):
    parts = ctx.room.name.split("_")
    name = parts[1].replace("-"," ") if len(parts)>1 else "there"
    product = parts[2].replace("-"," ") if len(parts)>2 else "your items"
    value = parts[3] if len(parts)>3 else ""
    session = AgentSession(turn_detection="stt", min_endpointing_delay=0.07)
    await session.start(agent=EffiloCartAgent(name, product, value), room=ctx.room)

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
