from flask import Flask, escape, request, render_template, session, redirect, make_response
from modles import item
from modles.user import User
from modles.video import Video
from common.database import Database
import time

app = Flask(__name__)
app.secret_key = "mada"


@app.before_first_request
def init_db():
    Database.initialize()


@app.route('/')
def hello():
    response = make_response(render_template('home.html'))
    response.set_cookie(key='framework', value='flask', expires=time.time()+6*60)
    return response

@app.route('/gg')
def cookieGet():

    response = make_response(render_template('home.html'))
    return response



@app.route('/login', methods=["GET", "POST"])
def login_method():
    if request.method == "POST":
        account = request.form['InputAccount']
        password = request.form['InputPassword']
        check = User.is_login_vaild(account, password)
        if check is True:
            session['account'] = account
            session['name'] = User.find_user_data(account).get('name')
            return redirect("/")
        else:
            message = "Your account or password is wrong !"
            return render_template("login.html", message)
    else:
        return render_template("login.html")


@app.route('/register', methods=["GET", "POST"])
def register_method():
    if request.method == "POST":
        name = request.form['InputName']
        account = request.form['InputAccount']
        password = request.form['InputPassword']
        User.register_user(name, account, password)
        result = User.register_user(name, account, password)
        if result is True:
            session['account'] = account
            session['name'] = User.find_user_data(account).get('name')
            return redirect("/")
        else:
            message = "Your account is already exist!"
            return render_template("register.html", message=message)
    else:
        return render_template("login.html")


@app.route('/logout')
def logout():
    session['account'] = not session['account']
    return redirect('/')


@app.route('/results')
def result_page():
    url = request.url
    page = request.args.get('sp')
    favorite_video = []
    user_video = Video.find_video(session['account'])
    for video in user_video:
        favorite_video.append(video['link'])

    if page is None:
        search = request.args.get('search')
        soup = item.find_search_context(search)
        all_item = item.every_video(soup)
        all_page = item.page_bar(soup)
        return render_template("result.html", result=search, all_item=all_item, all_page=all_page,
                               url=url, favorite_video=favorite_video)

    elif page is not None:
        page = request.args.get('sp')
        current_page = request.args.get('current_page')
        value = "search_query={}".format(search) + "&sp={}".format(page)
        soup = item.find_page_context(value)
        all_item = item.every_video(soup)
        all_page = item.page_bar(soup)
        return render_template("result_page.html", result=search, all_item=all_item, all_page=all_page,
                               current_page=current_page, int=int, url=url, favorite_video=favorite_video)
    else:
        return redirect('/')


@app.route('/favorite', methods=["GET", "POST"])
def favorite_video():
    if session['account']:
        if request.method == 'POST':
            url = request.form['url']
            title = request.form['title']
            link = request.form['link']
            img = request.form['img']
            account = session['account']
            Video(account, title, link, img).save_to_db()
            return redirect(url)
        else:
            account = session['account']
            user_video = Video.find_video(account)
            return render_template('favorite.html', user_video=user_video)
    else:
        return redirect('/login')


@app.route("/delete", methods=['POST'])
def delete_method():
    link = request.form['link']
    account = session['account']
    Video.delete_video(account, link)
    return redirect("/favorite")


@app.route('/download')
def download():
    value = request.args.get('value')
    download_type, url = value.split("&")
    if download_type == "MP3":
        item.download_mp3(url)
        return render_template("download.html")
    elif download_type == "MP4":
        item.download_mp4(url)
        return render_template("download.html")

