from flask import jsonify
from flask_login import login_required

from app.libs.auth import admin_only
from app.libs.error_code import CreateSuccess, DeleteSuccess, NotFound, Success
from app.libs.red_print import RedPrint
from app.models.oj import OJ
from app.models.problem_set import ProblemSet
from app.validators.problem_set import (CreateContestForm,
                                        CreateProblemSetForm,
                                        ModifyProblemSetForm)
from app.models.problem_set.category import Category

api = RedPrint('monitor')


@api.route("/valid_oj", methods=['GET'])
def get_oj_list():
    oj_list = OJ.search(status=1, page_size=-1)['data']
    return jsonify({
        'code': 0,
        'data': oj_list
    })


@api.route("/valid_contest_oj", methods=['GET'])
def get_contest_oj_list():
    oj_list = OJ.search(status=1, contest_valid=1, page_size=-1)['data']
    return jsonify({
        'code': 0,
        'data': oj_list
    })


@api.route("/summary", methods=['GET'])
def get_summary():
    collection_list = Category.search(page_size=-1, order={'id': 'desc'})['data']
    return jsonify({
        'code': 0,
        'data': collection_list
    })


@api.route('/Category/<int:id_>', methods=['GET'])
def get_collection(id_):
    problem_set_list = ProblemSet.search(category_id=id_, page_size=-1, order={'id': 'desc'})['data']
    return jsonify({
        'code': 0,
        'data': problem_set_list
    })


@api.route("/<int:id_>", methods=['GET'])
def get_problem_set_api(id_):
    problem_set = ProblemSet.get_by_id(id_)
    if problem_set is None:
        raise NotFound('Problem set not found')

    fields = problem_set.fields.copy()
    fields.extend(['problem_list', 'detail'])
    problem_set.fields = fields
    return jsonify({
        "code": 0,
        "data": problem_set
    })


@api.route("/add_problem_set", methods=['POST'])
@login_required
@admin_only
def create_problem_set_api():
    form = CreateProblemSetForm().validate_for_api().data_
    ProblemSet.create(**form)
    raise CreateSuccess('Problem set has been created')


@api.route("/add_contest", methods=['POST'])
@login_required
@admin_only
def create_contest_api():
    form = CreateContestForm().validate_for_api().data_
    ProblemSet.create(**form)
    # todo: create task
    raise CreateSuccess('Contest will be available soon')


@api.route("/<int:id_>", methods=['PUT'])
@login_required
@admin_only
def modify_problem_set_api(id_):
    problem_set = ProblemSet.get_by_id(id_)
    if problem_set is None:
        raise NotFound('Problem set not found')

    form = ModifyProblemSetForm().validate_for_api().data_
    problem_set.modify(**form)
    raise Success('Problem set has been modified')


@api.route("/<int:id_>", methods=['DELETE'])
@login_required
@admin_only
def delete_problem_set_api(id_):
    problem_set = ProblemSet.get_by_id(id_)
    if problem_set is None:
        raise NotFound('Problem set not found')

    problem_set.delete()
    raise DeleteSuccess('Problem set has been deleted')
