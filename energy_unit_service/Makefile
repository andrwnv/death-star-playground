PROJECTNAME=$(shell basename "$(PWD)")

MAKEFLAGS += --silent

default: help
.PHONY: help
all: help

## install: Install dependencies.
install:
	@echo " Installing dependencies of $(PROJECTNAME) ..."
	@pip3 install -r requirements.txt


## gen: Generate proto files.
gen:
	@echo " Start "$(PROJECTNAME)" ..."

	@python3 -m grpc_tools.protoc \
		-Iproto/energy_unit=../protos \
		--python_out=. \
		--grpc_python_out=. \
		../protos/registration.proto

	@python3 -m grpc_tools.protoc \
		-Iproto/energy_unit=../protos/energy-unit \
		--python_out=. \
		--grpc_python_out=. \
		../protos/energy-unit/energy_unit.proto

## run: Start in development mode.
run:
	@echo " Start "$(PROJECTNAME)" ..."
	@python3 main.py -c ./configs/dev/config.yaml


help: Makefile
	@echo
	@echo " Choose a command run in "$(PROJECTNAME)":"
	@echo
	@sed -n 's/^##//p' $< | column -t -s ':' |  sed -e 's/^/ /'
	@echo
