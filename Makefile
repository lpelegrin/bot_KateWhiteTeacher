#
# DOCKER COMMANDS
#
docker-build:
	docker build -t lpelegrin/bot-katewhiteteacher:$(VERSION) -f ci/Dockerfile src/.
docker-push: docker-build
	docker push lpelegrin/bot-katewhiteteacher:$(VERSION)

docker-build-test:
	docker build -t lpelegrin/bot-katewhiteteacher:test -f ci/Dockerfile src/.
docker-push-test: docker-build-test
	docker push lpelegrin/bot-katewhiteteacher:test

#
# HELM COMMANDS
#
helm-prod:
	helm delete katewhiteteacher-prod || true
	helm upgrade -i -f ci/helm/values.prod.yaml -n kate-prod katewhiteteacher-prod ci/helm/.

helm-test:
	helm delete katewhiteteacher-test || true
	helm upgrade -i -f ci/helm/values.test.yaml -n kate-test katewhiteteacher-test ci/helm/.

#
# CUSTOM
#
try: docker-push-test helm-test

trigger-job-test:
	kubectl get pods -n kate-test --no-headers -o=custom-columns=NAME:.metadata.name | xargs -I{} kubectl exec -n kate-test {} -- bash -c "python3 main.py job"
trigger-job-prod:
	kubectl get pods -n kate-prod --no-headers -o=custom-columns=NAME:.metadata.name | xargs -I{} kubectl exec -n kate-prod {} -- bash -c "python3 main.py job"	