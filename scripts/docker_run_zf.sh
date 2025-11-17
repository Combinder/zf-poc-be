docker run -d --name zf-poc-be \
  --restart unless-stopped \
  --network network1 \
  --ip 10.0.2.135 \
  --env-file /mnt/vol0/docker/zf-poc-be/prod.env \
  zf-poc-be:v0.1.0