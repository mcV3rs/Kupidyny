import io
import os
from zipfile import ZipFile

import pdfkit
from flask import (render_template, redirect, url_for, send_file, current_app, after_this_request)
from flask_login import login_required, current_user

import project.functions as f
from . import photo_blueprint
from ..models import File, Wedding, UserWedding


# TODO Dodać obsługę zdjęcia hero dla albumu
def prepare_html(wedding_id):
    wedding = Wedding.query.filter_by(id=wedding_id).first()

    # Get the HTML output
    out = render_template('book_template_html.html',
                          hero_img="hero.jpeg",
                          names=f"{wedding.get_wife()} & {wedding.get_husband()}",
                          date=wedding.get_date(),
                          city=wedding.get_city(),
                          files=f.get_photos_with_names(wedding.get_id()))

    save_path = os.path.join(current_app.config['UPLOAD_PATH'],
                             f"{wedding.get_wife()}_{wedding.get_husband()}_fotobook.html")

    with open(save_path, "w", encoding="utf-8") as file:
        file.write(out)

    return save_path


def prepare_pdf(wedding_id):
    wedding = Wedding.query.filter_by(id=wedding_id).first()

    # Get the HTML output
    out = render_template('book_template_pdf.html',
                          hero_img="hero.jpeg",
                          names=f"{wedding.get_wife()} & {wedding.get_husband()}",
                          date=wedding.get_date(),
                          city=wedding.get_city(),
                          files=f.get_photos_with_names(wedding.get_id()))

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
    """
    Strona umożliwiająca edycję konkretnego zdjęcia do użytku przez parę weselną
    """
    # TODO zmiana tej funkcji pod edycję przez gości
    return render_template('photo.html',
                           files=f.get_photos())


@photo_blueprint.route('/book-edit')
@login_required
def book_edit():
    """
    Strona umożliwiająca wybór zdjęć do umieszczenia w albumie
    """
    user_wedding = UserWedding.query.filter_by(user_id=current_user.id).first()

    if user_wedding is None:
        # TODO dodanie komunikatu o braku wesela dla aktualnego konta
        return redirect(url_for('recipes.index'))
    else:
        return render_template('photo_book.html',
                               files=f.get_photos(user_wedding.wedding.get_id()),
                               wedding_id=user_wedding.wedding.id)


@photo_blueprint.route('/book/<int:wedding_id>')
@login_required
def book_preview(wedding_id):
    """
    Strona wyświetlająca aktualny wygląd albumu dla pary weselnej
    """
    wedding = Wedding.query.filter_by(id=wedding_id).first()

    if wedding is not None:
        return render_template('book_template.html',
                               hero_img="hero.jpeg",
                               names=f"{wedding.get_wife()} & {wedding.get_husband()}",
                               date=wedding.get_date(),
                               city=wedding.get_city(),
                               files=f.get_photos_with_names(wedding.get_id()),
                               show_download_bar=False)
    else:
        # TODO dodanie komunikatu o braku wesela dla aktualnego konta
        return redirect(url_for('recipes.index'))


@photo_blueprint.route('/download/html/<int:wedding_id>')
def download_html_book(wedding_id):
    """
    Strona do pobierania pliku html
    :param wedding_id:
    :return:
    """

    @after_this_request
    def remove_file(response):
        try:
            os.remove(file_path)
        except Exception as error:
            current_app.logger.error("Error removing or closing downloaded file handle", error)
        return response

    wedding = Wedding.query.filter_by(id=wedding_id).first()

    if wedding is not None:
        file_path = prepare_html(wedding_id)

        return_data = io.BytesIO()
        with open(file_path, 'rb') as fo:
            return_data.write(fo.read())
        return_data.seek(0)

        return send_file(
            return_data,
            mimetype='text/html',
            download_name=f"{wedding.get_wife()}_{wedding.get_husband()}_fotobook.html",
            as_attachment=True
        )
    else:
        return redirect(url_for('recipes.index'))


@photo_blueprint.route('/download/pdf/<int:wedding_id>')
def download_pdf_book(wedding_id):
    """
    Strona do pobierania pliku pdf
    :param wedding_id:
    :return:
    """

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
    """
    Strona do pobierania pliku zip
    :param wedding_id:
    :return:
    """

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
            "pdf": prepare_pdf(wedding_id),
            "html": prepare_html(wedding_id),
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


@photo_blueprint.route('/qr')
def qr_guest():
    """
    Strona zawierająca QR kody dla gości
    """
    user_wedding = UserWedding.query.filter_by(user_id=current_user.id).first()

    if user_wedding is None:
        # TODO dodanie komunikatu o braku wesela dla aktualnego konta
        return redirect(url_for('recipes.index'))
    else:
        return render_template('qr_hub.html',
                               files=f.get_photos(user_wedding.wedding.get_id()),
                               wedding_id=user_wedding.wedding.id,
                               wedding_uuid=user_wedding.wedding.get_uuid())


"""
Obsługa gości - wyświetlanie albumu oraz dodawanie zdjęć
"""


@photo_blueprint.route('/wedding-book/<uuid:wedding_uuid>')
def wedding_book_guest(wedding_uuid):
    wedding = Wedding.query.filter_by(uuid=wedding_uuid).first()

    if wedding is not None:
        return render_template('book_template.html',
                               hero_img="hero.jpeg",
                               names=f"{wedding.get_wife()} & {wedding.get_husband()}",
                               date=wedding.get_date(),
                               city=wedding.get_city(),
                               files=f.get_photos_with_names(wedding.get_id()),
                               show_download_bar=True,
                               wedding_id=wedding.get_id())
    else:
        # TODO dodanie komunikatu o niepoprawnym/uszkodzonym linku
        return redirect(url_for('recipes.index'))


@photo_blueprint.route('/add-picture/<uuid:wedding_uuid>')
def add_picture_guest(wedding_uuid):
    # TODO dodanie edycji zdjęć przez gościa
    return redirect(url_for('recipes.index'))
