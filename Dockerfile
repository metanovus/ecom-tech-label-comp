FROM python:3.11-slim-bookworm
WORKDIR /app
COPY . .

RUN python -m venv venv
RUN . venv/bin/activate && pip install --no-cache-dir -r requirements.txt

CMD . venv/bin/activate && streamlit run app/streamlit_test.py --server.port $PORT --server.address $HOST_NAME
