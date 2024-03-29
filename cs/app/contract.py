import os, io

from flask import Blueprint, render_template, request, current_app, send_file, abort
from google.cloud import storage

from .models import Contract

contract = Blueprint('contract', __name__)

@contract.route('/contract/<int:id>')
def contract_details(id):

    contract = Contract.query.get(id)

    return render_template('contract/contract-details.html', contract=contract)
    

@contract.route('/contract/copy/<int:id>')
def contract_copy(id):

    contract = Contract.query.get(id)

    try:
        customer_id = str(contract.customer_id)
        contractor_id = str(contract.contractor_id)
        contract_id = str(contract.id)

        bucket_name = current_app.config['GCS_BUCKET_NAME']

        storage_client = storage.Client()

        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob('contract/' + customer_id.zfill(5) + contractor_id.zfill(5) + contract_id + '.pdf')
        pdf_binary = blob.download_as_bytes()

        return send_file(
            io.BytesIO(pdf_binary),
            mimetype='application/pdf',
            as_attachment=False,
            attachment_filename='test.pdf'
        )

    except FileNotFoundError:
        abort(404)