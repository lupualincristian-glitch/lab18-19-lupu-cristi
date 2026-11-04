"""Verificarea automată a laboratoarelor nr. 18 și nr. 19.

Rulează pe GitHub, la fiecare Pull Request, și se poate rula și local:
    python verifica.py --lab 18 --url http://localhost:5180 --repo lab18-19-nume-prenume [--diff fisier.diff]

Pornește de la aplicația deja pornită și verifică în browser ce trebuie să se vadă
după fiecare sarcină. Valorile așteptate se calculează din numele repozitoriului,
la fel ca în Models/Varianta.cs și Models/Baza.cs.
"""
import argparse, json, re, sys, time
from playwright.sync_api import sync_playwright

# ---------------------------------------------------------------- variantele
def cod_varianta(repo):
    nume = repo.split('/')[-1].lower()
    if nume.endswith('.git'):
        nume = nume[:-4]
    if nume.startswith('lab18-19-'):
        nume = nume[9:]
    return nume, sum((i + 1) * ord(c) for i, c in enumerate(nume)) % 90 + 10

FELURI = [  # id, denumire, categorie, pret, calorii, proteine
    (1, 'Zeamă de găină', 'Supe', 22, 210, 14), (2, 'Borș roșu', 'Supe', 20, 180, 6),
    (3, 'Supă-cremă de dovleac', 'Supe', 19, 160, 4), (4, 'Pârjoale cu sos de roșii', 'Feluri principale', 38, 420, 26),
    (5, 'Piept de pui la grătar', 'Feluri principale', 42, 350, 34), (6, 'Paste cu pui & ciuperci', 'Feluri principale', 40, 520, 28),
    (7, 'Mămăligă cu brânză și smântână', 'Feluri principale', 30, 480, 18), (8, 'Piure de cartofi', 'Garnituri', 14, 210, 4),
    (9, 'Hrișcă', 'Garnituri', 12, 190, 7), (10, 'Salată de varză', 'Salate', 10, 60, 2),
    (11, 'Salată grecească', 'Salate', 25, 180, 6), (12, 'Plăcinte cu vișine', 'Desert', 15, 280, 5)]

def fel(cod, id_):
    for f in FELURI:
        if f[0] == id_:
            return {'denumire': f[1], 'categorie': f[2], 'pret': f[3] + cod % 5,
                    'calorii': f[4] + (cod * (id_ + 2)) % 30, 'proteine': f[5] + cod % 3}

def locuri_initiale(cod):
    return {1: 6 + cod % 5, 2: 2 + cod % 3, 3: 0, 4: 10 + cod % 7, 5: 4 + cod % 4, 6: 8 + cod % 6}

# ---------------------------------------------------------------- rezultate
REZ = []

def bifa(sarcina, ce, ok, motiv=''):
    REZ.append((sarcina, ce, bool(ok), '' if ok else motiv))

def incearca(sarcina, ce, functie):
    try:
        functie()
    except Exception as e:  # o greșeală într-o sarcină nu le oprește pe celelalte
        bifa(sarcina, ce, False, 'eroare la verificare: ' + str(e).split('\n')[0][:160])

class Pagina:
    """O filă de browser care ține evidența cererilor și a reîncărcărilor."""
    def __init__(self, browser, url):
        self.p = browser.new_page(locale='ro-MD')
        self.p.set_default_timeout(6000)
        self.raspunsuri, self.navigari = [], 0
        self.p.on('response', lambda r: self.raspunsuri.append(r) if r.request.resource_type in ('fetch', 'xhr') else None)
        self.p.on('framenavigated', self._nav)
        self.p.goto(url)
        self.navigari = 0

    def _nav(self, frame):
        if frame == self.p.main_frame:
            self.navigari += 1

    def ora(self):
        return self.p.inner_text('p.text-muted.small')

    def asteapta(self, n_inainte, timp=4.0):
        sfarsit = time.time() + timp
        while time.time() < sfarsit and len(self.raspunsuri) <= n_inainte:
            self.p.wait_for_timeout(100)
        self.p.wait_for_timeout(500)
        self.p.wait_for_load_state()

