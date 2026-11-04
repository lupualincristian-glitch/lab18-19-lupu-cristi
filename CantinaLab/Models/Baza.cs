namespace CantinaLab.Models
{
    // Datele aplicației, ținute în memorie. Se pierd la oprirea aplicației.
    public static class Baza
    {
        public static List<string> Categorii = new List<string> { "Supe", "Feluri principale", "Garnituri", "Salate", "Desert" };

        public static List<string> Pauze = new List<string> { "12:20", "13:10", "14:00" };

        public static List<Fel> Feluri = new List<Fel>();

        public static List<Rezervare> Rezervari = new List<Rezervare>();

        private static int urmatorulNumar = 1;

        // Pregătește meniul pentru varianta ta: prețurile, caloriile și proteinele
        // diferă puțin de la un elev la altul.
        public static void Pregateste(int cod)
        {
            Feluri.Clear();
            Rezervari.Clear();
            Adauga(1, "Zeamă de găină", "Supe", 22, 210, 14, false, cod);
            Adauga(2, "Borș roșu", "Supe", 20, 180, 6, false, cod);
            Adauga(3, "Supă-cremă de dovleac", "Supe", 19, 160, 4, true, cod);
            Adauga(4, "Pârjoale cu sos de roșii", "Feluri principale", 38, 420, 26, false, cod);
            Adauga(5, "Piept de pui la grătar", "Feluri principale", 42, 350, 34, false, cod);
            Adauga(6, "Paste cu pui & ciuperci", "Feluri principale", 40, 520, 28, false, cod);
            Adauga(7, "Mămăligă cu brânză și smântână", "Feluri principale", 30, 480, 18, true, cod);
            Adauga(8, "Piure de cartofi", "Garnituri", 14, 210, 4, true, cod);
            Adauga(9, "Hrișcă", "Garnituri", 12, 190, 7, true, cod);
            Adauga(10, "Salată de varză", "Salate", 10, 60, 2, true, cod);
            Adauga(11, "Salată grecească", "Salate", 25, 180, 6, true, cod);
            Adauga(12, "Plăcinte cu vișine", "Desert", 15, 280, 5, true, cod);
            urmatorulNumar = cod * 10 + 1;
        }

        private static void Adauga(int id, string denumire, string categorie, int pret, int calorii, int proteine, bool vegetarian, int cod)
        {
            Fel fel = new Fel();
            fel.Id = id;
            fel.Denumire = denumire;
            fel.Categorie = categorie;
            fel.Pret = pret + cod % 5;
            fel.Calorii = calorii + (cod * (id + 2)) % 30;
            fel.Proteine = proteine + cod % 3;
            fel.Vegetarian = vegetarian;
            Feluri.Add(fel);
        }

        // Felurile din categoria aleasă. Fără categorie: tot meniul.
        public static List<Fel> Filtreaza(string categorie)
        {
            List<Fel> rezultat = new List<Fel>();
            foreach (Fel fel in Feluri)
            {
                if (string.IsNullOrEmpty(categorie) || fel.Categorie == categorie)
                {
                    rezultat.Add(fel);
                }
            }
            return rezultat;
        }

        // Felul cu id-ul dat sau null, dacă nu există.
        public static Fel Gaseste(int id)
        {
            foreach (Fel fel in Feluri)
            {
                if (fel.Id == id)
                {
                    return fel;
                }
            }
            return null;
        }

        // Numărul următoarei rezervări.
        public static int UrmatorulNumar()
        {
            int numar = urmatorulNumar;
            urmatorulNumar = urmatorulNumar + 1;
            return numar;
        }
    }
}
