# An example of DHT sensor and Drogue cloud

This example shows how to connect your DHT-22 temperature sensor to Drogue cloud.

These instructions will not cover how to connect the sensor to the Raspberry Pi as there are multiple sources for that online already.

We'll go into the details on how to build and run a container image and connect it to the Drogue cloud.

## Development machine

To create an image you need to use cross-platform build on non-arm platforms, like
### Build

```sh
docker buildx build --platform linux/arm -t quay.io/dejanb/drogue-dht-py -f Dockerfile --push .
```

### Create Drogue device

Next, you should create an application and device on the [Drogue cloud](https://sandbox.drogue.cloud/).

For more information about Drogue IoT project, refer to https://www.drogue.io/#getting-started

```sh
drg create app dejanb

drg create device --app dejanb pi --data '{"credentials":{"credentials":[{"pass":"foobar"}]}}'
```

## Host machine

## Run container

On you Edge node, you can now run the workload like

```sh
sudo docker run --privileged --rm -ti --device=/dev/gpiochip0 \
-e ENDPOINT=https://http.sandbox.drogue.cloud/v1/foo \
-e APP_ID=dejanb \
-e DEVICE_ID=pi \
-e DEVICE_PASSWORD=foobar \
-e GEOLOCATION="{\"lat\": \"44.8166\", \"lon\": \"20.4721\"}" \
quay.io/dejanb/drogue-dht-py:latest
```

## Install service

You can also use systemd to make workload auto-start on device boot.

Copy [docker.drogue.service](docker.drogue.service) to `/etc/systemd/system/docker.drogue.service`

~~~sh
sudo systemctl enable docker.drogue.service
sudo reboot
~~~
