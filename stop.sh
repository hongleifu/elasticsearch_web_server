#!/bin/bash
ps aux | grep python | grep search_web_server | awk '{print $2}' | xargs kill -9
