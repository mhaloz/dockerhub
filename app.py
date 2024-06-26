#from flask import Flask

#app = Flask(__name__)

#@app.route('/')
#def hello_world():
#   return 'Hello Jenkins webhookss'

#if __name__ == '__main__':
 #   app.run(debug=True)

#

from fastapi import FastAPI
import mangum
import uvicorn
 
app = FastAPI()
 
@app.get("/")
def read_root():
    return {"Hello": "jenkins_cicd_pipeline"}
 
handler = mangum.Mangum(app)
 
if __name__ == "__main__":
   uvicorn.run(app, host="0.0.0.0", port=8080)
