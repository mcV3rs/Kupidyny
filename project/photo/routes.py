import pdfkit
from flask import (render_template, Response, redirect, url_for)
from flask_login import login_required

from . import photo_blueprint
from ..models import File, Wedding


# Routes
@photo_blueprint.route('/photo-edit')
@login_required
def photo_edit():
    # Uploaded files, with record id DB
    files = File.query.all()
    return_paths = []

    for file in files:
        return_paths.append(file.get_path())

    return render_template('photo.html',
                           files=return_paths)


# TODO prawdopodobnie do usunięcia
@photo_blueprint.route('/photo-book')
@login_required
def photo_book():
    # Uploaded files, with record id DB
    files = File.query.all()
    return_paths = []

    for file in files:
        return_paths.append(file.get_path())

    return render_template('photo_book.html',
                           files=return_paths)


@photo_blueprint.route('/book/<int:wedding_id>')
def html_template(wedding_id):
    wedding = Wedding.query.filter_by(id=wedding_id).first()

    if wedding is not None:
        print(wedding.get_uuid())

        # Uploaded files, with record id DB
        files = File.query.filter_by(wedding_id=wedding.get_id())
        return_paths = {}

        for row in files:
            return_paths[row.get_guest_name()] = row.get_path()

        # Get the HTML output
        return render_template('book_template.html',
                               hero_img="hero.jpeg",
                               names=f"{wedding.get_wife()} & {wedding.get_husband()}",
                               date=wedding.get_date(),
                               city=wedding.get_city(),
                               files=return_paths)
    else:
        return redirect(url_for('recipes.index'))


@photo_blueprint.route('/pdf/<uuid:wedding_uuid>')
def pdf_book(wedding_uuid):
    wedding = Wedding.query.filter_by(uuid=wedding_uuid).first()

    if wedding is not None:
        # Uploaded files, with record id DB
        files = File.query.filter_by(wedding_id=wedding.get_id())
        return_paths = {}

        for row in files:
            return_paths[row.get_guest_name()] = row.get_path()

        # Get the HTML output
        out = render_template('book_template_pdf.html',
                              hero_img="hero.jpeg",
                              names=f"{wedding.get_wife()} & {wedding.get_husband()}",
                              date=wedding.get_date(),
                              city=wedding.get_city(),
                              files=return_paths)

        options = {
            "orientation": "landscape",
            "page-size": "A4",
            "margin-top": "1.0cm",
            "margin-right": "1.0cm",
            "margin-bottom": "1.0cm",
            "margin-left": "1.0cm",
            "encoding": "UTF-8",
            "enable-local-file-access": True,
        }

        # Build PDF from HTML
        pdf = pdfkit.from_string(out, options=options)

        # Download the PDF
        return Response(pdf, mimetype="application/pdf")
    else:
        return redirect(url_for('recipes.index'))
