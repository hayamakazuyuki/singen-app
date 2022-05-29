from crypt import methods
from flask import Blueprint, render_template, request, flash, redirect, url_for

from ..extentions import db

from ..models import Contractor, Satiscare

from .forms import ContractorForm

contractor = Blueprint('contractor', __name__, url_prefix='/contractor')

@contractor.route('/')
def index():

    q = request.args.get('q')

    if q:

        # if q.isdigit():
    
        #     contractor = Contractor.query.get(q)

        #     if contractor:
        #         return redirect(url_for('contractor.profile', id=q))

        #     else:
        #         return redirect(url_for('contractor.index'))

        # else:

        search = "%{}%".format(q)
        page = request.args.get('page', 1, type=int)
        contractors = Contractor.query.filter(Contractor.name.like(search)).paginate(page=page, per_page=20)
        count = len(Contractor.query.filter(Contractor.name.like(search)).all())

        return render_template('contractor/index.html', page=page, contractors=contractors, count=count, search=search)
    
    else:
        # return 'なし'
        return render_template('contractor/index.html')


@contractor.route('/register', methods=['GET', 'POST'])
def register():

    form = ContractorForm()

    if form.validate_on_submit():

        id = request.form['id']
        
        # check if id already exists in the db
        exists = Contractor.query.get(id)

        if exists:
            return 'あります'

        else:
            name = request.form['name']
            title = request.form.get('title')
            representative = request.form['representative']
            zip = request.form['zip']
            prefecture = request.form['prefecture']
            city = request.form['city']
            town = request.form['town']
            address = request.form.get('address')
            bldg = request.form.get('bldg')
            registered_by = 1
            care = request.form.get('care')

            contractor = Contractor(id=id, name=name, title=title, representative=representative, zip=zip,
             prefecture=prefecture, city=city, town=town, address=address, bldg=bldg, registered_by=registered_by)

            db.session.add(contractor)
            
            if care:
                care = Satiscare(contractor_id=id, membership=care)
                db.session.add(care)

            db.session.commit()

            flash('パートナーを登録しました。', 'success')

            return redirect(url_for('contractor.profile', id=id))

    return render_template('contractor/register.html', form=form)

# show and update customer profile
@contractor.route('/<int:id>')
@contractor.route('/<int:id>/<mode>', methods=['GET', 'POST'])
def profile(id, mode=None):
    contractor = Contractor.query.get(id)

    if mode == 'edit':
        form = ContractorForm()

        if form.validate_on_submit():

            contractor.name = request.form['name']
            contractor.title = request.form.get('title')
            contractor.representative = request.form['representative']
            contractor.zip = request.form['zip']
            contractor.prefecture = request.form['prefecture']
            contractor.city = request.form['city']
            contractor.town = request.form['town']
            contractor.address = request.form.get('address')
            contractor.bldg = request.form.get('bldg')
            contractor.registered_by = 1

            # if care checkbox is checked
            care = request.form.get('care')

            # if already a satiscare member 
            is_member = Satiscare.query.filter_by(contractor_id=id).first()

            if is_member and not care:
                member = Satiscare.query.filter_by(contractor_id=id).first()
                db.session.delete(member)

            elif not is_member and care:
                care = Satiscare(contractor_id=id, membership=care)
                db.session.add(care)

            else:
                pass

            db.session.commit()

            flash('パートナー情報を更新しました。', 'success')

            return redirect(url_for('contractor.profile', id=id))

        return render_template('contractor/edit.html', contractor=contractor, form=form)

    return render_template('contractor/profile.html', contractor=contractor)
