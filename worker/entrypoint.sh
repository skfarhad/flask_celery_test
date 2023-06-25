#!/bin/sh
set -e

#celery -A tasks worker --loglevel INFO --pool=solo
celery -A tasks worker --loglevel INFO
