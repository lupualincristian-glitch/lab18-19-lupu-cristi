using Microsoft.AspNetCore.Mvc;
using CantinaLab.Models;

namespace CantinaLab.Controllers
{
    public class MeniuController : Controller
    {
        // GET /Meniu?categorie=Supe : pagina întreagă, cu layout
        public IActionResult Index(string categorie)
        {
            ViewBag.Categorie = categorie;
            List<Fel> feluri = Baza.Filtreaza(categorie);
            return View(feluri);
        }

        // Acțiunile pentru cererile trimise din scriptul paginii le scrii aici.
    }
}
