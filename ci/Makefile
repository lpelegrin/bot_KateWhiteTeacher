#
# DOCKER COMMANDS
#
docker-build:
	docker build -t lpelegrin/bot-katewhiteteacher:$(VERSION) -f Dockerfile ../src/.
docker-push: docker-build
	docker push lpelegrin/bot-katewhiteteacher:$(VERSION)

docker-build-test:
	docker build -t lpelegrin/bot-katewhiteteacher:test -f Dockerfile ../src/.
docker-push-test: build-test
	docker push lpelegrin/bot-katewhiteteacher:test

#
# HELM COMMANDS
#
helm-delete:
	helm delete 

helm-prod:
	helm delete katewhiteteacher-prod || true
	helm upgrade -i -f helm/values.prod.yaml -n default katewhiteteacher-prod helm/.

helm-test:
	helm delete katewhiteteacher-test || true
	helm upgrade -i -f helm/values.test.yaml -n default katewhiteteacher-test helm/.