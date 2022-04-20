from jira import JIRA
from time import sleep

import pandas as pd
import json


username = 'Your username'
api_token = 'Your jira token'
server = 'Your jira server'
project_key = "'Your project'"
jql = 'Your jql'

jira = JIRA(server=server, basic_auth=(username, api_token))

block_size = 1
block_num = 0
jira_search = jira.search_issues(
    jql,
    startAt=block_size * block_num,
    maxResults=block_size,
    fields=('summary, issuetype, status, reporter, assignee, sprint'),
    expand='changelog'
)

index_beg = 0
header = True
mode = 'w'

while bool(jira_search):
    data_jira = []
    for issue in jira_search:
        # print(issue.__dict__)
        queue = issue.key
        summary = issue.fields.summary
        request_type = str(issue.fields.issuetype)

        reporter_login = None
        reporter_name = None
        reporter = issue.raw['fields'].get('reporter', None)
        if reporter is not None:
            reporter_login = reporter.get('key', None)
            reporter_name = reporter.get('displayName', None)

        status = None
        st = issue.fields.status
        if st is not None:
            status = st.name

        data_jira.append((summary, queue, request_type, status, reporter_name, ))

    # print(data_jira)

    index_end = index_beg + len(data_jira)

    data_jira = pd.DataFrame(data_jira, index=range(index_beg, index_end),
                             columns=['summary', 'queue', 'type', 'status', 'reporter_name'])
    data_jira.to_json(path_or_buf='data_jira.json', indent=1, index=False,
                      orient='table', force_ascii=True)

    block_num += 1
    index_beg = index_end
    header = False
    mode = 'a'

    if block_num % 50 == 0:
        print(block_num * block_size)

    sleep(1)

    jira_search = False


jira.close()

