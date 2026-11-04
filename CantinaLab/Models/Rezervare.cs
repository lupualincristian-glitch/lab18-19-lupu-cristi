using System.ComponentModel.DataAnnotations;

namespace CantinaLab.Models
{
    // O rezervare de prânz, trimisă din formularul „Rezervă prânzul”.
    public class Rezervare
    {
        // Numărul rezervării îl dă serverul, după ce datele sunt valide.
        public int Numar { get; set; }

        [Display(Name = "Numele")]
        [Required(ErrorMessage = "Scrie numele.")]
        [StringLength(40, ErrorMessage = "Numele are cel mult 40 de caractere.")]
        public string Nume { get; set; }

        [Display(Name = "Grupa")]
        [Required(ErrorMessage = "Scrie grupa.")]
        [StringLength(10, ErrorMessage = "Grupa are cel mult 10 caractere.")]
        public string Grupa { get; set; }

        [Display(Name = "Felul")]
        [Range(1, 1000, ErrorMessage = "Alege felul.")]
        public int FelId { get; set; }

        [Display(Name = "Pauza")]
        [Required(ErrorMessage = "Alege pauza.")]
        public string Pauza { get; set; }
    }
}
