from flask import Flask, render_template, request, redirect, url_for, jsonify
import json, os

app = Flask(__name__)
DATA_FILE = 'data.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# ===========================
# ======== HTML ROUTES =====
# ===========================
@app.route('/')
def index():
    makanan = load_data()
    return render_template('index.html', makanan=makanan)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = load_data()
        new_item = {
            "id": len(data) + 1,
            "nama": request.form['nama'],
            "kategori": request.form['kategori'],
            "deskripsi": request.form['deskripsi']
        }
        data.append(new_item)
        save_data(data)
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    data = load_data()
    item = next((m for m in data if m["id"] == id), None)
    if not item:
        return "Data tidak ditemukan", 404
    if request.method == 'POST':
        item["nama"] = request.form['nama']
        item["kategori"] = request.form['kategori']
        item["deskripsi"] = request.form['deskripsi']
        save_data(data)
        return redirect(url_for('index'))
    return render_template('edit.html', item=item)

@app.route('/delete/<int:id>')
def delete(id):
    data = load_data()
    data = [m for m in data if m["id"] != id]
    save_data(data)
    return redirect(url_for('index'))

# ===========================
# ======== API ROUTES ======
# ===========================
@app.route('/api/makanan', methods=['GET'])
def get_makanan():
    data = load_data()
    return jsonify(data), 200

@app.route('/api/makanan/<int:id>', methods=['GET'])
def get_makanan_by_id(id):
    data = load_data()
    item = next((m for m in data if m['id'] == id), None)
    if not item:
        return jsonify({"error": "Data tidak ditemukan"}), 404
    return jsonify(item), 200

@app.route('/api/makanan', methods=['POST'])
def add_makanan():
    data = load_data()
    req_data = request.get_json()
    new_item = {
        "id": len(data) + 1,
        "nama": req_data.get('nama'),
        "kategori": req_data.get('kategori'),
        "deskripsi": req_data.get('deskripsi')
    }
    data.append(new_item)
    save_data(data)
    return jsonify(new_item), 201

@app.route('/api/makanan/<int:id>', methods=['PUT'])
def update_makanan(id):
    data = load_data()
    item = next((m for m in data if m['id'] == id), None)
    if not item:
        return jsonify({"error": "Data tidak ditemukan"}), 404

    req_data = request.get_json()
    item['nama'] = req_data.get('nama', item['nama'])
    item['kategori'] = req_data.get('kategori', item['kategori'])
    item['deskripsi'] = req_data.get('deskripsi', item['deskripsi'])
    save_data(data)
    return jsonify(item), 200

@app.route('/api/makanan/<int:id>', methods=['DELETE'])
def delete_makanan(id):
    data = load_data()
    new_data = [m for m in data if m['id'] != id]
    if len(new_data) == len(data):
        return jsonify({"error": "Data tidak ditemukan"}), 404
    save_data(new_data)
    return jsonify({"message": "Data berhasil dihapus"}), 200

if __name__ == '__main__':
    app.run(debug=True)
