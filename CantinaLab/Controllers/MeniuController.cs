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
        public IActionResult Lista(string categorie)
        {
            List<Fel> feluri = Baza.Filtreaza(categorie);
            return PartialView("_Lista", feluri);
        }
        // GET /Meniu/Nutritie?id=2 : datele nutritive în format JSON
        public IActionResult Nutritie(int id)
        {
            Fel fel = Baza.Gaseste(id);
            if (fel == null)
            {
                return NotFound();
            }

            InfoNutritiva info = new InfoNutritiva
            {
                Calorii = fel.Calorii,
                Proteine = fel.Proteine,
                Pret = fel.Pret
            };

            return Json(info);
        }

        // Acțiunile pentru cererile trimise din scriptul paginii le scrii aici.
    }
}
