# nfs_exporter_py
Source code for https://hub.docker.com/repository/docker/elghali/nfs_exporter_py

# nfs_exporter_py

This is a prometheus exporter that collects metrics using a python script. The script's main function is to expose the number of files in a directory specified by `dir_path` parameter.
Usage
---
```
git clone https://github.com/elghali/nfs_exporter_py.git
cd nfs_exporter_py
python3 script-exporter-py [dir_path]

[Try it](https://loclhost:9469)

```

## Docker

`docker run -it -v "[dir_path]:[dir_path]" -p 9469:9469 -e dir_path="[dir_path]" -d elghali/nfs_exporter_py:1.0`

## K8s
To try the exporter on K8s we can use the below sample deployment or visit [examples](https://github.com/elghali/nfs_exporter_py/examples) for more examples.
```
---
kind: ConfigMap
apiVersion: v1
metadata:
  name: nfs-exporter-py
  namespace: nfs-exporter
  labels:
    app.kubernetes.io/name: nfs-exporter-py
data:
  config.yaml: |
    dir_path: /home/elghali,/home/elghali/myFiles
    port: 9469
    metric_freq: 60
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nfs-exporter-py
  namespace: nfs-exporter
  labels:
    app.kubernetes.io/name: nfs-exporter-py
spec:
  replicas: 1
  selector:
    matchLabels:
      app.kubernetes.io/name: nfs-exporter-py
  template:
    metadata:
      labels:
        app.kubernetes.io/name: nfs-exporter-py
    spec:
      containers:
        - name: nfs-exporter-py
          image: elghali/nfs_exporter_py:1.4
          ports:
            - name: http
              containerPort: 9469
              protocol: TCP
          livenessProbe:
            failureThreshold: 3
            httpGet:
              path: /
              port: 9469
              scheme: HTTP
            initialDelaySeconds: 10
            periodSeconds: 10
            successThreshold: 1
            timeoutSeconds: 10
          readinessProbe:
            failureThreshold: 3
            httpGet:
              path: /
              port: 9469
              scheme: HTTP
            periodSeconds: 10
            successThreshold: 1
            timeoutSeconds: 10
          volumeMounts:
            - name: config
              mountPath: /nfs_exporter_py/config.yaml
              subPath: config.yaml
            - mountPath: /ni
              name: nfs-root
      volumes:
        - name: config
          configMap:
            name: nfs-exporter-py
            defaultMode: 0777
        - name: nfs-root
          nfs:
            path: <mountPath>
            server: <nfsIp>

```

## Config.yaml properties

| Option | Default | Description
| ----------- | ----------- | ----------- |
| dir_path | /opt | NFS path(s) to montior
| port | 9469 | Exposed port |
| metric_freq | 10 | Metrics scraping frequency |