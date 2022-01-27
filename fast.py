import fastapi
from fastapi import FastAPI
from fastapi.responses import FileResponse
app = FastAPI()
@app.get("/")
def home(): #root
  return{"Data":"Test"}

@app.get("/about")
def about():
  return{"Data":"Help"}

@app.get("/question1")
def question1():
	return FileResponse("question1.png")
@app.get("/question2")
def question2():
	return FileResponse("question2.png")
@app.get("/question3")
def question3():
	return FileResponse("question3.png")
@app.get("/question4")
def question4():
	return FileResponse("question4.png")
@app.get("/question5")
def question5():
	return FileResponse("question5.png")