import pdfkit
from flask import (render_template, request, Response)
from flask_login import login_required

from . import photo_blueprint
from ..models import File


# Routes
@photo_blueprint.route('/photo-edit')
@login_required
def photo_edit():
    # Uploaded files, with record id DB
    files = File.query.all()
    return_paths = []

    for file in files:
        return_paths.append(file.get_name())

    return render_template('photo.html',
                           files=return_paths)


@photo_blueprint.route('/photo-book')
@login_required
def photo_book():
    # Uploaded files, with record id DB
    files = File.query.all()
    return_paths = []

    for file in files:
        return_paths.append(file.get_name())

    return render_template('photo_book.html',
                           files=return_paths)


@photo_blueprint.route('/book')
def book_template():
    wedding_id = request.args.get('wedding_id', default=0, type=int)

    if wedding_id == 0:
        return render_template('recipes/index.html')

    if wedding_id == 1:
        # Uploaded files, with record id DB
        files = File.query.all()
        return_paths = []

        for file in files:
            return_paths.append(file.get_name())

        # Get the HTML output
        return render_template('book_template.html',
                               hero_img="hero.jpeg",
                               names="Justyna & Karol",
                               date="15.01.2023",
                               city="Gliwice",
                               files=return_paths)


@photo_blueprint.route('/download')
def download_book():
    # Uploaded files, with record id DB
    files = File.query.all()
    return_paths = []

    for file in files:
        return_paths.append(file.get_name())

    print(return_paths)

    # Get the HTML output
    out = render_template('book_template.html',
                          hero_img="hero.jpeg",
                          names="Justyna & Karol",
                          date="15.01.2023",
                          city="Gliwice",
                          files=return_paths)

    # PDF options
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
