namespace SalaLab.Models
{
    // Datele pentru antetul paginii, trimise browserului în format JSON.
    public class RezumatRezervari
    {
        // Câte locuri ai rezervat tu de la pornirea aplicației.
        public int LocurileMele { get; set; }

        // Câte locuri mai sunt libere, la toate evenimentele la un loc.
        public int TotalLibere { get; set; }
    }
}
