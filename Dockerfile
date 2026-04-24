FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir "livekit-agents[sarvam,anthropic,silero]" python-dotenv
COPY agent.py .
CMD ["python", "agent.py", "start"]
