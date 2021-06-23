## Development machine

### Build

docker buildx build --platform linux/arm -t quay.io/dejanb/drogue-dht-py -f Dockerfile --push .


### Create Drogue device

drg create app dejanb

drg create device --app dejanb pi --data '{"credentials":{"credentials":[{"pass":"foobar"}]}}'

## Host machine

## Run container

~~~sh
sudo docker run --privileged --rm -ti --device=/dev/gpiochip0 \
-e ENDPOINT=https://http.sandbox.drogue.cloud/v1/foo \
-e APP_ID=dejanb \
-e DEVICE_ID=pi \
-e DEVICE_PASSWORD=foobar \
-e GEOLOCATION="{\"lat\": \"44.8166\", \"lon\": \"20.4721\"}" \
quay.io/dejanb/drogue-dht-py:latest
~~~

## Install service

Copy [docker.drogue.service] to `/etc/systemd/system/docker.drogue.service`

~~~sh
sudo systemctl enable docker.drogue.service
sudo reboot
~~~
