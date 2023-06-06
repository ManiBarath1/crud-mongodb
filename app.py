from flask import Flask,render_template,redirect,request,url_for
from flask_pymongo import PyMongo


app=Flask(__name__)
app.config['MONGO_URI']='mongodb://localhost:27017/crud'
mongo=PyMongo(app)

@app.route("/")
def home():
    l1=[]
    l2=[]
    item_coll=mongo.db.item
    user_coll=mongo.db.user
    for i in item_coll.find():
        l1.append(i)
    for j in user_coll.find():
        l2.append(j)
    return render_template("index.html",I=l1,U=l2)

@app.route("/additem",methods=["POST","GET"])
def add_item():
    if request.method=="POST":
        iname=request.form.get("iname")
        quantity=request.form.get("icount")
        price=request.form.get("iprice")
        total=int(quantity)*int(price)
        coll=mongo.db.item
        coll.insert_one({'IName':iname,'Quantity':quantity,'Price':price,"Total":total})
        return redirect(url_for("home"))
    return render_template("item.html")

@app.route("/adduser",methods=["POST","GET"])
def add_user():
    if request.method=="POST":
        UName=request.form.get("uname")
        Mobile=request.form.get("umobile")
        Loc=request.form.get("uloc")
        coll=mongo.db.user
        coll.insert_one({'UName':UName,'Mobile':Mobile,'Loc':Loc})
        return redirect(url_for("home"))
    return render_template("user.html")

@app.route("/iupdate/<string:iname>",methods=["POST","GET"])
def iupdate(iname):
    if request.method=="POST":
        iname=request.form.get("iname")
        quantity=request.form.get("icount")
        price=request.form.get("iprice")
        total=int(quantity)*int(price)
        coll=mongo.db.item
        coll.update_one({'IName':iname},{'$set':{"Quantity":quantity,"Price":price,"Total":total}})
        return redirect(url_for("home"))
    coll=mongo.db.item
    item=coll.find_one({"IName":iname})
    return render_template("iupdate.html",item=item)

@app.route("/uupdate/<string:uname>",methods=["POST","GET"])
def uupdate(uname):
    if request.method=="POST":
        mobile=request.form.get("umobile")
        loc=request.form.get("uloc")
        coll=mongo.db.user
        coll.update_one({'UName':uname},{'$set':{"Mobile":mobile,"Loc":loc}})
        return redirect(url_for("home"))
    coll=mongo.db.user
    user=coll.find_one({"UName":uname})
    return render_template("uupdate.html",user=user)

@app.route("/idelete/<string:iname>",methods=["GET"])
def idelete(iname):
    coll=mongo.db.item
    coll.delete_one({"IName":iname})
    return redirect(url_for("home"))

@app.route("/udelete/<string:uname>",methods=["GET"])
def udelete(uname):
    coll=mongo.db.user
    coll.delete_one({"UName":uname})
    return redirect(url_for("home"))




if __name__=="__main__":
    app.run(debug=True)