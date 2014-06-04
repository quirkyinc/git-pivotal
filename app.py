import os
import simplejson
import requests
import logging
from os.path import abspath, dirname, join

from flask import Flask, request


app = Flask(__name__)
app_path = abspath(dirname(__file__))
PIVOTAL_URL = "http://www.pivotaltracker.com/services/v3/source_commits"


def get_api_token(email):
    json_file_path = abspath(join(dirname(__file__), 'pivotal_tokens.json'))
    json_result = simplejson.loads(open(json_file_path).read())
    for user, user_values in json_result.get('github_hook').get('user_api_tokens').iteritems():
        if user_values.get('email') == email:
            return user_values.get('api_token')
    return json_result.get('github_hook').get('default_api_token')


def form_xml_post_data(commit):
    message = commit.get('message')
    author = commit.get('author').get('name')
    commit_id = commit.get('id')
    url = commit.get('url')
    commit_xml = "<source_commit><message>%s</message><author>%s</author><commit_id>%s</commit_id><url>%s</url></source_commit>" % (message, author, commit_id, url)
    return commit_xml


@app.route('/', methods=['POST'])
def process_hook():
    url = PIVOTAL_URL
    try:
        payload = request.values.get('payload')
        payload_json = simplejson.loads(payload)
        commits = payload_json.get('commits')
        if commits:
            api_token = get_api_token(commits[0].get('author').get('email'))

        for commit in commits:
            xml_data = form_xml_post_data(commit)
            req = requests.post(url, data=xml_data,
                headers={
                    'X-TrackerToken': api_token,
                    'Content-type': 'application/xml',
                }
            )
            if not req:
                logging.debug(
                    u"Commiting ticket to pivotal resulted in an error."
                    " %s url with data %s and api_token %s",
                    url, xml_data, api_token
                )
    except Exception:
        logging.exception("Exception when attempting to process payload")
        return "Your hook made trouble so nothing done."
    else:
        return "Thank your for your hook"

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
