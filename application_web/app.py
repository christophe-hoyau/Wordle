from crypt import METHOD_BLOWFISH
from typing import ContextManager
from flask import Flask, render_template, g, request, redirect, url_for, session
import sqlite3
import Calcul_position
import random

DATABASE = 'base_de_données/database.db'
app = Flask(__name__)
app.secret_key = "2P2I"


def get_db():  # cette fonction permet de créer une connexion à la base
    # ou de récupérer la connexion existante
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def get_user(user_id):
    c = get_db().cursor()
    c.execute("SELECT name FROM profile WHERE name =?", (user_id,))
    return c.fetchall()


def get_mot(len1, len2):
    x = get_db()
    c = x.cursor()
    c.execute("SELECT mot FROM dictionnaire WHERE longueur >= ? AND longueur <= ?", (len1, len2,))
    l = c.fetchall()
    c.close()
    x.close()
    return l


@app.before_request
def before_request():
    g.user = None

    if 'user' in session:
        g.user = session['user']


def get_tentative(L, M):
    s = ''
    for i in range(len(L)):
        s += L[i]
        s += '/'
        for j in range(len(M[i])):
            s += str(M[i][j])
        s += '//'
    return s


@app.teardown_appcontext
def close_connection(exception):  # pour fermer la connexion proprement
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.before_request
def before_request():
    g.user = None

    if 'user' in session:
        g.user = session['user']


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return (render_template("Accueil_projet.html"))


@app.route('/difficulte', methods=['GET', 'POST'])
def difficulte():
    if g.user is None:
        return redirect(url_for('login'))
    else:
        session['tentative'] = []

    global mot_a_trouver, l1, l2

    if request.method == "POST":

        if request.form.get('mycheckbox') == "1":
            l1 = 5
        elif request.form.get('mycheckbox') == "2":
            l1 = 6
        elif request.form.get('mycheckbox') == "3":
            l1 = 7
        elif request.form.get('mycheckbox') == "4":
            l1 = 8
        elif request.form.get('mycheckbox') == "5":
            l1 = 9
        elif request.form.get('mycheckbox') == "6":
            l1 = 10
        elif request.form.get('mycheckbox') == "7":
            l1 = 11
        if request.form.get('checkbox') == "1":
            l2 = 5
        elif request.form.get('checkbox') == "2":
            l2 = 6
        elif request.form.get('checkbox') == "3":
            l2 = 7
        elif request.form.get('checkbox') == "4":
            l2 = 8
        elif request.form.get('checkbox') == "5":
            l2 = 9
        elif request.form.get('checkbox') == "6":
            l2 = 10
        elif request.form.get('checkbox') == "7":
            l2 = 11

        if l1 > l2:
            k = l1
            l1 = l2
            l2 = k
        l = get_mot(l1, l2)
        a = random.randint(0, len(l))
        mot_a_trouver = l[a][0]
        return redirect(url_for("jeu1"))
    else:
        return render_template('difficulte.html')


