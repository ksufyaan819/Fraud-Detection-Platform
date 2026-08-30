# /fraud-detection-platform/Makefile

.PHONY: data train up down

data:
	python scripts/generate_data.py

train:
	python scripts/train_model.py

retrain:
	python scripts/retrain_from_feedback.py

up:
	docker compose -f docker/docker-compose.yml up --build -d

down:
	docker compose -f docker/docker-compose.yml down