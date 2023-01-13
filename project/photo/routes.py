import base64
import csv
import datetime
import io
import json
import os
import re
import shutil
import time
from zipfile import ZipFile

import pdfkit
from flask import (render_template, redirect, url_for, send_file, current_app, after_this_request, request, flash)
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

import project.functions as f
from . import photo_blueprint
from .. import db
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


def prepare_cupid(wedding_id):
    # Przygotowanie ścieżek do plików
    wedding = Wedding.query.filter_by(id=wedding_id).first()
    paths = {
        "zip": os.path.join(current_app.config['UPLOAD_PATH'],
                            f"{wedding.get_wife()}_{wedding.get_husband()}_fotobook.cupid"),
        "wedding": os.path.join(current_app.config['UPLOAD_PATH'],
                                f"{wedding.get_wife()}_{wedding.get_husband()}_wedding.csv"),
        "files": os.path.join(current_app.config['UPLOAD_PATH'],
                              f"{wedding.get_wife()}_{wedding.get_husband()}_files.csv"),
        "files_folder": os.path.join(current_app.config['UPLOAD_PATH'],
                                     f"{wedding.get_wife()}_{wedding.get_husband()}_files"),
    }

    # Zapisywanie danych dotyczących wesela
    with open(paths["wedding"], 'w', newline='', encoding="utf-8") as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        columns, row = wedding.to_csv()

        csvwriter.writerow(columns)
        csvwriter.writerow(row)

    # Zapisywanie danych dotyczących plików gości
    files = File.query.filter_by(wedding_id=wedding.get_id())
    with open(paths["files"], 'w', newline='', encoding="utf-8") as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        columns = files[0].get_columns()

        csvwriter.writerow(columns)
        for file in files:
            csvwriter.writerow(file.get_csv_row())

    with ZipFile(paths["zip"], 'w') as zip_file:
        for key in paths:
            if key != "zip" and key != "files_folder":
                zip_file.write(paths[key], arcname=f"{key}.csv")
                os.remove(paths[key])
            elif key == "files_folder":
                for file in files:
                    zip_file.write(os.path.join(current_app.config['UPLOAD_PATH'], file.get_path()),
                                   arcname=f"files/{file.get_path()}")

    return paths["zip"]


'''
Obsługa zalogowanego użytkownika
'''

@photo_blueprint.route('/book-edit')
@login_required
def book_edit():
    """
    Strona umożliwiająca wybór zdjęć do umieszczenia w albumie
    """
    user_wedding = UserWedding.query.filter_by(user_id=current_user.id).first()

    if user_wedding is None:
        flash('Dla aktualnego konta nie ma przypisanego wesela, proszę skontaktować się z serwisem')
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
        flash('Niepoprawny lub uszkodzony link')
        return redirect(url_for('recipes.index'))


@photo_blueprint.route('/import-book', methods=['POST'])
@login_required
def import_book():
    try:
        if request.method == "POST":
            # Odkodowanie pliku
            data_cupid = request.files["cupid_file"]
            filename = "import_cupid.zip"

            # Zapisanie pliku
            path = os.path.join(current_app.config['UPLOAD_PATH'], "import_cupid")
            os.mkdir(path)
            path1 = os.path.join(path, filename)
            data_cupid.save(path1)

            # Wypakowanie archiwum
            with ZipFile(path1, 'r') as zip_file:
                zip_file.extractall(path)
            os.remove(path1)

            # Import danych dotyczących wesela
            wedding = UserWedding.query.filter_by(user_id=current_user.get_id()).first().wedding
            with open(os.path.join(path, "wedding.csv"), 'r') as file:
                dict_reader = csv.DictReader(file)
                list_of_dict = list(dict_reader)

                wedding.wife = list_of_dict[0]["wife"]
                wedding.husband = list_of_dict[0]["husband"]
                wedding.city = list_of_dict[0]["city"]
                wedding.date = datetime.datetime.strptime(list_of_dict[0]["date"], "%Y-%m-%d").date()

            # Import danych dotyczących zdjęć
            with open(os.path.join(path, "files.csv"), 'r') as file:
                dict_reader = csv.DictReader(file)
                list_of_dict = list(dict_reader)

                for row in list_of_dict:
                    new_file = File(path=row["path"], wedding_id=wedding.get_id(), guest_name=row["guest_name"])
                    db.session.add(new_file)

            # Posprzątanie
            files = os.listdir(os.path.join(path, "files"))
            for file in files:
                shutil.copy2(os.path.join(os.path.join(path, "files"), file),
                             os.path.join(current_app.config['UPLOAD_PATH'], file))

            shutil.rmtree(path)
            db.session.commit()

            return redirect(url_for('users.profile'))
    except:
        flash('Podczas operacji wystąpił błąd, proszę skontaktować się z serwisem')
        return redirect(url_for('recipes.index'))


