import datetime

import hashlib

import json

from flask import Flask, jsonify, request, render_template

LEDGER = []

class Blockchain:

	def __init__(self):
		self.chain = []
		self.create_block(proof=1, previous_hash='0', transaction="GENESIS")

	def create_block(self, proof, previous_hash, transaction):
		block = {'index': len(self.chain) + 1,
				'timestamp': str(datetime.datetime.now()),
				'proof': proof,
				'previous_hash': previous_hash,
				'transaction': transaction
                }
		self.chain.append(block)
		return block

	def print_previous_block(self):
		return self.chain[-1]

	def proof_of_work(self, previous_proof):
		new_proof = 1
		check_proof = False

		while check_proof is False:
			hash_operation = hashlib.sha256(
				str(new_proof**2 - previous_proof**2).encode()).hexdigest()
			if hash_operation[:5] == '00000':
				check_proof = True
			else:
				new_proof += 1

		return new_proof

	def hash(self, block):
		encoded_block = json.dumps(block, sort_keys=True).encode()
		return hashlib.sha256(encoded_block).hexdigest()

	def chain_valid(self, chain):
		previous_block = chain[0]
		block_index = 1

		while block_index < len(chain):
			block = chain[block_index]
			if block['previous_hash'] != self.hash(previous_block):
				return False

			previous_proof = previous_block['proof']
			proof = block['proof']
			hash_operation = hashlib.sha256(
				str(proof**2 - previous_proof**2).encode()).hexdigest()

			if hash_operation[:5] != '00000':
				return False
			previous_block = block
			block_index += 1

		return True

app = Flask(__name__)

blockchain = Blockchain()

@app.route('/mine_block', methods=['GET'])
def mine_block():
	global LEDGER
	previous_block = blockchain.print_previous_block()
	previous_proof = previous_block['proof']
	proof = blockchain.proof_of_work(previous_proof)
	previous_hash = blockchain.hash(previous_block)
	transaction = LEDGER[0]
	block = blockchain.create_block(proof, previous_hash, transaction)
	LEDGER = LEDGER[1:]

	response = {'message': 'A block is MINED',
				'index': block['index'],
				'timestamp': block['timestamp'],
				'proof': block['proof'],
				'previous_hash': block['previous_hash'],
				'transaction' : transaction}

	return render_template("display.html", items = [response])

@app.route('/get_chain', methods=['GET'])
def display_chain():
	response = {'chain': blockchain.chain,
				'length': len(blockchain.chain)}
	return render_template("display.html", items=response['chain'])

@app.route('/valid', methods=['GET'])
def valid():
	valid = blockchain.chain_valid(blockchain.chain)

	if valid:
		response = {'message': 'The Blockchain is valid.'}
	else:
		response = {'message': 'The Blockchain is not valid.'}

	return render_template('valid.html', response=response)

@app.route('/meddle', methods=['GET'])
def meddle():
	blockchain.chain[-1]['previous_hash'] = '8ac9e19'
	return "MEDDLED HEHEHE"

@app.route('/', methods=['POST', 'GET'])
def add():
	global LEDGER

	print(blockchain.chain)
	if request.method == "POST":
		data = request.form
		LEDGER += [dict(data)]
		print(dict(data))
		
	return render_template('home.html')
	

@app.route('/add', methods=['GET'])
def index():
	return render_template('input.html')


if (__name__ == '__main__'):
	app.run(host='127.0.0.1', port=5000, debug = True)
