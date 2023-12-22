from flask import Flask,Response, make_response

app = Flask(__name__)
@app.route("/")
def view():
    resp = make_response("这是响应内容")
    resp.headers["hello"] = "world"
    resp.status = '404 NOT FOUND'
    return resp

if __name__ == "__main__":
    app.run(debug=True)