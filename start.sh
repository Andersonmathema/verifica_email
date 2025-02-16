#!/bin/bash

# Se $PORT não estiver definido, usa 8501 como padrão (localmente)
PORT=${PORT:-8501}

streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true