"""
Obsługa pobierania - pobieranie książki w formatach
"""


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
        flash('Niepoprawny lub uszkodzony link')
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
        flash('Niepoprawny lub uszkodzony link')
        return redirect(url_for('recipes.index'))


@photo_blueprint.route('/download/cupid/<int:wedding_id>')
def download_cupid_book(wedding_id):
    """
    Strona do pobierania pliku cupid
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
        file_path = prepare_cupid(wedding_id)

        return_data = io.BytesIO()
        with open(file_path, 'rb') as fo:
            return_data.write(fo.read())
        return_data.seek(0)

        return send_file(
            return_data,
            mimetype='application/cupid',
            download_name=f"{wedding.get_wife()}_{wedding.get_husband()}_fotobook.cupid",
            as_attachment=True
        )
    else:
        flash('Niepoprawny lub uszkodzony link')
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
            "cupid": prepare_cupid(wedding_id)
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
        flash('Niepoprawny lub uszkodzony link')
        return redirect(url_for('recipes.index'))


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
        flash('Niepoprawny lub uszkodzony link')
        return redirect(url_for('recipes.index'))


@photo_blueprint.route('/add-picture/<uuid:wedding_uuid>')
def add_picture_guest(wedding_uuid):
    wedding = Wedding.query.filter_by(uuid=wedding_uuid).first()

    if wedding is not None:
        return render_template('add_picture.html',
                               wedding=wedding,
                               names=f"{wedding.get_wife()} & {wedding.get_husband()}",
                               date=wedding.get_date(),
                               city=wedding.get_city(),
                               wedding_uuid=wedding.get_uuid())
    else:
        flash('Niepoprawny lub uszkodzony link')
        return redirect(url_for('recipes.index'))


@photo_blueprint.route('/edit-picture/<uuid:wedding_uuid>', methods=['POST'])
def edit_picture_guest(wedding_uuid):
    wedding = Wedding.query.filter_by(uuid=wedding_uuid).first()

    if wedding is not None:
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)

        if filename != '':
            file_ext = (os.path.splitext(filename)[1]).lower()

            if file_ext not in current_app.config['UPLOAD_EXTENSIONS']:
                flash('Nieudane wgranie pliku, możliwe, że użyte rozszerzenie nie jest wspierane przez serwis')
                return redirect(url_for('recipes.index'))

            path = os.path.join(current_app.config['UPLOAD_PATH'], filename)
            uploaded_file.save(path)

            return render_template('edit_picture.html',
                                   path=path,
                                   wedding_id=wedding.get_id(),
                                   img=filename,
                                   wedding=wedding)
    else:
        flash('Niepoprawny lub uszkodzony link')
        return redirect(url_for('recipes.index'))


@photo_blueprint.route('/save_picture/<uuid:wedding_uuid>', methods=['POST'])
def upload_file_guest(wedding_uuid):
    wedding = Wedding.query.filter_by(uuid=wedding_uuid).first()

    if wedding is not None:
        image_data = re.sub('^data:image/.+;base64,', '', request.form['image'])
        extension = request.form["extension"]
        guest_name = request.form["guest_name"]

        uploaded_file = base64.b64decode(image_data)
        filename = f"{int(time.time())}.{extension}"

        if filename != '':
            file_ext = (os.path.splitext(filename)[1]).lower()

            if file_ext not in current_app.config['UPLOAD_EXTENSIONS']:
                return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

            path = os.path.join(current_app.config['UPLOAD_PATH'], filename)

            new_file = File(path=filename, wedding_id=wedding.get_id(), guest_name=guest_name)
            db.session.add(new_file)
            db.session.commit()

            with open(path, "wb") as fh:
                fh.write(uploaded_file)

            return json.dumps({
                'success': True,
                'message': 'Success'
            }), 201, {'ContentType': 'application/json'}
    else:
        return json.dumps({
            'success': False,
            'message': 'Wedding not found or link is broken'
        }), 400, {'ContentType': 'application/json'}