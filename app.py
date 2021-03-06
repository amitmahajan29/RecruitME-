from flask import Flask, render_template, url_for, request, jsonify, redirect, send_file
from flask_cors import CORS, cross_origin
from werkzeug import secure_filename
from scripts.json_handler import *
import nltk
nltk.download("stopwords")
from pyresparser import ResumeParser
import requests
import json
import os
import shutil
from math import ceil
from Naive_Bayes import *
from bs4 import BeautifulSoup


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "data"
CORS(app)




#for candidate
@app.route("/login")
def login():
	return render_template("login.html")
	


@app.route("/signin", methods=["GET", "POST"])
def signin():

	username = request.form["username"]
	password = request.form["password"]

	flag, data = validate(username, password)
	print(data)
	if flag:

		if data["t"] == 1:
			return render_template("index.html", username = username)
		else:
			return render_template("demo.html", username = username, mobile = data["mobile"], emailid = data["emailid"])


	return render_template("login.html", message = "Invalid Name or Password")	



@app.route("/signup_cand", methods=["GET", "POST"])
def signup_cand():

	username = request.form["username"]
	password = request.form["password"]
	mobile = request.form["mobile"]
	emailid = request.form["emailid"]
	github = request.form["github"]
	stackoverflow = request.form["stackoverflow"]
	yocket = request.form["yocket"]
	codechef = request.form["codechef"]	

	signup_user(username, password, mobile, emailid, github, stackoverflow, yocket, codechef, 0)

	return render_template("demo.html", uersname = username, mobile = mobile, emailid = emailid)



@app.route("/signup_rect", methods = ["GET", "POST"])
def signup_rect():

	username = request.form["username"]
	password = request.form["password"]
	mobile = request.form["mobile"]
	emailid = request.form["emailid"]

	signup_user(username, password, mobile, emailid, 1)

	return render_template("index.html")


#For Candidate
@app.route("/demo")
def demo():
	return render_template("demo.html")


def get_query(condition):

  arr = [0 for i in range(len(s_skills))]

  for i in condition:
    if i in d_skills.keys():
      arr[d_skills[i]] = 1

  return arr


@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():

	username = request.form["username"]

	data = load(user)

	f = request.files['file']
	try:
		f.save(secure_filename(f.filename))
		shutil.move(secure_filename(f.filename), "data/")
	except:
		pass
	"""
	print(1234)
	print("data/"+f.filename)
	resume = ResumeParser("data/"+f.filename).get_extracted_data()
	print(1234)
	model = load("data/model.json")
	nb = [Naive_Bayes(model[str(i)]) for i in range(11)]
	print(4321)
	predictions = [nb[i].predict(get_query(resume["skills"])) for i in range(11)]
	data[username]["rating"] = predictions 
	summ = 0
	for i in predictions:
		summ += i[1]
	data[username]["avg_rating"] = summ/11

	data[username]["resume"] = secure_filename(f.filename)
	data[username]["skills"] = resume["skills"]
	data[username]["total_experience"] = resume["total_experience"]
	dump(user, data)
	"""

	#model = load("data/model.json")


	"""
	if True:	
		if request.method == 'POST':
			f = request.files['file']
			#f.save(secure_filename(f.filename))
			#shutil.move(secure_filename(f.filename), "data/")
			print(1111)
			resume = ResumeParser("data/"+secure_filename(f.filename)).get_extracted_data()
			print(resume)
			model = load("data/model.json")
			print(1)
			nb = [Naive_Bayes(model[str(i)]) for i in range(11)]
			print(2)
			print(nb)
			predictions = [nb[i].predict(get_query(resume["skills"])) for i in range(11)]
			data[username]["rating"] = predictions 
			summ = 0
			for i in predictions:
				summ += i[1]
			data[username]["avg_rating"] = summ/11

			data[username]["resume"] = secure_filename(f.filename)
			data[username]["skills"] = resume["skills"]
			data[username]["total_experience"] = resume["total_experience"]
			dump(user, data)
			#os.system("mv ")
	else:
		pass
	"""
	return render_template("demo.html", username = username, mobile = data[username]["mobile"], emailid = data[username]["emailid"])

#For Recruter
@app.route("/index")
def index():
	return render_template("index.html")

@app.route("/rectlogin")
def rectlogin():
	return render_template("rectlogin.html")

@app.route("/postjob")
def postjob():
	return render_template("postjob.html")

@app.route("/profile")
def profile():
	username = request.args.get("username")
	data = load(user)
	print(data[username])
	return render_template("profile.html", username = username, mobile = data[username]["mobile"], emailid = data[username]["emailid"])

