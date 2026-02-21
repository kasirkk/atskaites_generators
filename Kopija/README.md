# Training & Wellness Report Generator

Python programma, kas nolasa treniņu un veselības CSV failus un izveido HTML atskaiti.

## Prasības

```bash
pip install pandas numpy
```

## Lietošana

1. Pārliecinieties, ka jūsu darba mapē ir šādi faili:
   - `metrics.csv` - veselības metrikas (miega, HRV, pulss, u.c.)
   - `workouts.csv` - treniņu dati

2. Palaidiet programmu:
```bash
python generate_report.py
```

3. Atveriet izveidoto `training_report.html` failu pārlūkprogrammā.

## Funkcionalitāte

Programma apstrādā šādus datus:
- ✅ Miega analīze (ilgums, dziļais miegs, REM, u.c.)
- ✅ HRV (sirds ritma variabilitāte) statistika
- ✅ Pulsa dati
- ✅ Treniņu kopsavilkums
- ✅ Treniņu tipi un ilgumi
- ✅ Sirds ritma dati treniņos

## Izejas fails

HTML atskaite ietver:
- Vizuālas kartītes ar galvenajiem rādītājiem
- Detalizētas tabulas ar datiem
- Statistiku un tendences
- Responsive dizainu (pielāgojas ekrāna izmēram)
