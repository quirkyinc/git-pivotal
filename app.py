import requests
import logging
from lxml import etree
from os import environ
from os.path import abspath, dirname, join

from flask import Flask, request


app = Flask(__name__)
app_path = abspath(dirname(__file__))
PIVOTAL_URL = "http://www.pivotaltracker.com/services/v3/source_commits"
XML_nodes = {
    'source_commit': ['message', 'author', 'commit_id', 'url']
}


def get_api_token(email):
    """
    Looks at the pivotal token configuration file and returns the appropriate
    API token associated with this email, else returns the default api token
    specified. This is the email that will be used when displaying a commit on
    the associated pivotal tracker ticket.
    """
    json_file_path = abspath(join(dirname(__file__), 'pivotal_tokens.json'))
    json_result = simplejson.loads(open(json_file_path).read())
    for user, user_values in json_result.get('github_hook').get('user_api_tokens').iteritems():
        if user_values.get('email') == email:
            return user_values.get('api_token')
    return json_result.get('github_hook').get('default_api_token')


def form_xml_post_data(commit):
    """
    Builds and returns XML for the post data to pivotal tracker.
    "<source_commit>
        <message>%s</message>
        <author>%s</author>
        <commit_id>%s</commit_id>
        <url>%s</url>
    </source_commit>" % (message, author, commit_id, url)
    """
    for key_node, nodes in XML_nodes.iteritems():
        root = etree.Element(key_node)
        for node in nodes:
            child = etree.Element(node)
            if node == 'commit_id':
                node = 'id'
            child.text = str(commit.get(node))
            root.append(child)
    return etree.tostring(root)


@app.route('/', methods=['POST'])
def process_hook():
    url = PIVOTAL_URL
    try:
        payload_json = request
        debugger
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
                    " {} url with data {} and api_token {}".format(url, xml_data, api_token)
                )
    except Exception:
        logging.exception("Exception when attempting to process payload")
        return "Your hook made trouble so nothing done."
    else:
        return "Thank your for your hook"

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