# ---------------------------------------------------------------- laboratorul 18
def lab18(browser, url, nume, cod):
    pg = Pagina(browser, url + '/Meniu')

    def varianta():
        t = pg.p.inner_text('footer')
        bifa('Pregătirea', 'varianta din subsol este a ta', ('Varianta: ' + nume) in t and ('cod %d' % cod) in t,
             'subsolul arată „%s”; trebuia „Varianta: %s · cod %d”. Ai modificat Varianta.cs sau Baza.cs?' % (t.strip()[:90], nume, cod))
    incearca('Pregătirea', 'varianta din subsol este a ta', varianta)

    def s1():
        r = pg.p.request.get(url + '/Meniu/Lista?categorie=Supe')
        html = r.text()
        ok = r.status == 200 and 'navbar' not in html and html.count('<tr') == 4 and 'Feluri găsite: 3' in html
        motiv = 'GET /Meniu/Lista?categorie=Supe → %d. ' % r.status
        if r.status == 200 and 'navbar' in html:
            motiv += 'Răspunsul conține meniul: acțiunea întoarce View în loc de PartialView.'
        elif r.status == 200:
            motiv += 'Tabelul nu are cele 3 supe.'
        else:
            motiv += 'Acțiunea Lista nu există sau aplicația nu a fost repornită.'
        bifa('S1', '/Meniu/Lista?categorie=Supe întoarce doar tabelul cu 3 supe', ok, motiv)
    incearca('S1', '/Meniu/Lista?categorie=Supe întoarce doar tabelul cu 3 supe', s1)

    def s2():
        ora, adresa, n = pg.ora(), pg.p.url, len(pg.raspunsuri)
        pg.p.select_option('#categorie', 'Garnituri')
        pg.asteapta(n)
        text = pg.p.inner_text('#zonaLista')
        cereri = len(pg.raspunsuri) - n
        ok = cereri >= 1 and 'Hrișcă' in text and 'Borș' not in text and pg.navigari == 0 and pg.ora() == ora
        if cereri == 0:
            motiv = 'La schimbarea categoriei nu a plecat nicio cerere fetch. Scriptul este în @section Scripts? Evenimentul este change?'
        elif pg.navigari:
            motiv = 'Pagina s-a reîncărcat.'
        elif 'navbar' in pg.p.inner_html('#zonaLista'):
            motiv = 'În zona listei a apărut toată pagina, cu meniu.'
        else:
            motiv = 'După „Garnituri”, lista nu arată doar garniturile.'
        bifa('S2', 'alegerea categoriei schimbă lista fără reîncărcare', ok, motiv)
    incearca('S2', 'alegerea categoriei schimbă lista fără reîncărcare', s2)

    def s3():
        e = fel(cod, 2)
        n = len(pg.raspunsuri)
        pg.p.select_option('#felAles', '2')
        pg.p.click('#btnNutritie')
        pg.asteapta(n)
        text = pg.p.inner_text('#nutritie')
        json_r = [r for r in pg.raspunsuri[n:] if 'json' in (r.headers.get('content-type') or '')]
        ok_val = (re.search(r'Calorii\D*%d\b' % e['calorii'], text) and re.search(r'Proteine\D*%d\b' % e['proteine'], text)
                  and re.search(r'Pre\S*\D*%d\b' % e['pret'], text))
        if not json_r:
            motiv = 'La clic nu a sosit niciun răspuns JSON. Acțiunea întoarce Json(...)?'
        elif 'undefined' in text:
            motiv = 'Pe pagină apare „undefined”: în JSON numele proprietăților încep cu literă mică.'
        else:
            motiv = 'Pentru Borș roșu trebuia „Calorii: %d kcal · Proteine: %d g · Preț: %d lei”; pe pagină: „%s”.' % (e['calorii'], e['proteine'], e['pret'], text[:80])
        bifa('S3', 'valoarea nutritivă (din JSON) apare fără reîncărcare', json_r and ok_val and pg.navigari == 0, motiv)
        if json_r:
            u = json_r[-1].url
            u2 = re.sub(r'([/=])2(?=$|[&?#])', r'\g<1>999', u)
            st = pg.p.request.get(u2).status if u2 != u else None
            bifa('S3', 'pentru un fel care nu există adresa JSON răspunde 404', st == 404,
                 'Adresa %s → %s; trebuia 404 (NotFound).' % (u2.replace(url, ''), st if st else 'nu am găsit id-ul în adresă'))
        else:
            bifa('S3', 'pentru un fel care nu există adresa JSON răspunde 404', False, 'Nu există încă adresa JSON.')
    incearca('S3', 'valoarea nutritivă (din JSON) apare fără reîncărcare', s3)

    def s4():
        n = len(pg.raspunsuri)
        pg.p.click('#zonaRezervare button[type=submit]')
        pg.asteapta(n)
        st = [r.status for r in pg.raspunsuri[n:]]
        erori = pg.p.locator('#zonaRezervare .field-validation-error').count()
        bifa('S4', 'formularul gol revine cu mesajele și codul 400, fără reîncărcare', 400 in st and erori >= 3 and pg.navigari == 0,
             'Pagina s-a reîncărcat: trimiterea nu trece prin fetch.' if pg.navigari else
             ('Codurile primite: %s, mesaje de eroare: %d. Trebuia 400 și mesajele lângă câmpuri.' % (st or 'nicio cerere', erori)))
        if pg.navigari:
            pg.p.goto(url + '/Meniu'); pg.navigari = 0
        pg.p.fill('#zonaRezervare #Nume', 'Ion Verificare')
        pg.p.fill('#zonaRezervare #Grupa', 'AAW2341')
        pg.p.select_option('#zonaRezervare #FelId', '4')
        pg.p.select_option('#zonaRezervare #Pauza', '13:10')
        n = len(pg.raspunsuri)
        pg.p.click('#zonaRezervare button[type=submit]')
        pg.asteapta(n)
        nr = cod * 10 + 1
        if pg.navigari:
            bifa('S4', 'formularul corect arată confirmarea în locul lui', False,
                 'Pagina s-a reîncărcat la a doua trimitere: ascultătorul este pe formular, nu pe zona care rămâne.')
            return
        text = pg.p.inner_text('#zonaRezervare')
        bifa('S4', 'formularul corect arată confirmarea în locul lui', ('Rezervarea nr. %d' % nr) in text and pg.navigari == 0,
             'Pagina s-a reîncărcat la a doua trimitere: ascultătorul este pe formular, nu pe zona care rămâne.' if pg.navigari else
             'Trebuia „Rezervarea nr. %d”; în zonă: „%s”.' % (nr, text.strip()[:80]))
    incearca('S4', 'formularul corect arată confirmarea în locul lui', s4)

