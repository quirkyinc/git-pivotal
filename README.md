git-pivotal
=================

A small repo to host code for git pivotal integration.

This is a simple utility that adds a post commit hook and updates pivotal tracker with status updates that we indicate in our git commits.

## SETUP

To get started, fork this repo and update the [pivotal_tokens.json](https://github.com/nityaoberoi/git-pivotal/blob/master/pivotal_tokens.json) with the following information:

* Github URL: This is the github url of your project. E.g.: https://github.com/nityaoberoi/git-pivotal
* Pivotal Project ID: You can find this in the url of your pivotal project. It is the <:id> listed in https://www.pivotaltracker.com/n/projects/<:id>
* Default Token: This is only used as a backup token. In case one of your developers updates their token incorrectly, this default token will be used to update the Pivotal Story. This means that the ticket is updated with the author name associated with the default token.
* Share your forked repo url with your team and have them add their individual pivotal tokens in this format under user_api_tokens:
        ```
        "Your Name" : {
                "email" : "you+github@email.com",
                "api_token": "pivotal-api-token"
            }
        }
        ```

## USAGE

* Once you deploy your app on heroku, update your git project webhooks
* Commit format
