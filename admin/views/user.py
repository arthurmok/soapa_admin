# --*-- coding:utf-8 --*--
import StringIO
from flask_login import login_user, logout_user, current_user, login_required
from flask import redirect, render_template, request, flash, session, url_for, jsonify, make_response
from admin.utils.validate_code import create_validate_code
from admin.models.user import *
from admin import admin_app, db, mem_cache
from ext import app


@admin_app.route('/')
@admin_app.route('/index/')
def index():
    return redirect(url_for('assets'))


@admin_app.route('/users')
@admin_app.route('/users/')
# @login_required
def user_list():
    print 222222, request.cookies
    users = db.session.query(User)
    groups = db.session.query(Group)
    selectors = db.session.query(Selector)
    roles = db.session.query(Role)
    return render_template('admin_user.html', users=users, groups=groups,
                           selectors=selectors, roles=roles, level_one='admin', level_two='users')


@admin_app.route('/api/login', methods=['POST'])
def api_login():

    try:
        # auth_code = session.get('yzk')
        # if not auth_code:
        #     auth_code = request.cookies.get('auth_code')
        # if not auth_code:
        #     return jsonify({"status": False, "desc": "请刷新验证码"})
        auth_dict = request.get_json()

        if auth_dict:
            username = auth_dict.get('username')
            if not username:
                username = auth_dict.get('userName')
            password = auth_dict.get('password')
            # code = auth_dict.get('auth_code')
        else:
            username = request.values.get('username')
            password = request.values.get('password')
            # code = request.values.get('auth_code')
        # if auth_code.upper() != code.upper():
        #     return jsonify({"status": False, "desc": "验证码错误"})
        user = db.session.query(User).filter(User.name == username, User.status==True).first()
        if not user:
            return jsonify({"status": False, "desc": "用户名或密码错误"})
        verify_res = user.check_password_hash(password)
        if not verify_res:
            return jsonify({"status": False, "desc": "用户名或密码错误"})
        session['username'] = user.name
        # session['company'] = user.company
        # role = db.session.query(Role).filter(Role.id == user.rid).first()
        # session['role'] = role.name
        selectors = get_selectors(user)
        mem_cache.set(user.name, selectors, timeout=30*60)
        # print 111111, mem_cache.get(user.name)
        # session['selectors'] = selectors
        login_user(user)
        response = make_response(jsonify({"status": True, "privileges": selectors}))
        response.headers["Set-Cookie"] = "username=%s;Max-Age=1800; Path=/;Domain=%s" % (user.name, request.host)
        # response.set_cookie('domain', 'localhost', max_age=1800)
        # response.set_cookie('path', '/', max_age=1800)
        # response.set_cookie('username', user.name, max_age=1800)

    except Exception, e:
        print e
        logger.error(e)
        db.session.rollback()
        return jsonify({"status": False, "desc": "用户登陆失败"})
    # response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response


@admin_app.route('/login', methods=['GET', 'POST'])
def do_login():
    next_url = request.values.get('next', '/')
    remember_me = request.values.get('remember_me', True)

    if request.method == 'POST':
        auth_dict = request.get_json()
        if auth_dict:
            username = auth_dict.get('username')
            password = auth_dict.get('password')
            code = auth_dict.get('auth_code')
        else:
            username = request.values.get('username')
            password = request.values.get('password')
            code = request.values.get('auth_code')
        if session.get('yzk').upper() != code.upper():
            flash('验证码错误'.decode('utf-8'), 'error')
            return render_template('login.html')
        user = db.session.query(User).filter(User.name == username, User.status==True).first()
        if not user:
            flash('用户名或密码错误'.decode('utf-8'), 'error')
            return render_template('login.html')
        verify_res = user.check_password_hash(password)
        if not verify_res:
            flash('用户名或密码错误'.decode('utf-8'), 'error')

            return render_template('login.html')
        session['username'] = user.name
        # session['company'] = user.company
        # role = db.session.query(Role).filter(Role.id == user.rid).first()
        # session['role'] = role.name
        selectors = get_selectors(user)
        session['selectors'] = selectors
        login_user(user, remember_me)
        # response = make_response(redirect(next_url))
        # response.headers["Set-Cookie"] = "username=%s;Max-Age=1800; Path=/;Domain=localhost" % user.name
        return redirect(next_url)
        # return response
    else:
        if current_user.is_active:
            # response = make_response(redirect(next_url))
            # print current_user.name
            # response.headers["Set-Cookie"] = "username=%s;Max-Age=1800; Path=/;Domain=localhost" % current_user.name
            return redirect(next_url)
            # return response

        return render_template('login.html')


@admin_app.route('/logout')
@login_required
def do_logout():
    if current_user.is_active:
        logout_user()
        for key in ['username', 'role', 'selectors']:
            session.pop(key, None)
    return redirect(url_for('admin.do_login'))


@admin_app.errorhandler(403)
def error403(error):
    return render_template('error-404.html'), 403


@admin_app.errorhandler(404)
def error404(error):
    return render_template('error-404.html'), 404


@admin_app.errorhandler(413)
def error413(error):
    return render_template('error-413.html'), 413


def get_selectors(user):
    groups = db.session.query(Group).filter(Group.id.in_(user.group_ids.split(',')))
    selectors = []
    for group in groups:
        if not group.selectors:
            continue
        elif group.selectors == '*':
            _selectors = db.session.query(Selector.name)
        else:
            _selectors = db.session.query(Selector.name).filter(Selector.id.in_(set(group.selectors.split(','))))
        selectors += [_selector.name for _selector in _selectors]
    return selectors


@admin_app.route('/users/code')
# @ login_required
def show_code():
    # 把strs发给前端,或者在后台使用session保存

    code_img, str_code = create_validate_code()
    session['yzk'] = str_code
    buf = StringIO.StringIO()
    code_img.save(buf, 'JPEG', quality=70)
    buf_str = buf.getvalue()
    response = app.make_response(buf_str)
    response.headers['Content-Type'] = 'image/jpeg'
    return response