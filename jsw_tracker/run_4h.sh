#!/bin/bash
# 4-hourly refresh (box side). IG play counts come from the Mac mini (~/jsw_tracker/ig_read.py via AdsPower headless);
# copy its latest JSON to ig_latest.json before this runs. Notion apply is done by an agent via MCP unless NOTION_TOKEN is set.
cd /workspace/jsw_tracker
ARGS=""; [ -f ig_latest.json ] && ARGS="$ARGS --ig-json ig_latest.json"; [ -f x_latest.json ] && ARGS="$ARGS --x-json x_latest.json"
python3 refresh.py $ARGS > out/last_run.log 2>&1
