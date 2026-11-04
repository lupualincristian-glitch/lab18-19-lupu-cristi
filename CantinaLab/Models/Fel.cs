namespace CantinaLab.Models
{
    // Un fel de mâncare din meniul cantinei.
    public class Fel
    {
        public int Id { get; set; }

        public string Denumire { get; set; }

        public string Categorie { get; set; }

        // Prețul unei porții, în lei.
        public int Pret { get; set; }

        // Caloriile unei porții, în kcal.
        public int Calorii { get; set; }

        // Proteinele unei porții, în grame.
        public int Proteine { get; set; }

        public bool Vegetarian { get; set; }
    }
}
