# Makefile for BillGeneratorUnified

.PHONY: test lint format dev install

install:
	pip install -r requirements.txt

test:
	.venv\Scripts\python.exe -m pytest tests/ -v

lint:
	.venv\Scripts\python.exe -m ruff check .

format:
	.venv\Scripts\python.exe -m black .
	.venv\Scripts\python.exe -m ruff check --fix .

dev:
	.venv\Scripts\python.exe -m streamlit run app.py