@app.route("/tempprofile")
def tempprofile():
	data = load(user)
	username1 = request.args.get("username")
	s_skills = set(['Html', 'Photoshop', 'Mobile', 'Pandas', 'Illustrator', 'Flask', 'Django', 'Nosql', 'Html5', 'Matlab', 'Jupyter', 'Postgresql', 'Keras', 'Css', 'Apis', 'C', 'Anaconda', 'Ui', 'Product', 'Sketch', 'Linux', 'Autocad', 'Excel', 'Jsp', 'Mysql', 'Python', 'Tensorflow', 'Javascript', 'Sql', 'Testing', 'Database', 'Wordpress', 'Selenium', 'Algorithms', 'Pytorch', 'Github', 'Php', 'Oracle', 'Rest', 'C#', 'C++', 'Java', 'Android', 'Ubuntu', 'Nltk', 'Aws', 'Swift', 'R'])
	skills = []
	for i in sorted(data[username1]["skills"]):
		if i in s_skills:
			skills.append(i)
	login_params = {'username': 'atharva456','password': ''}
	username = "Ye11ow-Flash"
	try:
		username = data[username1]["github"]
	except:
		pass
	user1 = requests.get('https://api.github.com/users/'+username)
	#user = requests.get('https://api.github.com/search/users/', params={'q':'sahil'})
	user_json = json.loads(user1.content or user1.text)
	#print(user_json)
	repos = requests.get('https://api.github.com/users/'+username+'/repos', params={'type':'owner','sort':'pushed'})
	repos_json = (json.loads(repos.content))
	language=[]
	for i in repos_json:
		language.append(i['language'])
	print(language)
	language=set(language)
	c_url = "https://www.codechef.com/users/ye11ow_flash"
	try:
		c_url = data[username1]["codechef"]
	except:
		pass
	rating=codechef(c_url)
	s_url = "https://stackoverflow.com/users/10905798/sangram-desai"
	try:
		#s_url = data[username1]["stackoverflow"]
		pass
	except:
		pass
	stack=stackoverflow(s_url)
	return render_template("profile.html",mobile = data[username1]["mobile"], emailid = data[username1]["emailid"],username=username1,follower=user_json["followers"],following=user_json["following"],totalrepo=user_json["public_repos"],language=language,rating=rating,stack=stack, sl=len(stack), skills=skills)

def codechef(url):
	rating=[]
	source_code = requests.get(url)
	plain_text=source_code.text
	soup = BeautifulSoup(plain_text)
	info=[]
	for link in soup.findAll('div',{'class' : 'rating-number'}):
		info.append(link.string)
	#print(info[0])
	rating.append(info[0])
	for link in soup.findAll('li'):
		info.append(link.text)
	#print(info[67])
	#print(info[66])
	rating.append(info[67].split()[0])
	rating.append(info[66].split()[0])
	return rating

def stackoverflow(url):
	#url = "https://stackoverflow.com/users/10905798/sangram-desai"
	source_code = requests.get(url)
	plain_text=source_code.text
	soup = BeautifulSoup(plain_text)
	info=[]
	# grid--cell ws-nowrap
	for link in soup.findAll('div', class_ = 'profile-top-tags'):
		info.append(link.text)
		temp = soup.find('span', class_ = 'fc-medium fs-title')
		# temp2 = soup.find('span', class_ = 'mr4 fw-bold tt-uppercase')
		if temp == None:
			continue
		for j in temp:
			info.append(j)


	s = str(info)
	# print(s)
	skillset = []
	sk = s.split('\\r')[0]
	sk = sk.split('\\n')
	for i in sk:
		if i != '':
			skillset.append(i)
	skillset = skillset[1:]
	skillset = skillset[0:4]+skillset[6:]
	print(skillset)
	return skillset


@app.route("/load_data")
def load_data():

	try:
		experience = int(request.args.get("experience"))
	except:
		experience = 0
	position = request.args.get("position")
	skill = request.args.get("skill")

	print(position, experience, skill)

	if position == "":

		data1 = load(user)
		data = {}
		for i in data1.keys(): 
			if data1[i]["t"] == 0 and data1[i]["total_experience "] >= experience:
				if skill == "":
					data[i] = data1[i]
				elif skill in data1[i]["skills"]:
					data[i] = data1[i]

		arr = sorted([[data[i]["avg_rating"], ceil(data[i]["total_experience "]), data[i]["resume"], i, data[i]["emailid"]] for i in data.keys()], reverse=True)

		return jsonify(data = arr)

	else:

		data1 = load(user)
		data = {}
		for i in data1.keys():
			if data1[i]["t"] == 0 and data1[i]["total_experience "] >= experience:
				if skill == "":
					data[i] = data1[i]
				elif skill in data1[i]["skills"]:
					data[i] = data1[i]

		arr = sorted([[data[i]["rating"][int(position)-1], ceil(data[i]["total_experience "]), data[i]["resume"], i, data[i]["emailid"]] for i in data.keys()], reverse=True)

		return jsonify(data = arr)







	#return render_template("index.html")
	return ""


@app.route("/get_pdf", methods=["GET", "POST"])
def get_pdf():
	username = request.form["username"]
	print(username,"username")
	data =load(user)
	print(data[username]["resume"])

	return send_file('data/'+data[username]["resume"], as_attachment=True)


if __name__ == "__main__":
   	app.run(debug = True)


   
   