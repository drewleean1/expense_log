from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from expense.auth import login_required
from expense.db import get_db

from datetime import datetime, date
import calendar 

import logging

bp = Blueprint('record', __name__)

current_month = datetime.now().month
current_year = datetime.now().year

print(current_month)

beginning = date(current_year, current_month, 1)
end = date(current_year, current_month, calendar.monthrange(current_year, current_month)[1])

@bp.route('/')
def personal(): 
    db = get_db()

    print(beginning, end)

    if g.user: 
        products = db.execute(
            'SELECT *'
            ' FROM expense'
            ' WHERE user_id = ? AND buy_date >= ? AND buy_date <= ?'
            ' ORDER BY buy_date DESC',
            (g.user['id'], beginning, end,)
        ).fetchall()        

        return render_template('record/personal.html', products = products, month=calendar.month_name[current_month], year=current_year)
    
    else: 
        return render_template('record/personal.html')

@bp.route('/add', methods=('GET', 'POST'))
@login_required
def add(): 
    if request.method == "POST": 
        buy_date = request.form['buy_date']
        item = request.form['item']
        amount = request.form['amount']
        category = request.form['category']
        error = None

        if not item: 
            error = 'Item is required'

        if not amount: 
            error = 'Amount is required'

        if error is not None: 
            flash(error)

        else: 
            db = get_db()
            db.execute(
                'INSERT INTO expense (buy_date, item, amount, category, user_id)'
                ' VALUES (?, ?, ?, ?, ?)',
                (buy_date, item, amount, category, g.user['id'])
            )
            db.commit()
            return redirect(url_for('record.personal'))

    return render_template('record/add.html')

def get_expense(id, check_user=True): 
    single_expense = get_db().execute(
        'SELECT e_id, buy_date, item, amount, category, user_id, username'
        ' FROM expense e JOIN user u ON e.user_id = u.id'
        ' WHERE e.e_id = ?', 
        (id,)
    ).fetchone()

    if single_expense is None: 
        abort(404, f"Expense id {id} doesn't exist.")

    if check_user and single_expense['user_id'] != g.user['id']: 
        abort(403)

    return single_expense

@bp.route('/<int:id>/edit', methods=('GET', 'POST'))
@login_required
def edit(id): 
    single_expense = get_expense(id)

    if request.method == 'POST': 
        buy_date = request.form['buy_date']
        item = request.form['item']
        amount = request.form['amount']
        category = request.form['category']

        db = get_db()
        db.execute(
            'UPDATE expense SET buy_date = ?, item = ?, amount = ?, category = ?'
            ' WHERE e_id = ?',
            (buy_date, item, amount, category, id)
        )
        db.commit()
        return redirect(url_for('record.personal'))
    
    return render_template('record/edit.html', single_expense = single_expense)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_expense(id)
    db = get_db()
    db.execute('DELETE FROM expense WHERE e_id = ?', (id,))
    db.commit()
    return redirect(url_for('record.personal'))