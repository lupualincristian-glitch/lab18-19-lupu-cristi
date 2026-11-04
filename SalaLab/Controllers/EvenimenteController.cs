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

        // Acțiunile pentru cererile trimise din scriptul paginii le scrii aici.
    }
}
