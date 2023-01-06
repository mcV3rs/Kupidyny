import io
import os
from zipfile import ZipFile

import pdfkit
from flask import (render_template, Response, redirect, url_for, send_file, current_app, after_this_request)
from flask_login import login_required

from . import photo_blueprint
from ..models import File, Wedding


# TODO wyczyścić metody pobierania zdjęć z BD
# TODO Dodać obsługę zdjęcia hero dla albumu
def prepare_html(wedding_id):
    wedding = Wedding.query.filter_by(id=wedding_id).first()

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


def prepare_pdf(wedding_id):
    wedding = Wedding.query.filter_by(id=wedding_id).first()

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
    save_path = os.path.join(current_app.config['UPLOAD_PATH'],
                             f"{wedding.get_wife()}_{wedding.get_husband()}_fotobook.pdf")
    pdfkit.from_string(out, save_path, options=options)
    return save_path


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


@photo_blueprint.route('/download/html/<int:wedding_id>')
def download_html_book(wedding_id):
    wedding = Wedding.query.filter_by(id=wedding_id).first()

    if wedding is not None:
        return send_file(
            prepare_html(wedding_id),
            mimetype='text/html',
            download_name=f"{wedding.get_wife()}_{wedding.get_husband()}_fotobook.html",
            as_attachment=True
        )
    else:
        return redirect(url_for('recipes.index'))


@photo_blueprint.route('/download/pdf/<int:wedding_id>')
def download_pdf_book(wedding_id):
    @after_this_request
    def remove_file(response):
        try:
            os.remove(file_path)
        except Exception as error:
            current_app.logger.error("Error removing or closing downloaded file handle", error)
        return response

    wedding = Wedding.query.filter_by(id=wedding_id).first()

    if wedding is not None:
        file_path = prepare_pdf(wedding_id)

        return_data = io.BytesIO()
        with open(file_path, 'rb') as fo:
            return_data.write(fo.read())
        return_data.seek(0)

        return send_file(
            return_data,
            mimetype='application/pdf',
            download_name=f"{wedding.get_wife()}_{wedding.get_husband()}_fotobook.pdf",
            as_attachment=True
        )
    else:
        return redirect(url_for('recipes.index'))


@photo_blueprint.route('/download/zip/<int:wedding_id>')
def download_zip_book(wedding_id):
    @after_this_request
    def remove_file(response):
        try:
            for key in paths:
                os.remove(paths[key])
        except Exception as error:
            current_app.logger.error("Error removing or closing downloaded file handle", error)
        return response

    wedding = Wedding.query.filter_by(id=wedding_id).first()

    if wedding is not None:
        paths = {
            "zip": os.path.join(current_app.config['UPLOAD_PATH'],
                                f"{wedding.get_wife()}_{wedding.get_husband()}_fotobook.zip"),
            "pdf": prepare_pdf(wedding_id)
        }

        with ZipFile(paths["zip"], 'w') as zip_file:
            for key in paths:
                if key != "zip":
                    zip_file.write(paths[key], arcname=f"{wedding.get_wife()}_{wedding.get_husband()}_fotobook.{key}")

        return_data = io.BytesIO()
        with open(paths["zip"], 'rb') as fo:
            return_data.write(fo.read())
        return_data.seek(0)

        return send_file(
            return_data,
            mimetype='application/pdf',
            download_name=f"{wedding.get_wife()}_{wedding.get_husband()}_fotobook.zip",
            as_attachment=True
        )
    else:
        return redirect(url_for('recipes.index'))


@photo_blueprint.route('/book/<int:wedding_id>')
def html_template(wedding_id):
    wedding = Wedding.query.filter_by(id=wedding_id).first()

    if wedding is not None:
        return prepare_html(wedding_id)
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