@app.route('/jeu', methods=['POST', 'GET'])
def jeu1():
    longueur_mot = len(mot_a_trouver)
    conn = get_db()
    c = conn.cursor()
    reponse_liste0 = [["." for i in range(0, longueur_mot)] for j in range(0, 7)]
    M = [[0 for i in range(0, longueur_mot)] for j in range(0, 7)]
    tentative = session['tentative']
    if len(tentative) == 0:
        if request.method == "POST":
            reponse = request.form["mot2"]
            c.execute("SELECT mot FROM dictionnaire WHERE mot =?", (reponse,))
            if len(c.fetchall()) == 0:
                return render_template("jeu1_mot_pas_dico.html", n=longueur_mot, rep1=reponse_liste0, mot=M)
            tentative.append(reponse)
            session['tentative'] = tentative
            return redirect(url_for("jeu1"))
        else:
            return render_template("jeu1.html", n=longueur_mot, rep1=reponse_liste0, mot=M)
    if len(tentative) == 1:
        if request.method == "POST":
            reponse = request.form["mot2"]
            c.execute("SELECT mot FROM dictionnaire WHERE mot =?", (reponse,))
            if len(c.fetchall()) == 0:
                L1 = list(tentative[0])
                L2 = [L1] + [["." for i in range(0, longueur_mot)] for j in range(0, 6)]
                M = Calcul_position.valid_where(mot_a_trouver, tentative[0])
                M2 = [M] + [[0 for i in range(0, longueur_mot)] for j in range(0, 6)]
                for i in range(0, 1):
                    for j in range(0, longueur_mot):
                        if M2[i][j] == 2:
                            L2[1][j] = L2[i][j]
                return render_template("jeu1_mot_pas_dico.html", n=longueur_mot, rep1=L2, mot=M2)
            L = tentative[0] + reponse
            tentative.append(reponse)
            session['tentative'] = tentative
            return redirect(url_for("jeu1"))
        else:
            L1 = list(tentative[0])
            L2 = [L1] + [["." for i in range(0, longueur_mot)] for j in range(0, 6)]
            M = Calcul_position.valid_where(mot_a_trouver, tentative[0])
            M2 = [M] + [[0 for i in range(0, longueur_mot)] for j in range(0, 6)]
            for i in range(0, 1):
                for j in range(0, longueur_mot):
                    if M2[i][j] == 2:
                        L2[1][j] = L2[i][j]
            if M2[0] == [2 for i in range(0, longueur_mot)]:
                L2[1] = ["." for i in range(0, longueur_mot)]
                if session['user'] != 'admin':
                    c.execute("INSERT INTO historique(joueur, mot_cible, tentatives) VALUES (?, ?, ?)",
                              (session['user'], mot_a_trouver, get_tentative(session['tentative'], M2)))
                    conn.commit()
                return render_template("jeufingagne.html", n=longueur_mot, rep1=L2, mot=M2)
            return render_template("jeu1.html", n=longueur_mot, rep1=L2, mot=M2)
    if len(tentative) == 2:
        if request.method == "POST":
            reponse = request.form["mot2"]
            c.execute("SELECT mot FROM dictionnaire WHERE mot =?", (reponse,))
            if len(c.fetchall()) == 0:
                L1 = list(tentative[0])
                L2 = list(tentative[1])
                L3 = [L1] + [L2] + [["." for i in range(0, longueur_mot)] for j in range(0, 5)]
                M1 = Calcul_position.valid_where(mot_a_trouver, tentative[0])
                M2 = Calcul_position.valid_where(mot_a_trouver, tentative[1])
                M3 = [M1] + [M2] + [[0 for i in range(0, longueur_mot)] for j in range(0, 5)]
                for i in range(0, 2):
                    for j in range(0, longueur_mot):
                        if M3[i][j] == 2:
                            L3[2][j] = L3[i][j]
                return render_template("jeu1_mot_pas_dico.html", n=longueur_mot, rep1=L3, mot=M3)
            L = tentative[0] + tentative[1] + reponse
            tentative.append(reponse)
            session['tentative'] = tentative
            return redirect(url_for("jeu1"))
        else:
            L1 = list(tentative[0])
            L2 = list(tentative[1])
            L3 = [L1] + [L2] + [["." for i in range(0, longueur_mot)] for j in range(0, 5)]
            M1 = Calcul_position.valid_where(mot_a_trouver, tentative[0])
            M2 = Calcul_position.valid_where(mot_a_trouver, tentative[1])
            M3 = [M1] + [M2] + [[0 for i in range(0, longueur_mot)] for j in range(0, 5)]
            for i in range(0, 2):
                for j in range(0, longueur_mot):
                    if M3[i][j] == 2:
                        L3[2][j] = L3[i][j]
            if M3[1] == [2 for i in range(0, longueur_mot)]:
                L3[2] = ["." for i in range(0, longueur_mot)]
                if session['user'] != 'admin':
                    c.execute("INSERT INTO historique(joueur, mot_cible, tentatives) VALUES (?, ?, ?)",
                              (session['user'], mot_a_trouver, get_tentative(session['tentative'], M3)))
                    conn.commit()
                return render_template("jeufingagne.html", n=longueur_mot, rep1=L3, mot=M3)
            return render_template("jeu1.html", n=longueur_mot, rep1=L3, mot=M3)
    if len(tentative) == 3:
        if request.method == "POST":
            reponse = request.form["mot2"]
            c.execute("SELECT mot FROM dictionnaire WHERE mot =?", (reponse,))
            if len(c.fetchall()) == 0:
                L1 = list(tentative[0])
                L2 = list(tentative[1])
                L3 = list(tentative[2])
                L4 = [L1] + [L2] + [L3] + [["." for i in range(0, longueur_mot)] for j in range(0, 4)]
                M1 = Calcul_position.valid_where(mot_a_trouver, tentative[0])
                M2 = Calcul_position.valid_where(mot_a_trouver, tentative[1])
                M3 = Calcul_position.valid_where(mot_a_trouver, tentative[2])
                M4 = [M1] + [M2] + [M3] + [[0 for i in range(0, longueur_mot)] for j in range(0, 4)]
                for i in range(0, 3):
                    for j in range(0, longueur_mot):
                        if M4[i][j] == 2:
                            L4[3][j] = L4[i][j]
                return render_template("jeu1_mot_pas_dico.html", n=longueur_mot, rep1=L4, mot=M4)
            L = tentative[0] + tentative[1] + tentative[2] + reponse
            tentative.append(reponse)
            session['tentative'] = tentative
            return redirect(url_for("jeu1"))
        else:
            L1 = list(tentative[0])
            L2 = list(tentative[1])
            L3 = list(tentative[2])
            L4 = [L1] + [L2] + [L3] + [["." for i in range(0, longueur_mot)] for j in range(0, 4)]
            M1 = Calcul_position.valid_where(mot_a_trouver, tentative[0])
            M2 = Calcul_position.valid_where(mot_a_trouver, tentative[1])
            M3 = Calcul_position.valid_where(mot_a_trouver, tentative[2])
            M4 = [M1] + [M2] + [M3] + [[0 for i in range(0, longueur_mot)] for j in range(0, 4)]
            for i in range(0, 3):
                for j in range(0, longueur_mot):
                    if M4[i][j] == 2:
                        L4[3][j] = L4[i][j]
            if M4[2] == [2 for i in range(0, longueur_mot)]:
                L4[3] = ["." for i in range(0, longueur_mot)]
                if session['user'] != 'admin':
                    c.execute("INSERT INTO historique(joueur, mot_cible, tentatives) VALUES (?, ?, ?)",
                              (session['user'], mot_a_trouver, get_tentative(session['tentative'], M4)))
                    conn.commit()
                return render_template("jeufingagne.html", n=longueur_mot, rep1=L4, mot=M4)
            return render_template("jeu1.html", n=longueur_mot, rep1=L4, mot=M4)
    if len(tentative) == 4:
        if request.method == "POST":
            reponse = request.form["mot2"]
            c.execute("SELECT mot FROM dictionnaire WHERE mot =?", (reponse,))
            if len(c.fetchall()) == 0:
                L1 = list(tentative[0])
                L2 = list(tentative[1])
                L3 = list(tentative[2])
                L4 = list(tentative[3])
                L5 = [L1] + [L2] + [L3] + [L4] + [["." for i in range(0, longueur_mot)] for j in range(0, 3)]
                M1 = Calcul_position.valid_where(mot_a_trouver, tentative[0])
                M2 = Calcul_position.valid_where(mot_a_trouver, tentative[1])
                M3 = Calcul_position.valid_where(mot_a_trouver, tentative[2])
                M4 = Calcul_position.valid_where(mot_a_trouver, tentative[3])
                M5 = [M1] + [M2] + [M3] + [M4] + [[0 for i in range(0, longueur_mot)] for j in range(0, 3)]
                for i in range(0, 4):
                    for j in range(0, longueur_mot):
                        if M5[i][j] == 2:
                            L5[4][j] = L5[i][j]
                return render_template("jeu1_mot_pas_dico.html", n=longueur_mot, rep1=L5, mot=M5)
            L = tentative[0] + tentative[1] + tentative[2] + tentative[3] + reponse
            tentative.append(reponse)
            session['tentative'] = tentative
            return redirect(url_for("jeu1"))
        else:
            L1 = list(tentative[0])
            L2 = list(tentative[1])
            L3 = list(tentative[2])
            L4 = list(tentative[3])
            L5 = [L1] + [L2] + [L3] + [L4] + [["." for i in range(0, longueur_mot)] for j in range(0, 3)]
            M1 = Calcul_position.valid_where(mot_a_trouver, tentative[0])
            M2 = Calcul_position.valid_where(mot_a_trouver, tentative[1])
            M3 = Calcul_position.valid_where(mot_a_trouver, tentative[2])
            M4 = Calcul_position.valid_where(mot_a_trouver, tentative[3])
            M5 = [M1] + [M2] + [M3] + [M4] + [[0 for i in range(0, longueur_mot)] for j in range(0, 3)]
            for i in range(0, 4):
                for j in range(0, longueur_mot):
                    if M5[i][j] == 2:
                        L5[4][j] = L5[i][j]
            if M5[3] == [2 for i in range(0, longueur_mot)]:
                L5[4] = ["." for i in range(0, longueur_mot)]
                if session['user'] != 'admin':
                    c.execute("INSERT INTO historique(joueur, mot_cible, tentatives) VALUES (?, ?, ?)",
                              (session['user'], mot_a_trouver, get_tentative(session['tentative'], M5)))
                    conn.commit()
                return render_template("jeufingagne.html", n=longueur_mot, rep1=L5, mot=M5)
            return render_template("jeu1.html", n=longueur_mot, rep1=L5, mot=M5)
    if len(tentative) == 5:
        if request.method == "POST":
            reponse = request.form["mot2"]
            c.execute("SELECT mot FROM dictionnaire WHERE mot =?", (reponse,))
            if len(c.fetchall()) == 0:
                L1 = list(tentative[0])
                L2 = list(tentative[1])
                L3 = list(tentative[2])
                L4 = list(tentative[3])
                L5 = list(tentative[4])
                L6 = [L1] + [L2] + [L3] + [L4] + [L5] + [["." for i in range(0, longueur_mot)] for j in range(0, 2)]
                M1 = Calcul_position.valid_where(mot_a_trouver, tentative[0])
                M2 = Calcul_position.valid_where(mot_a_trouver, tentative[1])
                M3 = Calcul_position.valid_where(mot_a_trouver, tentative[2])
                M4 = Calcul_position.valid_where(mot_a_trouver, tentative[3])
                M5 = Calcul_position.valid_where(mot_a_trouver, tentative[4])
                M6 = [M1] + [M2] + [M3] + [M4] + [M5] + [[0 for i in range(0, longueur_mot)] for j in range(0, 2)]
                for i in range(0, 5):
                    for j in range(0, longueur_mot):
                        if M6[i][j] == 2:
                            L6[5][j] = L6[i][j]
                return render_template("jeu1_mot_pas_dico.html", n=longueur_mot, rep1=L6, mot=M6)
            L = tentative[0] + tentative[1] + tentative[2] + tentative[3] + tentative[4] + reponse
            tentative.append(reponse)
            session['tentative'] = tentative
            return redirect(url_for("jeu1"))
        else:
            L1 = list(tentative[0])
            L2 = list(tentative[1])
            L3 = list(tentative[2])
            L4 = list(tentative[3])
            L5 = list(tentative[4])
            L6 = [L1] + [L2] + [L3] + [L4] + [L5] + [["." for i in range(0, longueur_mot)] for j in range(0, 2)]
            M1 = Calcul_position.valid_where(mot_a_trouver, tentative[0])
            M2 = Calcul_position.valid_where(mot_a_trouver, tentative[1])
            M3 = Calcul_position.valid_where(mot_a_trouver, tentative[2])
            M4 = Calcul_position.valid_where(mot_a_trouver, tentative[3])
            M5 = Calcul_position.valid_where(mot_a_trouver, tentative[4])
            M6 = [M1] + [M2] + [M3] + [M4] + [M5] + [[0 for i in range(0, longueur_mot)] for j in range(0, 2)]
            for i in range(0, 5):
                for j in range(0, longueur_mot):
                    if M6[i][j] == 2:
                        L6[5][j] = L6[i][j]
            if M6[4] == [2 for i in range(0, longueur_mot)]:
                L6[5] = ["." for i in range(0, longueur_mot)]
                if session['user'] != 'admin':
                    c.execute("INSERT INTO historique(joueur, mot_cible, tentatives) VALUES (?, ?, ?)",
                              (session['user'], mot_a_trouver, get_tentative(session['tentative'], M6)))
                    conn.commit()
                return render_template("jeufingagne.html", n=longueur_mot, rep1=L6, mot=M6)
            return render_template("jeu1.html", n=longueur_mot, rep1=L6, mot=M6)
    if len(tentative) == 6:
        if request.method == "POST":
            reponse = request.form["mot2"]
            c.execute("SELECT mot FROM dictionnaire WHERE mot =?", (reponse,))
            if len(c.fetchall()) == 0:
                L1 = list(tentative[0])
                L2 = list(tentative[1])
                L3 = list(tentative[2])
                L4 = list(tentative[3])
                L5 = list(tentative[4])
                L6 = list(tentative[5])
                L7 = [L1] + [L2] + [L3] + [L4] + [L5] + [L6] + [["." for i in range(0, longueur_mot)] for j in
                                                                range(0, 1)]
                M1 = Calcul_position.valid_where(mot_a_trouver, tentative[0])
                M2 = Calcul_position.valid_where(mot_a_trouver, tentative[1])
                M3 = Calcul_position.valid_where(mot_a_trouver, tentative[2])
                M4 = Calcul_position.valid_where(mot_a_trouver, tentative[3])
                M5 = Calcul_position.valid_where(mot_a_trouver, tentative[4])
                M6 = Calcul_position.valid_where(mot_a_trouver, tentative[5])
                M7 = [M1] + [M2] + [M3] + [M4] + [M5] + [M6] + [[0 for i in range(0, longueur_mot)] for j in
                                                                range(0, 1)]
                for i in range(0, 6):
                    for j in range(0, longueur_mot):
                        if M7[i][j] == 2:
                            L7[6][j] = L7[i][j]
                return render_template("jeu1_mot_pas_dico.html", n=longueur_mot, rep1=L7, mot=M7)
            L = tentative[0] + tentative[1] + tentative[2] + tentative[3] + tentative[4] + tentative[5] + reponse
            tentative.append(reponse)
            session['tentative'] = tentative
            return redirect(url_for("jeu1"))
        else:
            L1 = list(tentative[0])
            L2 = list(tentative[1])
            L3 = list(tentative[2])
            L4 = list(tentative[3])
            L5 = list(tentative[4])
            L6 = list(tentative[5])
            L7 = [L1] + [L2] + [L3] + [L4] + [L5] + [L6] + [["." for i in range(0, longueur_mot)] for j in range(0, 1)]
            M1 = Calcul_position.valid_where(mot_a_trouver, tentative[0])
            M2 = Calcul_position.valid_where(mot_a_trouver, tentative[1])
            M3 = Calcul_position.valid_where(mot_a_trouver, tentative[2])
            M4 = Calcul_position.valid_where(mot_a_trouver, tentative[3])
            M5 = Calcul_position.valid_where(mot_a_trouver, tentative[4])
            M6 = Calcul_position.valid_where(mot_a_trouver, tentative[5])
            M7 = [M1] + [M2] + [M3] + [M4] + [M5] + [M6] + [[0 for i in range(0, longueur_mot)] for j in range(0, 1)]
            for i in range(0, 6):
                for j in range(0, longueur_mot):
                    if M7[i][j] == 2:
                        L7[6][j] = L7[i][j]
            if M7[5] == [2 for i in range(0, longueur_mot)]:
                L7[6] = ["." for i in range(0, longueur_mot)]
                if session['user'] != 'admin':
                    c.execute("INSERT INTO historique(joueur, mot_cible, tentatives) VALUES (?, ?, ?)",
                              (session['user'], mot_a_trouver, get_tentative(session['tentative'], M7)))
                    conn.commit()
                return render_template("jeufingagne.html", n=longueur_mot, rep1=L7, mot=M7)
            return render_template("jeu1.html", n=longueur_mot, rep1=L7, mot=M7)
    if len(tentative) == 7:
        L1 = list(tentative[0])
        L2 = list(tentative[1])
        L3 = list(tentative[2])
        L4 = list(tentative[3])
        L5 = list(tentative[4])
        L6 = list(tentative[5])
        L7 = list(tentative[6])
        L8 = [L1] + [L2] + [L3] + [L4] + [L5] + [L6] + [L7]
        M1 = Calcul_position.valid_where(mot_a_trouver, tentative[0])
        M2 = Calcul_position.valid_where(mot_a_trouver, tentative[1])
        M3 = Calcul_position.valid_where(mot_a_trouver, tentative[2])
        M4 = Calcul_position.valid_where(mot_a_trouver, tentative[3])
        M5 = Calcul_position.valid_where(mot_a_trouver, tentative[4])
        M6 = Calcul_position.valid_where(mot_a_trouver, tentative[5])
        M7 = Calcul_position.valid_where(mot_a_trouver, tentative[6])
        M8 = [M1] + [M2] + [M3] + [M4] + [M5] + [M6] + [M7]
        if M8[6] == [2 for i in range(0, longueur_mot)]:
            if session['user'] != 'admin':
                c.execute("INSERT INTO historique(joueur, mot_cible, tentatives) VALUES (?, ?, ?)",
                          (session['user'], mot_a_trouver, get_tentative(session['tentative'], M8)))
            return render_template("jeufingagne.html", n=longueur_mot, rep1=L8, mot=M8)
        if session['user'] != 'admin':
            c.execute("INSERT INTO historique(joueur, mot_cible, tentatives) VALUES (?, ?, ?)",
                      (session['user'], mot_a_trouver, get_tentative(session['tentative'], M8)))
            conn.commit()
        return render_template("jeufinperdu.html", n=longueur_mot, rep1=L8, mot=M8,mot_bon=mot_a_trouver)


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if g.user:
            return redirect(url_for('profile'))
        return render_template("login.html")
    if request.method == "POST":
        c = get_db().cursor()
        username = request.form["username"]
        if len(get_user(username)) != 0:
            user = get_user(username)[0][0]
            c.execute("SELECT password FROM profile WHERE name =?", (user,))
            password = c.fetchall()[0][0]
            if request.form["password"] == password:
                session["user"] = request.form["username"]
                return redirect(url_for("profile"))
            else:
                return render_template("login_error.html", error="Le mot de passe est erroné")
        else:
            return render_template("login_error.html", error="L'utilisateur n'existe pas")


@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    if request.method == 'POST':
        conn = get_db()
        c = conn.cursor()
        names = request.form.get("name")
        password = request.form.get("password")
        if len(get_user(names)) != 0:
            return render_template('signup_error.html', error="L'utilisateur existe déjà")
        else:
            c.execute("INSERT INTO profile VALUES (?,?)", (names, password,))
            conn.commit()
            return redirect(url_for('login'))


@app.route('/profile', methods=["GET", "POST"])
def profile():
    if g.user:
        if request.method == "GET":
            return render_template("profile.html", user=session['user'])
        if request.method == "POST":
            session.pop('user', None)
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


@app.route('/historique', methods=["GET", "POST"])
def historique():
    if g.user:
        if session['user'] == 'admin':
            return render_template("historique_admin.html")
        else:
            c = get_db().cursor()
            c.execute("SELECT mot_cible, tentatives FROM historique WHERE joueur=?", (session['user'],))
            tentatives = c.fetchall()
            return render_template("historique.html", tentative=tentatives, longueur_tentative=len(tentatives))
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()
