# [luisnabais/cloudflare-ddns](https://github.com/luisnabais/docker-cloudflare-ddns)

This code consists on a few components:
- Python script, which connects to Cloudflare to update a DNS entry
- Dockerfile, to build the image for the Python script. Based on Python official slim image
- docker-compose example file

## Supported Architectures

It should support most architectures, however, I just built it for arm64v8.


## Usage

Here are some example snippets to help you get started creating a container.

### docker-compose (recommended, [click here for more info](https://docs.linuxserver.io/general/docker-compose))

```yaml
---
version: '2.1'
services:
  cloudflare-ddns:
    image: luisnabais/cloudflare-ddns:1.0
    container_name: cloudflare-ddns
    hostname: cloudflare-ddns
    environment:
      - EMAIL=example@mail.com
      - API_KEY=a8dd892bd2a0a69187358b1ce7f7cabc2f85
      - HOSTNAME=home.example.com
      - ZONE_ID=6ef3e0abc8ad776905a522c2ceb6f7d0
      - RECORD_ID=99ebe0933256654a8f0ec19d2a16fa50
      - TTL=600
    restart: unless-stopped
```

### docker cli ([click here for more info](https://docs.docker.com/engine/reference/commandline/cli/))

```bash
docker run -d \
  --name=cloudflare-ddns \
  -e EMAIL=example@mail.com \
  -e API_KEY=a8dd892bd2a0a69187358b1ce7f7cabc2f85 \
  -e HOSTNAME=home.example.com \
  -e ZONE_ID=6ef3e0abc8ad776905a522c2ceb6f7d0 \
  -e RECORD_ID=99ebe0933256654a8f0ec19d2a16fa50 \
  -e TTL=600 \
  --restart unless-stopped \
  luisnabais/cloudflare-ddns:1.0
```

### Directly execution of the script

```bash
./update_ddns.py \
	--email example@mail.com \
    --api-key a8dd892bd2a0a69187358b1ce7f7cabc2f85 \
	--hostname home.example.com \
    --zone-id 6ef3e0abc8ad776905a522c2ceb6f7d0 \
    --record-id 99ebe0933256654a8f0ec19d2a16fa50 \
    --ttl 600
```

## Parameters

| Parameter | Function |
| :----: | --- |
| `-e EMAIL=example@mail.com` | CloudFlare E-mail. |
| `-e API_KEY=a8dd892bd2a0a69187358b1ce7f7cabc2f85` | Account global CloudFlare API Key. |
| `-e HOSTNAME=home.example.com` | The hostname/DNS to update. |
| `-e ZONE_ID=6ef3e0abc8ad776905a522c2ceb6f7d0` | The Zone ID where the hostname is. It can be checked on the CloudFlare account. |
| `-e RECORD_ID=99ebe0933256654a8f0ec19d2a16fa50` | The Record ID for the entry to update. Run once the script manually without record id as parameter, it will return all records, just get the record ID to insert here. |
| `-e TTL=600` | The interval in seconds to update the DNS entry. 600 is 10 minutes. |


## Updating Info

Below are the instructions for updating containers:

### Via Docker Compose

* Update all images: `docker-compose pull`
  * or update a single image: `docker-compose pull cloudflare-ddns`
* Let compose update all containers as necessary: `docker-compose up -d`
  * or update a single container: `docker-compose up -d cloudflare-ddns`

### Via Docker Run

* Update the image: `docker pull luisnabais/cloudflare-ddns:1.0`
* Stop the running container: `docker stop cloudflare-ddns`
* Delete the container: `docker rm cloudflare-ddns`
* Recreate a new container with the same docker run parameters as instructed above.

* You can also remove the old dangling images: `docker image prune`

## Building locally

If you want to make local modifications to these images for development purposes or just to customize the logic:

```bash
git clone https://github.com/luisnabais/docker-cloudflare-ddns.git
cd docker-cloudflare-ddns
docker build \
  --no-cache \
  --pull \
  -t luisnabais/cloudflare-ddns:1.0 .
```
## Versions

* **11.05.22:** - Initial Release.
