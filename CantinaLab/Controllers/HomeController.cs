using System.Diagnostics;
using Microsoft.AspNetCore.Mvc;
using CantinaLab.Models;

namespace CantinaLab.Controllers
{
    public class HomeController : Controller
    {
        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
        public IActionResult Error()
        {
            string idCerere = HttpContext.TraceIdentifier;
            if (Activity.Current != null)
            {
                idCerere = Activity.Current.Id;
            }
            ErrorViewModel model = new ErrorViewModel { RequestId = idCerere };
            return View(model);
        }
    }
}
