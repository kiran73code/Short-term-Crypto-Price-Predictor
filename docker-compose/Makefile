# Redpand cluster
redpanda-start:
	docker-compose -f redpanda.yml up -d
	
redpanda-stop:
	docker-compose -f redpanda.yml down


add-one-partition-to-trades-topic:
	docker compose -f redpanda.yml exec redpanda rpk topic add-partitions trades --num 1

# technical-indicators-pipeline

technical-indicators-pipeline-build:
	docker compose -f technical-indicators-pipeline.yml build

technical-indicators-pipeline-run: technical-indicators-pipeline-build
	docker compose -f technical-indicators-pipeline.yml up

technical-indicators-pipeline-stop:
	docker compose -f technical-indicators-pipeline.yml down

	