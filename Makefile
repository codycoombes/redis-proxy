build:
	docker-compose build redis && docker-compose build proxy

run:
	docker-compose up -d redis && docker-compose up -d proxy

stop:
	docker-compose down -v

test:
	docker-compose build && docker-compose up