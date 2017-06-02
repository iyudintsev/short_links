from flask import views, render_template, request, flash, redirect, url_for, abort
from application import service
from forms import GenerateShortUrlForm


def add_url_rules(app):
    app.add_url_rule('/', view_func=IndexView.as_view('index'))
    app.add_url_rule('/<hash_>', view_func=SendView.as_view('send'))


class IndexView(views.View):
    methods = ["GET", "POST"]

    def dispatch_request(self):
        form = GenerateShortUrlForm(request.form)
        if request.method == "POST":
            if form.validate_on_submit():
                service.create_request(url=form.url.data)
                return redirect(url_for('index'))
            else:
                flash('Invalid Url')
        data = map(lambda r: r.link, service.get_last_requests())
        return render_template('index.html', form=form, data=data)


class SendView(views.View):
    methods = ["GET", "POST"]

    def dispatch_request(self, hash_):
        link = service.get_link_by_hash(hash_)
        if not link:
            abort(404)

        return redirect(link.url)
