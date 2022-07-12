# custom prometheus metrics exporter



### Build container image

````bash
# podman build -t custom-exporter:latest .
````

### Run container

````bash
$ podman run --rm --name custom-exporter -p 6666:8888 localhost/custom-exporter \
             --name=my_metric \
             --labels=key1=value1,key2=value2 \
             --port=8888
````

### help

````
$ exporter.py [--name=<some metric name>] \
              [--labels=<key=value>,[<key=value>]] \
              [--port=<port>] \
              [-h]

$ exporter.py --name=my_metrics \
              --labels=app=test1 \
              --port=2000

````

### Payload

Push a metric with one or more labels

````
$ curl http://127.0.0.1:2000/payload?key1=value1&key2=value2
ok
$ curl http://127.0.0.1:2000/payload?key1=value1&key2=value3
ok
$ curl http://127.0.0.1:2000/payload?key1=value1&key2=value3
ok
$ curl http://127.0.0.1:2000/payload?key1=value1&key2=value2
ok
$ curl http://127.0.0.1:2000/payload?key3=value1&key2=value2
ok
$ curl http://127.0.0.1:2000/payload?key3=value1&key2=value2
ok
````

### Metrics

Pull metrics

````bash
$ curl http://localhost:2000/metrics

# HELP shell Number of events
# TYPE shell counter
shell{task="run",key1="value1",key2="value2"} 2
shell{task="run",key1="value1",key2="value3"} 2
shell{task="run",key3="value2",key2="value2"} 2
````

