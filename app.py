from flask import Flask, render_template, request, redirect, session, url_for
from datetime import datetime
import os


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ordonnance')
def ordonnance_base():
    return render_template('ordonnance.html')


@app.route('/formulaire', methods=['GET', 'POST'])
def formulaire():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        nom = request.form['nom']
        prenom = request.form['prenom']
        date = request.form['date']

        # Récupérer les prescriptions (vous devrez adapter si plusieurs prescriptions)
        medicament = request.form.getlist('medicament')
        dose = request.form.getlist('dose')
        boites = request.form.getlist('boites')
        posologie = request.form.getlist('posologie')

        # Créer une structure de données pour les prescriptions
        prescriptions = []
        for i in range(len(medicament)):
            prescriptions.append({
                'medicament': medicament[i],
                'dose': dose[i],
                'boites': boites[i],
                'posologie': posologie[i]
            })

        # Sauvegarder les informations dans la session
        session['nom'] = nom
        session['prenom'] = prenom
        session['date'] = date
        session['prescriptions'] = prescriptions

        # Rediriger vers la page de visualisation
        return redirect(url_for('visualiser_ordonnance'))

    # Pour la méthode GET, pré-remplir avec les données de la session
    nom = session.get('nom', '')
    prenom = session.get('prenom', '')
    date = session.get('date', '')
    prescriptions = session.get('prescriptions', [])

    return render_template('formulaire.html', nom=nom, prenom=prenom, date=date, prescriptions=prescriptions)

# Route pour visualiser l'ordonnance
# Clé secrète pour chiffrer les sessions (générer une clé aléatoire et sécurisée)

app.secret_key = os.urandom(24)

@app.route('/visualiser_ordonnance', methods=['GET', 'POST'])
def visualiser_ordonnance():
    if request.method == 'POST':
        # Récupérer les données du formulaire patient
        nom = request.form['nom']
        prenom = request.form['prenom']
        date = request.form['date']
        print("POST: ", nom, prenom)

        # Récupérer la date courante
        date_courante = datetime.now().strftime("%d/%m/%Y")

        # Récupérer les prescriptions dynamiques
        prescriptions = []
        index = 0

        # Boucle pour récupérer les prescriptions envoyées
        while True:
            medicament = request.form.get(f'medicament_{index}')
            dose = request.form.get(f'dose_{index}')
            boites = request.form.get(f'boites_{index}')
            posologie = request.form.get(f'posologie_{index}')
            
            if not medicament:  # Si aucun médicament n'est trouvé, on arrête la boucle
                break

            # Ajouter la prescription au tableau
            prescriptions.append({
                'medicament': medicament,
                'dose': dose,
                'boites': boites,
                'posologie': posologie
            })
            index += 1

        # Sauvegarder les informations dans la session
        session['nom'] = nom
        session['prenom'] = prenom
        session['date'] = date
        session['prescriptions'] = prescriptions

        # Rediriger vers la page de visualisation
        return redirect(url_for('visualiser_ordonnance'))

    # Si GET ou rechargement de la page, récupérer les données de la session
    nom = session.get('nom', '')
    prenom = session.get('prenom', '')
    date = session.get('date', '')
    print("GET: ", nom, prenom)
    prescriptions = session.get('prescriptions', [])
    print(prescriptions)
    date_courante = datetime.now().strftime("%d/%m/%Y")

    return render_template('visualisation.html', nom=nom, prenom=prenom, date_courante=date_courante, date=date, prescriptions=prescriptions)

@app.route('/historique')
def historique():
    return render_template('historique.html')


if __name__ == "__main__":
    app.run(debug=True)