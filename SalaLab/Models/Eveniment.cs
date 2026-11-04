namespace SalaLab.Models
{
    // Un eveniment din sala de festivități sau din altă sală a colegiului.
    public class Eveniment
    {
        public int Id { get; set; }

        public string Denumire { get; set; }

        public DateTime Data { get; set; }

        public string Sala { get; set; }

        public int LocuriTotal { get; set; }

        public int LocuriLibere { get; set; }
    }
}
