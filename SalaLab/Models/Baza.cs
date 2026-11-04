namespace SalaLab.Models
{
    // Datele aplicației, ținute în memorie. Se pierd la oprirea aplicației.
    public static class Baza
    {
        public static List<Eveniment> Evenimente = new List<Eveniment>();

        // Câte locuri ai rezervat tu de la pornirea aplicației.
        public static int LocurileMele = 0;

        // Pregătește evenimentele pentru varianta ta: locurile libere
        // diferă de la un elev la altul.
        public static void Pregateste(int cod)
        {
            Evenimente.Clear();
            LocurileMele = 0;
            Adauga(1, "Concertul corului colegiului", new DateTime(2026, 11, 5, 18, 0, 0), "Sala de festivități", 40, 6 + cod % 5);
            Adauga(2, "Seara de poezie", new DateTime(2026, 11, 7, 17, 0, 0), "Biblioteca", 20, 2 + cod % 3);
            Adauga(3, "Spectacolul de teatru „Ultima oră”", new DateTime(2026, 11, 12, 18, 30, 0), "Sala de festivități", 60, 0);
            Adauga(4, "Concursul de dans", new DateTime(2026, 11, 14, 16, 0, 0), "Sala de sport", 80, 10 + cod % 7);
            Adauga(5, "Proiecția de film", new DateTime(2026, 11, 19, 15, 0, 0), "Sala 204", 30, 4 + cod % 4);
            Adauga(6, "Întâlnirea cu absolvenții", new DateTime(2026, 11, 26, 14, 0, 0), "Sala de festivități", 50, 8 + cod % 6);
        }

        private static void Adauga(int id, string denumire, DateTime data, string sala, int total, int libere)
        {
            Eveniment eveniment = new Eveniment();
            eveniment.Id = id;
            eveniment.Denumire = denumire;
            eveniment.Data = data;
            eveniment.Sala = sala;
            eveniment.LocuriTotal = total;
            eveniment.LocuriLibere = libere;
            Evenimente.Add(eveniment);
        }

        // Evenimentul cu id-ul dat sau null, dacă nu există.
        public static Eveniment Gaseste(int id)
        {
            foreach (Eveniment eveniment in Evenimente)
            {
                if (eveniment.Id == id)
                {
                    return eveniment;
                }
            }
            return null;
        }

        // Locurile libere la toate evenimentele la un loc.
        public static int TotalLibere()
        {
            int total = 0;
            foreach (Eveniment eveniment in Evenimente)
            {
                total = total + eveniment.LocuriLibere;
            }
            return total;
        }
    }
}
