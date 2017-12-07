from flask import Flask, abort, json, redirect, request

# ########################################################
def get_answer(question):
    return question

# ########################################################
def get_history(sessionId):
    pass
# ########################################################
app = Flask(__name__)
app.debug = True

defaultSessionId = 'ffffffffffffffffffffffffffffffff'

# If we debug, we will route everything here, else, we will route only POST ...
decorator = (
             if app.debug else app.route("/api/answer/<question>", methods=['POST']))

# ... and refuse the other
if not app.debug:
    @app.route("/api/answer/<question>", methods=['GET'])
    def api_answer_get(question):

@app.route("/api/answer/<question>", methods=['POST', 'GET'])
def api_answer(question):
    if request.method:
        return '{"error":"Please use POST instead of GET"}', 405

    if 'session' not in request.cookies:
        make_response
        if app.debug:
            .set_cookie('session', defaultSessionId)
    '''if 'session' not in request.cookies:
        if not app.debug:
            return json.dumps({'error':'Please add cookies'}), 401
        response = app.make_response(redirect())
        response.set_cookie('session', defaultSessionId)'''
    "userSession = request.cookies['session']"
    return json.dumps(dict(
        answer=f(x)
    ))


# ####################################
# Default path => Send a 404
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def default(path):
    abort(404)


def main():
    app.run()


if __name__ == '__main__':
    main()
