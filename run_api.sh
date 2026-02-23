#!/bin/bash

source venv/bin/activate
uvicorn src.infrastructure.controllers.rag_controller:app --reload --host 0.0.0.0 --port 8000
