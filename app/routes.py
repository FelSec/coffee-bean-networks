from flask import render_template, request, jsonify, json
from app import app
import re
import os
from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions
from couchbase.auth import PasswordAuthenticator
from couchbase.exceptions import CouchbaseException, AuthenticationException
from dotenv import load_dotenv

load_dotenv()

flags_data = [
    {"name": "Flag One", "solved": False, "value": os.getenv("FLAGONE")},
    {"name": "Flag Two", "solved": False, "value": os.getenv("FLAGTWO")},
    {"name": "Flag Three", "solved": False, "value": os.getenv("FLAGTHREE")},
    {"name": "Flag Four", "solved": False, "value": os.getenv("FLAGFOUR")},
]


# Routes
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/blog")
def blog():
    # Check if the 'id' query parameter is provided
    blog_id = request.args.get("id")
    # Check if the 'debug' query parameter is provided
    if "debug" in request.args:
        debug_flag = True
    else:
        debug_flag = False

    if blog_id:
        # FLAG ONE - Vulnerable request - requires debug to view
        blog_post = get_post_by_id(blog_id)

        if blog_post:
            debug_data = f"Input: select (select content,id,title from blog_posts where id='{blog_id}')\nOutput: {json.dumps(blog_post,indent = 4, separators = (',', ': '))}"
            return render_template(
                "blog-post.html", post=blog_post, debug=debug_flag, data=debug_data
            )
        else:
            return page_not_found({"error": "Blog post not found"})
    else:
        blog_posts = get_all_posts()
        return render_template("blog.html", posts=blog_posts)


@app.route("/status")
def status():
    action = request.args.get("action")
    status = request.args.get("status")
    if status:
        update_status(status)
    current_status = get_current_status(action)
    if not current_status:
        return handle_bad_request(
            {"error": "Issue getting the server status! Please REFRESH to try again."}
        )
    # FLAG TWO - vulnerable request - Update server status - boolean blind
    return render_template("status.html", msg=current_status)


@app.route("/shop")
def shop():
    # FLAG FOUR - vulnerable request / param: product - curl
    if "product" not in request.args:
        product_data = get_all_products()
        if not product_data:
            return page_not_found(
                {"error": "Unable to load the shop. Please try again later!"}
            )
        return render_template("shop.html", products=product_data)

    product_id = request.args.get("product")
    product_detail = get_product_by_id(product_id)
    if not product_detail:
        return page_not_found({"error": "Product not found"})

    return render_template("product.html", product=product_detail)


@app.route("/flags", methods=["GET", "POST"])
def flags():
    msg = None
    if request.method == "POST":
        flag = request.values.get("flag")
        if flag:
            msg = check_flag(flag)
        else:
            msg = {"error": "Check what you're sending!"}
    return render_template("flags.html", flags=flags_data, message=msg)


# API Endpoints
@app.route("/api/blog", methods=["GET"])
def get_blog_posts():
    return jsonify(get_all_posts())


@app.route("/api/blog/<string:index>", methods=["GET"])
def get_blog_post(index):
    post = get_post_by_id(index)
    if post:
        return jsonify(post)
    else:
        return jsonify({"error": "Blog post not found"}), 404


@app.route("/api/status", methods=["GET"])
def get_status():
    return jsonify({"status": "Service is running"})


# FLAG THREE - vulnerable request in path - lang is vulnerable to injection
@app.route("/api/<string:lang>/ping", methods=["GET"])
def get_ping(lang):
    try:
        auth = PasswordAuthenticator(
            os.getenv("DB_USERNAME_THREE"), os.getenv("DB_PASSWORD_THREE")
        )
        cluster_opts = ClusterOptions(auth)
        cluster = Cluster("couchbase://localhost", cluster_opts)

        query = f"select ans from languages where code='{lang}'"
        rows = cluster.query(query)
        results = None
        for row in rows:
            if not row.get("ans"):
                continue
            results = {"response": row["ans"]}
        if results:
            return jsonify({"response": "pong!"})
        return jsonify({"error": "Translation not found"})
    except (CouchbaseException, AuthenticationException):
        return jsonify({"error": "Error retreiving langauge information."})


# Error Handling
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template("error.html", error=e), 404


@app.errorhandler(400)
def handle_bad_request(e):
    # note that we set the 404 status explicitly
    return render_template("error.html", error=e), 400


