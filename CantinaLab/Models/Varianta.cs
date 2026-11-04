namespace CantinaLab.Models
{
    // Varianta de date a elevului.
    // Se calculează din numele repozitoriului (lab18-19-nume-prenume), citit din .git/config.
    // NU modifica acest fișier: verificarea automată calculează aceleași valori.
    public static class Varianta
    {
        public static string Nume = "necunoscut";
        public static int Cod = 0;

        public static void Citeste(string folderProiect)
        {
            DirectoryInfo folder = new DirectoryInfo(folderProiect);
            for (int nivel = 0; nivel < 5; nivel++)
            {
                if (folder == null)
                {
                    return;
                }
                string config = Path.Combine(folder.FullName, ".git", "config");
                if (File.Exists(config))
                {
                    foreach (string rand in File.ReadAllLines(config))
                    {
                        string text = rand.Trim();
                        if (text.StartsWith("url") && text.Contains("github.com"))
                        {
                            string adresa = text.Substring(text.IndexOf('=') + 1).Trim();
                            if (adresa.EndsWith(".git"))
                            {
                                adresa = adresa.Substring(0, adresa.Length - 4);
                            }
                            string nume = adresa.Substring(adresa.LastIndexOf('/') + 1).ToLower();
                            if (nume.StartsWith("lab18-19-"))
                            {
                                nume = nume.Substring(9);
                            }
                            Nume = nume;
                            Cod = CalculeazaCod(nume);
                            return;
                        }
                    }
                }
                folder = folder.Parent;
            }
        }

        public static int CalculeazaCod(string nume)
        {
            int suma = 0;
            for (int i = 0; i < nume.Length; i++)
            {
                suma = suma + (i + 1) * nume[i];
            }
            return suma % 90 + 10;
        }
    }
}
