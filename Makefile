run:
	docker build -t exporter:latest . &&  docker run -d --restart unless-stopped -p 9879:9879 exporter:latest