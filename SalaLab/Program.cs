using System.Globalization;
using System.Text.Encodings.Web;
using System.Text.Unicode;
using SalaLab.Models;

WebApplicationBuilder builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddControllersWithViews();

// Literele românești rămân necodificate în HTML (ă, nu &#x103;),
// ca să le citești ușor în fila Network. Nu este obiectul laboratorului.
builder.Services.AddSingleton<HtmlEncoder>(HtmlEncoder.Create(UnicodeRanges.All));

WebApplication app = builder.Build();

// Varianta ta de date se calculează din numele repozitoriului tău de pe GitHub.
// Valorile din aplicație diferă puțin de la un elev la altul. Nu modifica aceste rânduri.
Varianta.Citeste(app.Environment.ContentRootPath);
Baza.Pregateste(Varianta.Cod);

// Cultura aplicației: aceeași pe toate calculatoarele din laborator,
// indiferent de setările regionale ale sistemului de operare.
CultureInfo cultura = new CultureInfo("ro-MD");
CultureInfo.DefaultThreadCurrentCulture = cultura;
CultureInfo.DefaultThreadCurrentUICulture = cultura;

// Configure the HTTP request pipeline.
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Home/Error");
    // The default HSTS value is 30 days. You may want to change this for production scenarios, see https://aka.ms/aspnetcore-hsts.
    app.UseHsts();
}

app.UseHttpsRedirection();
app.UseRouting();

app.UseAuthorization();

app.MapStaticAssets();

app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Evenimente}/{action=Index}/{id?}")
    .WithStaticAssets();


app.Run();
