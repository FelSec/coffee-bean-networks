# Coffee Bean Networks

A simple pyhton-based web application and Couchbase environment for testing N1QL injection techniques and tooling.

## Launching the environment

**Important Note: The first time launching the environment will take about 5 minutes or so, subsequent lauches will take about 2 minutes.**

### Build Locally

```
git clone https://github.com/FelSec/coffee-bean-networks
cd coffee-bean-networks
docker build -t cbn-n1ql .
docker run -d --name cbn-n1ql -P cbn-n1ql
```

### Pre-built Image

```
docker pull felsec/cbn-n1ql:latest
docker run -d --name cbn-n1ql -P felsec/cbn-n1ql
```

**By default the application runs on port 5000, this can be changed to any port using `-p <port>:5000`. E.G. `-p 80:5000**
