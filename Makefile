.PHONY: dev-up dev-down dev-logs smoke mock-capture

dev-up:
	docker compose -f infra/compose.dev.yaml up --build

dev-down:
	docker compose -f infra/compose.dev.yaml down

dev-logs:
	docker compose -f infra/compose.dev.yaml logs -f

smoke:
	./scripts/compose-smoke.sh

mock-capture:
	python3 tools/mock-capture/mock_capture.py
