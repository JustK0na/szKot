SELECT 
    p.id_połączenia,
    l.nazwa_linii AS nazwa_linii,
    sp.nazwa_stacji AS stacja_początkowa,
    sk.nazwa_stacji AS stacja_końcowa,
    po.model_pociągu AS model,
    pr.nazwa as przewoznik,
    p.czas_przejazdu,
    p.data,
    p.opóźnienie
FROM polaczenia p
JOIN linie_kolejowe l ON p.id_lini = l.id_linii
JOIN stacje_kolejowe sp ON p.id_stacji_początkowej = sp.id_stacji
JOIN stacje_kolejowe sk ON p.id_stacji_końcowej = sk.id_stacji
JOIN pociagi po ON p.id_pociągu = po.id_pociągu
JOIN przewoznicy pr ON po.id_przewoźnika = pr.id_przewoznika;