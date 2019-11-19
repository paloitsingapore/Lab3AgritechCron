#!/bin/bash
  curl https://hub.docker.com/v2/repositories/agritechpaloit/webapp/tags 2>/dev/null|jq '."results"[]["last_updated"]'
