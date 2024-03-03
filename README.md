# Death Star Playground

## Run
### <u>Simple way</u>
```bash
$ docker-compose up
```

### <u>Difficult way</u>

1. Install and run RabbitMQ
2. Install all requirements for each service
3. Configure each service
4. Manually run services

Manual service setup example:
```bash
$ cd energy_unit_service
$ pip3 install -r requirements.txt
$ cp configs/dev/config.yaml config.yaml && nano config.yaml
$ python3 main.py -c config.yaml
```

## Misc dependencies
- `GRPC v1.60.0`
- `RabbitMQ v3.12`
- `Python v.3.10`
