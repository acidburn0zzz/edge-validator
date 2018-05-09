# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import time
import rapidjson as json
from app import app


app.config['TESTING'] = True
client = app.test_client()


def validate_sample(namespace, name, messages):
    start = time.time()
    fail = 0
    for msg in messages:
        route = '/' + namespace
        rv = client.post(route,
                         data=msg,
                         content_type='application/json')
        fail += int(rv.status_code == 400)
    end = time.time()
    total = len(messages)
    err_rate = fail/float(total)
    print(
        "ErrorRate: {:.2f}%\t"
        "Total: {}\t"
        "Time: {:.1f} seconds\t"
        "DocType: {}.{}"
        .format(err_rate, total, end-start, namespace, name)
    )


def report_telemetry(path):
    for root, _, files in os.walk(path):
        for name in files:
            filename = os.path.join(root, name)
            messages = []
            with open(filename, 'r') as f:
                for line in f:
                    content = json.loads(line).get('content', {})
                    messages.append(content)
            namespace = os.path.basename(root)
            validate_sample(namespace, name, messages)


if __name__ == '__main__':
    report_telemetry('resources/data/')
