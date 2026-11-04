namespace CantinaLab.Models
{
    // Datele despre un fel pe care serverul le trimite browserului în format JSON.
    public class InfoNutritiva
    {
        public int Calorii { get; set; }

        public int Proteine { get; set; }

        public int Pret { get; set; }
    }
}
