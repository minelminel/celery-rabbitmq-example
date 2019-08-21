
def report_ready(url):
    json_data = dict(url=url,status='READY')
    return json_data


def report_done(url):
    json_data = dict(url=url,status='DONE')
    return json_data
