"""Routes for the course resource.
"""

from run import app
from flask import request,json
from http import HTTPStatus
import data
import datetime


@app.route("/course/<int:id>", methods=['GET'])
def get_course(id):
    """Get a course by id.

    :param int id: The record id.
    :return: A single course (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------   
    1. Bonus points for not using a linear scan on your data structure.
    """
    # YOUR CODE HERE
    course = list(filter(lambda x: x["id"] == id, data.load_data()))
    if len(course)==1:
        response = app.response_class(
            response=json.dumps(course[0]),
            status=200,
            mimetype='application/json'
        )
    else:
        msg = {"error":f"Course {id} does not exist"}
        response = app.response_class(
            response=json.dumps(msg),
            status=404,
            mimetype='application/json'
        )
    return response


@app.route("/course", methods=['GET'])
def get_courses():
    """Get a page of courses, optionally filtered by title words (a list of
    words separated by commas".

    Query parameters: page-number, page-size, title-words
    If not present, we use defaults of page-number=1, page-size=10

    :return: A page of courses (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    ------------------------------------------------------------------------- 
    1. Bonus points for not using a linear scan, on your data structure, if
       title-words is supplied
    2. Bonus points for returning resulted sorted by the number of words which
       matched, if title-words is supplied.
    3. Bonus points for including performance data on the API, in terms of
       requests/second.
    """
    # YOUR CODE HERE
    title_words = request.args.get('title-words')
    if title_words:
        # courses = list(filter(lambda x: any(title in x['title'] for title in title_words.split(',')) , data.load_data()))
        courses = []
        for course in data.load_data():
            if any(title.lower() in course["title"].lower() for title in title_words.split(',')):
                courses.append(course)
    else:
        courses = data.load_data()


    page_size = int(1 if not request.args.get('page-size') else request.args.get('page-size'))
    # courses = data.load_data()
    record_count = len(courses)
    page_count = int((record_count/page_size))
    page_number = int(1 if not request.args.get('page-number') else request.args.get('page-number'))



    metadata = {
        "page_count": page_count,
        "page_number": page_number,
        "page_size": page_size,
        "record_count": record_count
    }

    if len(courses) >= 1:
        response = app.response_class(
            response=json.dumps({
                "data":courses[(page_number-1)*page_size:page_size*page_number],
                "metadata":metadata
                }
            ),
            status=200,
            mimetype='application/json'
        )
    else:
        response = app.response_class(
            response=json.dumps({
                "data": [],
                "metadata": metadata
            }
            ),
            status=200,
            mimetype='application/json'
        )
    return response

def validate_put_data(post_data,request_data):

    if "id" in post_data and "date_updated" in post_data and "on_discount" in post_data \
        and "price" in post_data and "title" in post_data:
        if "id" in request_data:
            if request_data["id"]==post_data["id"]:
                return True
            else:
                return False

        return True

    else:
        return False

def validate_post_data(post_data):

    if "id" in post_data and "date_created" in post_data and "date_updated" in post_data and "on_discount" in post_data \
        and "price" in post_data and "title" in post_data:
        return True
    else:
        return False



@app.route("/course", methods=['POST'])
def create_course():
    """Create a course.
    :return: The course object (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    1. Bonus points for validating the POST body fields
    """
    # YOUR CODE HERE
    request_data = request.get_json()
    description = None if len(request_data.get('description',None)) >=255\
                  else request_data.get('description',None)
    discount_price = request_data.get('discount_price',None)
    title = request_data.get('title',None) if len(request_data.get('title',None)) >=5 and len(request_data.get('title',None)) <=100\
                  else None
    price = request_data.get('price',None)
    image_path = None if len(request_data.get('image_path',None)) >=100\
                  else request_data.get('image_path',None)
    on_discount = request_data.get("on_discount",None)

    id = max(data.load_data(), key=lambda x:x['id'])
    date_created = str(datetime.datetime.now())
    date_updated = date_created

    payload = {
        "description": description,
        "discount_price": discount_price,
        "title": title,
        "price": price,
        "image_path": image_path,
        "on_discount": on_discount,
        "date_created": date_created,
        "date_updated": date_updated,
        "id": id['id']+1
    }
    courses = data.load_data()

    if validate_post_data(payload):

        if payload["description"] != None and payload["title"] !=None and payload["image_path"] !=None:

            courses.append(payload)
            with open("./json/course.json", "w") as outfile:
                json.dump(courses, outfile)

            response = app.response_class(
                response=json.dumps({
                    "data": payload
                }
                ),
                status=200,
                mimetype='application/json')
        else:
            msg = {"message": "The id does match the payload"}
            response = app.response_class(
                response=json.dumps(msg),
                status=400,
                mimetype='application/json'
            )
    else:
        msg = {"message": "The id does match the payload"}
        response = app.response_class(
            response=json.dumps(msg),
            status=400,
            mimetype='application/json'
        )
    return response



@app.route("/course/<int:id>", methods=['PUT'])
def update_course(id):
    """Update a a course.
    :param int id: The record id.
    :return: The updated course object (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    1. Bonus points for validating the PUT body fields, including checking
       against the id in the URL

    """

    # YOUR CODE HERE
    request_data = request.get_json()
    description = request_data.get('description', None)
    discount_price = request_data.get('discount_price', None)
    title = request_data.get('title', None)
    price = request_data.get('price', None)
    image_path = request_data.get('image_path', None)
    on_discount = request_data.get("on_discount", None)

    date_created = request_data.get("date_created", None)
    date_updated = str(datetime.datetime.now())


    payload = {
        "description": description,
        "discount_price": discount_price,
        "title": title,
        "price": price,
        "image_path": image_path,
        "on_discount": on_discount,
        "date_updated": date_updated,
        "id": id
    }

    if validate_put_data(payload,request_data):
        courses = data.load_data()
        for item in courses:
            if item["id"]==id:
                item["description"]: description
                item["discount_price"]: discount_price
                item["title"]: title
                item["price"]: price
                item["image_path"]: image_path
                item["on_discount"]: on_discount
                item["date_updated"]: date_updated

        with open("./json/course.json", "w") as outfile:
            json.dump(courses, outfile)

        response = app.response_class(
            response=json.dumps({
                "data": payload
            }
            ),
            status=200,
            mimetype='application/json')
    else:
        msg = {"message": "The id does match the payload"}
        response = app.response_class(
            response=json.dumps(msg),
            status=400,
            mimetype='application/json'
        )
    return response



@app.route("/course/<int:id>", methods=['DELETE'])
def delete_course(id):
    """Delete a course
    :return: A confirmation message (see the challenge notes for examples)
    """
    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    None
    """
    # YOUR CODE HERE

    courses = list(filter(lambda x: x["id"] == id, data.load_data()))

    if len(courses) >= 1:
        courses = list(filter(lambda x: x["id"] != id, data.load_data()))
        with open("./json/course.json", "w") as outfile:
            json.dump(courses, outfile)
        msg = "The specified course was deleted"
        response = app.response_class(
            response=json.dumps(msg),
            status=200,
            mimetype='application/json'
        )
    else:
        msg = {"error": f"Course {id} does not exist"}
        response = app.response_class(
            response=json.dumps(msg),
            status=404,
            mimetype='application/json'
        )
    return response