# ---------------------------------------------------------------- laboratorul 19
def lab19(browser, url, nume, cod):
    loc = locuri_initiale(cod)
    pg = Pagina(browser, url + '/Evenimente')
    rand = lambda i: pg.p.locator('#corpTabel tr').nth(i - 1)
    locuri = lambda i: int(rand(i).locator('strong').inner_text())
    # butonul de rezervare al rândului (un rând poate avea și alte butoane, de exemplu „Renunț”)
    buton = lambda i: rand(i).locator('button').filter(has_text=re.compile('rezerv|epuizat', re.I)).first

    def varianta():
        t = pg.p.inner_text('footer')
        ok = ('Varianta: ' + nume) in t and ('cod %d' % cod) in t and locuri(1) == loc[1]
        bifa('Pregătirea', 'varianta din subsol este a ta', ok,
             'Subsolul sau locurile Concertului nu corespund variantei „%s” (cod %d). Ai modificat Varianta.cs sau Baza.cs?' % (nume, cod))
    incearca('Pregătirea', 'varianta din subsol este a ta', varianta)

    def s1():
        inainte, ora, ora2, n = locuri(1), pg.ora(), rand(2).locator('td').last.inner_text(), len(pg.raspunsuri)
        # marcăm rândul vechi: după outerHTML, elementul acesta nu mai există
        pg.p.evaluate("document.querySelector('#corpTabel tr').setAttribute('data-rand-vechi', '1')")
        buton(1).click()
        pg.asteapta(n, 5)
        cereri = len(pg.raspunsuri) - n
        ok = cereri >= 1 and pg.navigari == 0 and locuri(1) == inainte - 1 and pg.ora() == ora \
            and rand(2).locator('td').last.inner_text() == ora2 and pg.p.locator('#corpTabel tr').count() == 6
        ramas = pg.p.locator('#corpTabel tr[data-rand-vechi]').count() > 0
        ok = ok and not ramas
        if cereri == 0:
            motiv = 'La clic pe „Rezervă un loc” nu a plecat nicio cerere.'
        elif pg.navigari:
            motiv = 'Pagina s-a reîncărcat.'
        elif ramas and locuri(1) == inainte - 1:
            motiv = 'Celulele s-au schimbat, dar rândul este tot cel vechi: răspunsul a fost pus cu innerHTML, nu cu outerHTML.'
        elif pg.p.locator('#corpTabel tr').count() != 6:
            motiv = 'Tabelul nu mai are 6 rânduri: răspunsul nu înlocuiește exact rândul (outerHTML).'
        else:
            motiv = 'Rândul Concertului trebuia să arate %d locuri; arată %d.' % (inainte - 1, locuri(1))
        bifa('S1', 'rezervarea actualizează doar rândul evenimentului', ok, motiv)
    incearca('S1', 'rezervarea actualizează doar rândul evenimentului', s1)

    def s2():
        if buton(3).is_disabled():
            # butonul „Epuizat” (sarcina suplimentară E2): cererea se trimite direct
            r = pg.p.request.post(url + '/Evenimente/Rezerva/3')
            bifa('S2', 'fără locuri: codul 409 și mesajul serverului pe pagină', r.status == 409 and 'Nu mai sunt locuri' in r.text(),
                 'Butonul este „Epuizat”, dar POST /Evenimente/Rezerva/3 răspunde %d; trebuia 409 cu „Nu mai sunt locuri…”.' % r.status)
            return
        n = len(pg.raspunsuri)
        buton(3).click()
        pg.asteapta(n, 5)
        st = [r.status for r in pg.raspunsuri[n:]]
        m = pg.p.inner_text('#mesaj')
        bifa('S2', 'fără locuri: codul 409 și mesajul serverului pe pagină', 409 in st and 'Nu mai sunt locuri' in m and pg.navigari == 0,
             'Codurile primite: %s; mesajul: „%s”. Trebuia 409 și „Nu mai sunt locuri la …”.' % (st or 'nicio cerere', m[:60]))
    incearca('S2', 'fără locuri: codul 409 și mesajul serverului pe pagină', s2)

    def s3():
        b = buton(4)
        n, t0 = len(pg.raspunsuri), time.time()
        b.click()
        pg.p.wait_for_timeout(250)
        in_asteptare = b.is_disabled() and 'Se rezerv' in b.inner_text()
        pg.asteapta(n, 5)
        if len(pg.raspunsuri) == n:
            for ce in ('cât așteaptă, butonul este dezactivat și scrie „Se rezervă…”', 'două clicuri rapide rezervă un singur loc',
                       'fără răspuns de la server: mesaj și butonul revine'):
                bifa('S3', ce, False, 'La clic pe „Rezervă un loc” nu a plecat nicio cerere.')
            return
        durata = pg.raspunsuri[n].request.timing['responseEnd'] / 1000.0
        bifa('S3', 'cât așteaptă, butonul este dezactivat și scrie „Se rezervă…”', in_asteptare and durata >= 0.9,
             ('Serverul a răspuns în %.1f s: lipsește Thread.Sleep(1000) din acțiune. ' % durata if durata < 0.9 else '')
             + ('' if in_asteptare else 'Imediat după clic, butonul nu era dezactivat cu textul „Se rezervă…”.'))
        inainte = locuri(5)
        b5 = buton(5)
        b5.click(); pg.p.wait_for_timeout(60)
        try:
            b5.click(timeout=300, force=True)
        except Exception:
            pass
        pg.p.wait_for_timeout(3200)
        bifa('S3', 'două clicuri rapide rezervă un singur loc', locuri(5) == inainte - 1,
             'După două clicuri rapide locurile au scăzut de la %d la %d.' % (inainte, locuri(5)))
        pg.p.route('**/Rezerva/**', lambda r: r.abort())
        b6 = buton(6)
        b6.click(); pg.p.wait_for_timeout(800)
        m = pg.p.inner_text('#mesaj').lower()
        pg.p.unroute('**/Rezerva/**')
        bifa('S3', 'fără răspuns de la server: mesaj și butonul revine', 'nu răspunde' in m and b6.is_enabled() and 'Rezervă un loc' in b6.inner_text(),
             'Când cererea nu primește răspuns, trebuia mesajul „Serverul nu răspunde…” și butonul activ din nou; mesajul: „%s”.' % m[:60])
    incearca('S3', 'cât așteaptă, butonul este dezactivat și scrie „Se rezervă…”', s3)

    def s4():
        pg.p.goto(url + '/Evenimente'); pg.navigari = 0
        mele, total = int(pg.p.inner_text('#locurileMele')), int(pg.p.inner_text('#totalLibere'))
        n = len(pg.raspunsuri)
        buton(1).click()
        pg.asteapta(n + 1, 6)
        json_r = [r for r in pg.raspunsuri[n:] if 'json' in (r.headers.get('content-type') or '')]
        m2, t2 = pg.p.inner_text('#locurileMele'), pg.p.inner_text('#totalLibere')
        ok = json_r and pg.navigari == 0 and m2 == str(mele + 1) and t2 == str(total - 1)
        if not json_r:
            motiv = 'După rezervare nu a sosit niciun răspuns JSON pentru antet.'
        elif 'undefined' in m2 + t2 or m2.strip() == '' or t2.strip() == '':
            motiv = 'În antet a apărut un text gol sau „undefined”: în JSON numele proprietăților încep cu literă mică.'
        else:
            motiv = 'Antetul trebuia să arate %d și %d; arată %s și %s.' % (mele + 1, total - 1, m2, t2)
        bifa('S4', 'antetul se actualizează după rezervare, din JSON', ok, motiv)
    incearca('S4', 'antetul se actualizează după rezervare, din JSON', s4)

