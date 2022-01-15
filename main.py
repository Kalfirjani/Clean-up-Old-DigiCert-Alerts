#!/usr/bin/env python
import requests
import json
import sys
import os
import re
from sending_email import send_email

last_day_of_prev_month = date.today().replace(day=1) - timedelta(days=1)

start_day_of_prev_month = date.today().replace(day=1) - timedelta(days=last_day_of_prev_month.day)

base_url = 'https://api.pagerduty.com'
service_id = ''
statuses = ''
since = str(start_day_of_prev_month)
until = str(last_day_of_prev_month)
pagerduty_key = os.environ['pagerduty_key']
api_key = pagerduty_key
pagerduty_key2 = os.environ['pagerduty_key2']
api_key2 = pagerduty_key2
headers = {
    'Authorization': 'Token token={0}'.format(api_key),
    'Content-type': 'application/json',
    'Accept': 'application/vnd.pagerduty+json;version=2'
}



def get_incidents(since, until, offset, service_id=None, statuses=None, total_incidents=[]):
    params = {
        'service_ids': [service_id],
        'statuses': ["acknowledged"],
        'since': since,
        'until': until,
        'offset': offset,
        'limit': 100
    }
    r = requests.get(
        '{0}/incidents'.format(base_url),
        headers=headers,
        data=json.dumps(params)
    )
    if r.json()['more']:
        total_incidents.extend(r.json()['incidents'])
        offset += 100
        return get_incidents(since, until, offset, service_id, total_incidents)
    else:
        total_incidents.extend(r.json()['incidents'])
        return total_incidents

def get_incidents_id(incident_id):

    r = requests.get(
        '{0}/incidents/{1}/log_entries?include[]=channels'.format(
            base_url, incident_id
        ),
        headers=headers
    )

    return incident_id

def main():
    counter = 0
    incident_list = []
    if service_id != '' and statuses != "resolved":
       incidents = get_incidents(since, until, 0, service_id)

       for incident in incidents:
            id = get_incidents_id(incident['id'])
            incident_list.append(id)
            counter += 1
            payload = {"incident": {
            "type": "incident_reference",
            "status": "resolved"
                  }}
            headers = {
                      "Content-Type": "application/json",
                      "Accept": "application/vnd.pagerduty+json;version=2",
                      "From": "your email",
                      "Authorization": "Token token={0}".format(api_key2)
                  }
            url = "https://api.pagerduty.com/incidents/{}".format(id)
            response = requests.request("PUT", url, json=payload, headers=headers)  
    email_body = """\
                      <html>
                        <body>
                         <p><b>DigiCert Acknowledged Incidents ID Below:</b>
                         <table>
                             <tr>{}</tr>
                        </table>
                        <table>
                         </p><b>"DigiCert Alerts has been Successfully Resolved for one Month ago!", {}"</b>
                      </body>
                    </html>""".format(incident_list, counter)

    send_email(email_body)

if __name__ == '__main__':
    main()
