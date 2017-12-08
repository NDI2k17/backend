from flask import Flask
from flask import abort
from flask import json
from flask import redirect
from flask import request
from flask import url_for
from flask import make_response

import os, time

# ########################################################
def _external_add(sessionId, _dict):
    # Check if the sessionId is known
    pass

def _external_get_answer(question, sessionId):
    return json.dumps(
        dict(question=question, sessionId=sessionId))

def _external_get_history(sessionId):
    return {}

# ########################################################
def get_answer(question, sessionId):
    _external_add(sessionId, dict(
        timestamp=time.time(),
        who='user',
        message=question
    ))

    answer = _external_get_answer(
        question=question, sessionId=sessionId)

    _external_add(sessionId, dict(
        timestamp=time.time(),
        who='bot',
        message=answer
    ))

    return answer

# ########################################################
# History will be a list of elements, with each elements
#   formatted like this:
# {'timestamp':1512685346.413079, 'who':'user',
# 'message':'Hello'}
def get_history(sessionId):
    raise NotImplementedError

# ########################################################
# I've created some types of exception in order to handle
#   errors
class InvalidSession(RuntimeError):pass
class UnknownUser(InvalidSession):pass
class UndefinedUser(InvalidSession):pass
# ########################################################
app = Flask(__name__)
app.debug = True

# Only used in debug
defaultSessionId = 'ffffffffffffffffffffffffffffffff'

# If we debug, we will route everything here, else,
#  we will route only POST and refuse the other
@app.route("/api/answer/", methods=['POST', 'GET'])
@app.route("/api/answer/<question>", methods=['POST', 'GET'])
def api_answer(question=None):
    if question is None:
        # I havn't found a way to parse it
        question = request.get_data()
        length = len('question=')
        try:
            index = request.get_data().lower().index('question=')
        except ValueError:
            return '{"error":"Please give us a \'question\' field in data"}', 401
        question = question[index + length:]
        if '&' in question:
            question = question[:question.index('&')]

    if request.method.upper() == 'GET' and not app.debug:
        return '{"error":"Please use POST instead of GET"}', 405

    try:
        # KeyError will only be caught for this line
        try:
            sessionId = request.cookies['session']
        except KeyError:
            raise InvalidSession()
        else:
            return make_response(
                json.dumps(dict(
                    answer=get_answer(
                        question=question,
                        sessionId=sessionId
                    )
                ))
            )
    except InvalidSession:
        if app.debug:
            response = redirect(url_for(
                'api_answer', question=question
            ))
            response.set_cookie('session', defaultSessionId)
            return response
        else:
            return '{"error":"Please give us a valid session id"}'


@app.route("/api/history/", methods=['POST', 'GET'])
def api_history():
    try:
        # KeyError will only be caught for this line
        try:
            sessionId = request.cookies['session']
        except KeyError:
            raise InvalidSession()
        else:
            return make_response(
                json.dumps(dict(
                    answer=get_history(
                        sessionId=sessionId
                    )
                ))
            )
    except InvalidSession:
        if app.debug:
            response = redirect(url_for(
                'api_history'
            ))
            response.set_cookie('session', defaultSessionId)
            return response
        else:
            return '{"error":"Please give us a valid session id"}'
    return _external_get_history(sessionId=sessionId)

    '''if 'session' not in request.cookies:
        if not app.debug:
            return json.dumps({'error':'Please add cookies'}), 401
        response = app.make_response(redirect())
        response.set_cookie('session', defaultSessionId)'''
    "userSession = request.cookies['session']"


# ####################################
# Default path => Send a 404
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def default(path):
    abort(404)


def main():
    app.run(host=os.getenv('IP', '0.0.0.0'),
            port=int(os.getenv('PORT', 4444)))

if __name__ == '__main__':
    main()