# generic functions
def get_post_by_id(index):
    try:
        auth = PasswordAuthenticator(
            os.getenv("DB_USERNAME_ONE"), os.getenv("DB_PASSWORD_ONE")
        )
        cluster_opts = ClusterOptions(auth)
        cluster = Cluster("couchbase://localhost", cluster_opts)

        query = f"SELECT (select id, title, content FROM blog_posts WHERE id='{index}')"
        rows = cluster.query(query)
        results = []
        for row in rows:
            results.append(row)
        if results != []:
            return results
        return None
    except (CouchbaseException, AuthenticationException):
        return None


def get_all_posts():
    try:
        auth = PasswordAuthenticator(
            os.getenv("DB_USERNAME_ONE"), os.getenv("DB_PASSWORD_ONE")
        )
        cluster_opts = ClusterOptions(auth)
        cluster = Cluster("couchbase://localhost", cluster_opts)

        query = "select id, title, content FROM blog_posts order by id"
        rows = cluster.query(query)
        results = []
        for row in rows:
            results.append(
                {"id": row["id"], "title": row["title"], "content": row["content"]}
            )
        return results
    except (CouchbaseException, AuthenticationException):
        return []


def get_all_products():
    try:
        auth = PasswordAuthenticator(
            os.getenv("DB_USERNAME_FOUR"), os.getenv("DB_PASSWORD_FOUR")
        )
        cluster_opts = ClusterOptions(auth)
        cluster = Cluster("couchbase://localhost", cluster_opts)

        query = "select id, name, description, strength, beans, flavours, intensity, suffix, price FROM products order by id"
        rows = cluster.query(query)
        results = []
        for row in rows:
            results.append(
                {
                    "id": row["id"],
                    "name": row["name"],
                    "description": row["description"],
                    "strength": row["strength"],
                    "beans": row["beans"],
                    "flavours": row["flavours"],
                    "intensity": row["intensity"],
                    "suffix": row["suffix"],
                    "price": row["price"],
                }
            )
        if results != []:
            return results
        return None
    except (CouchbaseException, AuthenticationException):
        return None


def get_product_by_id(product_id):
    try:
        auth = PasswordAuthenticator(
            os.getenv("DB_USERNAME_FOUR"), os.getenv("DB_PASSWORD_FOUR")
        )
        cluster_opts = ClusterOptions(auth)
        cluster = Cluster("couchbase://localhost", cluster_opts)

        query = f"select id, name, description, strength, beans, flavours, intensity, suffix, price FROM products where id='{product_id}'"
        rows = cluster.query(query)
        results = {}
        for row in rows:
            results = {
                "id": row["id"],
                "name": row["name"],
                "description": row["description"],
                "strength": row["strength"],
                "beans": row["beans"],
                "flavours": row["flavours"],
                "intensity": row["intensity"],
                "suffix": row["suffix"],
                "price": row["price"],
            }
        return results
    except (CouchbaseException, AuthenticationException):
        return None


def check_flag(flag):
    format_check = re.search("^CBN[{][a-z0-9_]+[}]$", flag)
    if not format_check:
        return {
            "error": "Invalid flag format! The flag should be in the format: CBN{<flag>}"
        }
    for cflag in flags_data:
        if cflag["value"] == flag:
            if cflag["solved"]:
                return {"error": "Flag Already Solved! Try Another One!"}
            cflag["solved"] = True
            return {"success": f"{cflag['name']} Solved!"}
    return {"error": "Incorrect flag provided!"}


def update_status(status):
    try:
        auth = PasswordAuthenticator(
            os.getenv("DB_USERNAME_TWO"), os.getenv("DB_PASSWORD_TWO")
        )
        cluster_opts = ClusterOptions(auth)
        cluster = Cluster("couchbase://localhost", cluster_opts)

        query = (
            f"UPDATE status as s SET s.status = '{status}' where component = 'service'"
        )
        rows = cluster.query(query)
        for row in rows:
            continue
    except (CouchbaseException, AuthenticationException):
        return None


def get_current_status(action):
    if not action:
        action = "refresh"
    try:
        auth = PasswordAuthenticator(
            os.getenv("DB_USERNAME_TWO"), os.getenv("DB_PASSWORD_TWO")
        )
        cluster_opts = ClusterOptions(auth)
        cluster = Cluster("couchbase://localhost", cluster_opts)

        query = f"select s.status FROM status as s where action='{action}'"
        rows = cluster.query(query)
        results = {}
        for row in rows:
            if not row.get("status"):
                continue
            results = {"status": row["status"]}
        return results
    except (CouchbaseException, AuthenticationException):
        return None