# ---------------------------------------------------------------- observații despre cod
INTERZIS = [(r'=>', 'funcție-săgeată sau lambda (=>)'), (r'\basync\b|\bawait\b', 'async/await'), (r'`', 'șir-șablon (`…`)'),
            (r'\bvar\b', 'var'), (r'\.(Where|Select|OrderBy|OrderByDescending|FirstOrDefault|Any|First|Sum|ToList)\(', 'LINQ'),
            (r'\?\?=|\?\.', 'operatorii ?. sau ??=')]

def observatii(diff_text):
    obs, fisier = [], ''
    for linie in diff_text.splitlines():
        if linie.startswith('+++ '):
            fisier = (linie[6:] if linie.startswith('+++ b/') else linie[4:]).split('\t')[0].strip()
        elif linie.startswith('+') and not linie.startswith('+++') and fisier.endswith(('.cs', '.cshtml', '.js')):
            cod = linie[1:]
            if 'RenderSectionAsync' in cod or cod.strip().startswith('//'):
                continue
            for model, nume in INTERZIS:
                if re.search(model, cod):
                    obs.append('%s: %s → `%s`' % (fisier, nume, cod.strip()[:90]))
    return obs

# ---------------------------------------------------------------- main
def main():
    a = argparse.ArgumentParser()
    a.add_argument('--lab', required=True, choices=['18', '19'])
    a.add_argument('--url', required=True)
    a.add_argument('--repo', required=True)
    a.add_argument('--diff')
    a.add_argument('--rezumat')
    a.add_argument('--commituri')
    x = a.parse_args()
    nume, cod = cod_varianta(x.repo)
    with sync_playwright() as p:
        b = p.chromium.launch()
        (lab18 if x.lab == '18' else lab19)(b, x.url.rstrip('/'), nume, cod)
        b.close()
    obs = observatii(open(x.diff, encoding='utf-8', errors='replace').read()) if x.diff else []
    trecute = sum(1 for r in REZ if r[2])
    out = ['## Laboratorul nr. %s · varianta `%s` (cod %d)' % (x.lab, nume, cod), '',
           '**%d din %d verificări trecute.**' % (trecute, len(REZ)), '',
           '| Sarcina | Ce se verifică | Rezultatul | De ce nu a trecut |', '|---|---|---|---|']
    for s, ce, ok, motiv in REZ:
        out.append('| %s | %s | %s | %s |' % (s, ce, '✅' if ok else '❌', motiv.replace('|', '/')))
    if x.commituri:
        mesaje = open(x.commituri, encoding='utf-8').read()
        lipsa = [s for s in ('S1', 'S2', 'S3', 'S4') if not re.search(r'^%s\b' % s, mesaje, re.M)]
        out += ['', '**Commit-urile:** ' + ('toate cele patru sarcini au commit (`S1`–`S4`).' if not lipsa else 'lipsesc commit-urile pentru ' + ', '.join(lipsa) + '.')]
    out += ['', '### Observații despre cod (nu schimbă rezultatul)', '']
    if obs:
        out.append('Sintaxă care nu a fost studiată: la susținere va trebui s-o explici, altfel sarcina primește jumătate din punctaj.')
        out += ['- ' + o for o in obs[:25]]
    else:
        out.append('Nicio sintaxă nestudiată în liniile adăugate.')
    text = '\n'.join(out)
    print(text)
    if x.rezumat:
        open(x.rezumat, 'a', encoding='utf-8').write(text + '\n')
    sys.exit(0 if trecute == len(REZ) else 1)

if __name__ == '__main__':
    main()
