using Microsoft.AspNetCore.Mvc;
using SalaLab.Models;

namespace SalaLab.Controllers
{
    public class EvenimenteController : Controller
    {
        // GET /Evenimente : pagina întreagă, cu layout
        public IActionResult Index()
        {
            return View(Baza.Evenimente);
        }
        [HttpPost]
        public IActionResult Rezerva(int id)
        {
            Eveniment eveniment = Baza.Gaseste(id);
            if (eveniment == null)
            {
                return NotFound();
            }
            if (eveniment.LocuriLibere == 0)
            {
                return Conflict("Nu mai sunt locuri la " + eveniment.Denumire + ".");
            }

            eveniment.LocuriLibere = eveniment.LocuriLibere - 1;
            Baza.LocurileMele = Baza.LocurileMele + 1;
            return PartialView("_RandEveniment", eveniment);
        }

        // Acțiunile pentru cererile trimise din scriptul paginii le scrii aici.
    }
}
