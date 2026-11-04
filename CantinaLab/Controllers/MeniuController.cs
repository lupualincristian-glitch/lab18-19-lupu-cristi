using Microsoft.AspNetCore.Mvc;
using CantinaLab.Models;

namespace CantinaLab.Controllers
{
    public class MeniuController : Controller
    {
        public IActionResult Index()
        {
            return View();
        }

        // Acțiunile pentru cererile trimise din scriptul paginii:

        // GET /Meniu/Lista?categorie=Supe : doar tabelul (vedere parțială) [S1]
        public IActionResult Lista(string categorie)
        {
            List<Fel> feluri = Baza.Filtreaza(categorie);
            return PartialView("_Lista", feluri);
        }

        // GET /Meniu/Nutritie?id=2 : datele nutritive în format JSON [S3]
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

        // POST /Meniu/Rezerva [S4]
        [HttpPost]
        public IActionResult Rezerva(Rezervare rezervare)
        {
            if (!ModelState.IsValid)
            {
                Response.StatusCode = 400;
                return PartialView("_Rezervare", rezervare);
            }

            ViewBag.NumarRezervare = Baza.UrmatorulNumar();
            return PartialView("_Confirmare", rezervare);
        }
    }
}